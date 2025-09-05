// =============== Smart Umbrella – Borrow/Return + Overdue + WhatsApp (FreeRTOS) ===============
// ===============================================================================================

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "RTClib.h"
#include <ESP32Servo.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>

// ---------------- WiFi / WhatsApp Config ----------------
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASS ""

const char* DEMO_HOST   = "api.callmebot.com";
String DEMO_PATH_FORMAT = "/whatsapp.php?phone=%s&text=%s&apikey=%s";
String DEMO_PHONE       = "601111973498";   // your phone (E.164 without '+')
String DEMO_APIKEY      = "2245071";       // your CallMeBot API key
String STATION_NAME     = "Station A";

// ---------------- Pins ----------------
#define BORROW_BUTTON     4
#define RETURN_BUTTON     5
#define FAKE_RETURN_BTN   19
#define STUDENT_A_BUTTON  18
#define STUDENT_B_BUTTON  23
#define STUDENT_C_BUTTON  32
#define RED_PIN   14
#define GREEN_PIN 27
#define BLUE_PIN  26

// ---------------- LCD / RTC / SERVO ----------------
LiquidCrystal_I2C lcd(0x27, 16, 2);
RTC_DS3231 rtc;

Servo myServo;
Servo myServo2; // New Servo

bool servo1Available = true; 
bool servo2Available = true;

enum ServoState { IDLE, MOVING_ANTICLOCKWISE, MOVING_CLOCKWISE };
ServoState servoState = IDLE;
unsigned long servoMoveStartTime = 0;
const unsigned long MOVING_TIME = 1000; // ms
const int startAngle = 0;
const int stopAngle  = 90;

int activeServo = 1; // Which servo to move (1 or 2)

// ---------------- Loans / Availability ----------------
const int TOTAL_UMBRELLAS = 2;
const String UMBRELLA_ID  = "U0001";
int availableUmbrellas    = TOTAL_UMBRELLAS;

struct Loan {
  String student;
  unsigned long borrowTime;
  int loanId;
  bool overdueNotified;
};
Loan loans[10];
int loanCount = 0;
int nextLoanId = 1;

bool studentVerified = false;
String currentStudent = "";

const unsigned long overdueLimit = 8000; // 10s demo

// ---------------- Deferred Action ----------------
enum ActionType { NONE, BORROW_ACTION, RETURN_ACTION };
ActionType pendingAction = NONE;
String pendingStudent = "";
bool pendingLate = false;
float pendingPenalty = 0.0f;

// ---------------- Logger ----------------
void logWithTime(const char* level, const char* fmt, ...) {
  char buf[256];
  va_list args;
  va_start(args, fmt);
  vsnprintf(buf, sizeof(buf), fmt, args);
  va_end(args);

  String ts = rtc.now().timestamp(DateTime::TIMESTAMP_FULL);
  ts.replace("\r", ""); // sanitize
  Serial.printf("[%s] | %s | %s\r\n", level, ts.c_str(), buf);
}

// ---------------- WiFi / HTTP helpers ----------------
void ensureWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < 15000) {
    delay(50);
  }
}

String urlEncode(const String& s){
  String o; o.reserve(s.length()*3);
  for (char c : s) {
    if (isalnum(c) || c=='-'||c=='_'||c=='.'||c=='~') o += c;
    else if (c==' ') o += "%20";
    else { char b[4]; sprintf(b,"%%%02X",(uint8_t)c); o += b; }
  }
  return o;
}

bool sendWhatsAppGET(const String& message){
  ensureWiFi();
  if (WiFi.status() != WL_CONNECTED) {
    logWithTime("WA", "No WiFi, send aborted");
    return false;
  }

  WiFiClientSecure client; 
  client.setInsecure();
  HTTPClient http;

  String enc = urlEncode(message);
  char path[360];
  snprintf(path, sizeof(path), DEMO_PATH_FORMAT.c_str(),
           DEMO_PHONE.c_str(), enc.c_str(), DEMO_APIKEY.c_str());
  String url = String("https://") + DEMO_HOST + String(path);

  if (!http.begin(client, url)) {
    logWithTime("WA", "http.begin failed");
    return false;
  }
  int code = http.GET();
  http.end();
  logWithTime("WA", "Sent to API -> %d", code);
  return code >= 200 && code < 300;
}

// ---------------- FreeRTOS Task ----------------
void sendTask(void *param) {
  String *pMsg = (String*)param;
  String msg = *pMsg;
  delete pMsg;

  sendWhatsAppGET(msg);
  vTaskDelete(NULL);
}

void spawnSendTask(const String& msg) {
  String *copy = new String(msg);
  BaseType_t ok = xTaskCreate(sendTask, "waSend", 8192, (void*)copy, 1, NULL);
  if (ok != pdPASS) {
    logWithTime("WA", "xTaskCreate failed, sending inline");
    sendWhatsAppGET(msg);
  }
}

// ---------------- Message templates ----------------
void notifyBorrow(const String& studentName, const String& umbId){
  String msg = "Hi " + studentName + ", you’ve borrowed an umbrella from " + STATION_NAME +
               ". Please return within 24 hours. (ID: " + umbId + ")";
  spawnSendTask(msg);
}

void notifyOverdue(const String& studentName){
  String msg = "Reminder: The umbrella you borrowed is overdue. Please return it ASAP.";
  spawnSendTask(msg);
}

void notifyReturn(const String& studentName, bool late, float penalty){
  String msg;
  if (late) {
    msg = "Thanks for returning the umbrella, " + studentName +
          ". Penalty RM" + String(penalty, 2) + " will be charged.";
  } else {
    msg = "Thanks for returning the umbrella on time, " + studentName + "!";
  }
  spawnSendTask(msg);
}

// ---------------- UI helpers ----------------
void setLED(bool redOn, bool greenOn, bool blueOn) {
  digitalWrite(RED_PIN,   redOn   ? HIGH : LOW);
  digitalWrite(GREEN_PIN, greenOn ? HIGH : LOW);
  digitalWrite(BLUE_PIN,  blueOn  ? HIGH : LOW);
}

void showLine(const String& l1, const String& l2 = "") {
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print(l1);
  lcd.setCursor(0, 1); lcd.print(l2);
  logWithTime("LCD", "%s | %s", l1.c_str(), l2.c_str());
}

void showIdleScreen() { 
  showLine("Tap your", "student ID"); 
  logWithTime("INFO", "Umbrellas available: %d", availableUmbrellas);
}

// ---------------- Loan helpers ----------------
int findLoanIndexByStudent(const String &student) {
  for (int i = 0; i < loanCount; ++i) if (loans[i].student == student) return i;
  return -1;
}
bool studentHasLoan(const String &student) { return findLoanIndexByStudent(student) != -1; }

void addLoan(const String &student) {
  if (loanCount >= 10) return;
  loans[loanCount].student = student;
  loans[loanCount].borrowTime = millis();
  loans[loanCount].loanId = nextLoanId++;
  loans[loanCount].overdueNotified = false;
  loanCount++;
}
void removeLoanAtIndex(int idx) {
  if (idx < 0 || idx >= loanCount) return;
  for (int i = idx; i < loanCount - 1; ++i) loans[i] = loans[i + 1];
  loanCount--;
}

// ---------------- ID tap handler ----------------
void handleStudent(int studentID) {
  String name;
  switch (studentID) {
    case 1: name = "Student A"; break;
    case 2: name = "Student B"; break;
    case 3: name = "Student C"; break;
    default: name = "Unknown"; break;
  }
  currentStudent = name;
  studentVerified = true;

  if (studentHasLoan(name)) showLine(name, "Already borrowed");
  else                      showLine(name, "ID Verified");

  logWithTime("ID", "%s tapped", name.c_str());
  delay(200);
}

// ---------------- Servo state machine ----------------
void updateServo() {
  if (servoState == IDLE) return;

  unsigned long progress = millis() - servoMoveStartTime;
  Servo *servoPtr = (activeServo == 1) ? &myServo : &myServo2; // select active servo

  if (servoState == MOVING_ANTICLOCKWISE) {
    if (progress <= MOVING_TIME) {
      long angle = map(progress, 0, MOVING_TIME, startAngle, stopAngle);
      servoPtr->write(angle);
    } else {
      servoPtr->write(stopAngle);
      servoState = MOVING_CLOCKWISE;
      servoMoveStartTime = millis();
      showLine("Motor " + String(activeServo), "Closing...");
      logWithTime("SERVO", "Finished opening Servo %d, now closing...", activeServo);
    }
  }
  else if (servoState == MOVING_CLOCKWISE) {
    if (progress <= MOVING_TIME) {
      long angle = map(progress, 0, MOVING_TIME, stopAngle, startAngle);
      servoPtr->write(angle);
    } else {
      servoPtr->write(startAngle);
      servoState = IDLE;
      logWithTime("SERVO", "Cycle complete (Servo %d open + close)", activeServo);

      if (pendingAction == BORROW_ACTION) {
        notifyBorrow(pendingStudent, UMBRELLA_ID);
      } else if (pendingAction == RETURN_ACTION) {
        notifyReturn(pendingStudent, pendingLate, pendingPenalty);
      }
      pendingAction = NONE;

      // Back to idle screen after each action
      showIdleScreen();
    }
  }
}

// ---------------- Arduino setup/loop ----------------
void setup() {
  pinMode(BORROW_BUTTON, INPUT_PULLUP);
  pinMode(RETURN_BUTTON, INPUT_PULLUP);
  pinMode(FAKE_RETURN_BTN, INPUT_PULLUP);
  pinMode(STUDENT_A_BUTTON, INPUT_PULLUP);
  pinMode(STUDENT_B_BUTTON, INPUT_PULLUP);
  pinMode(STUDENT_C_BUTTON, INPUT_PULLUP);

  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  lcd.init();
  lcd.backlight();
  Serial.begin(115200);

  myServo.attach(16);
  myServo2.attach(17);

  if (!rtc.begin()) {
    logWithTime("SYS", "Couldn't find RTC");
    while (1) delay(10);
  }

  showIdleScreen();
  setLED(availableUmbrellas == 0, availableUmbrellas > 0, false);

  ensureWiFi();
  logWithTime("SYS", "System ready. Umbrellas available: %d", availableUmbrellas);
}

void loop() {
  updateServo();

  if (digitalRead(STUDENT_A_BUTTON) == LOW) handleStudent(1);
  if (digitalRead(STUDENT_B_BUTTON) == LOW) handleStudent(2);
  if (digitalRead(STUDENT_C_BUTTON) == LOW) handleStudent(3);

  // Borrow
  if (digitalRead(BORROW_BUTTON) == LOW) {
  if (!studentVerified) {
    showLine("Tap ID first", "to borrow");
  } else if (studentHasLoan(currentStudent)) {
    showLine("Already borrowed", "Return first");
  } else if (availableUmbrellas <= 0) {
    showLine("No umbrella", "available");
    delay(1000);
    showIdleScreen();
  } else {
    // Select which servo has umbrella
    if (servo1Available) {
      activeServo = 1;
      servo1Available = false;
    } else if (servo2Available) {
      activeServo = 2;
      servo2Available = false;
    } else {
      showLine("No umbrella", "available");
      delay(1000);
      showIdleScreen();
    }

    addLoan(currentStudent);
    if (availableUmbrellas > 0) availableUmbrellas--;

    showLine("Borrowed by", currentStudent + " M" + String(activeServo));

    logWithTime("BORROW", "%s borrowed %s", currentStudent.c_str(), UMBRELLA_ID.c_str());

    servoState = MOVING_ANTICLOCKWISE;
    servoMoveStartTime = millis();

    pendingAction  = BORROW_ACTION;
    pendingStudent = currentStudent;

    studentVerified = false;
    currentStudent = "";
    setLED(availableUmbrellas == 0, availableUmbrellas > 0, false);
  }
}

  // Return
  if (digitalRead(RETURN_BUTTON) == LOW) {
  if (!studentVerified) {
    showLine("Tap ID first", "to return");
  } else {
    int idx = findLoanIndexByStudent(currentStudent);
    if (idx == -1) {
      showLine("No active loan", "Cannot return");
      logWithTime("WARN", "%s tried to return without active loan", currentStudent.c_str());
    } else {
      unsigned long totalBorrowTime = millis() - loans[idx].borrowTime;
      bool isLate = (totalBorrowTime > overdueLimit);
      float penalty = isLate ? ((totalBorrowTime - overdueLimit) / 1000) * 0.50f : 0.0f;

      // Which servo to open for returning? 
      // Free one that was locked: simple logic (first free one)
      if (!servo1Available) { activeServo = 1; servo1Available = true; }
      else if (!servo2Available) { activeServo = 2; servo2Available = true; }

      if (isLate) {
        char buf[17];
        snprintf(buf, sizeof(buf), "Penalty RM%.2f", penalty);
        showLine("Late return!", buf);
      } else {
        showLine("Thanks for", "returning on time!");
        showLine("Returning...", "Motor " + String(activeServo));
      }

      servoState = MOVING_ANTICLOCKWISE;
      servoMoveStartTime = millis();

      pendingAction  = RETURN_ACTION;
      pendingStudent = currentStudent;
      pendingLate    = isLate;
      pendingPenalty = penalty;

      removeLoanAtIndex(idx);
      if (availableUmbrellas < TOTAL_UMBRELLAS) availableUmbrellas++;

      studentVerified = false;
      currentStudent = "";
      setLED(availableUmbrellas == 0, availableUmbrellas > 0, false);
    }
  }
}

  // Fake return
  if (digitalRead(FAKE_RETURN_BTN) == LOW) {
    showLine("Invalid Return!");
    logWithTime("WARN", "Invalid return attempted");
    delay(1000);
    showIdleScreen();
  }

  // Overdue scan
  for (int i = 0; i < loanCount; ++i) {
    unsigned long age = millis() - loans[i].borrowTime;
    if (age > overdueLimit && !loans[i].overdueNotified) {
      notifyOverdue(loans[i].student);
      loans[i].overdueNotified = true;
      logWithTime("OVERDUE", "Reminder queued for %s", loans[i].student.c_str());
    }
  }

  delay(5);
}
