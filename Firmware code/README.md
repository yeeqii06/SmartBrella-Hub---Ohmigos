## ▶️ Quick Start (Wokwi Simulator)  
Try the project instantly in your browser:  
👉 [Run SmartBrella on Wokwi](https://wokwi.com/projects/440551645595388929)

---

## ⚡ Key Features  
- Borrow/Return with face recognition → Simulated via buttons (A, B, C).
- LCD Display → Shows borrowing/return status and umbrella availability.
- RGB LED Indicators → Green = Umbrella available, Red = Umbrella not unavailable.
- Servo Lock/Unlock → Controls umbrella access during borrow/return.
- Overdue Detection → RTC-based tracking with WhatsApp reminders.
- Penalty Calculation → Late returns automatically logged with fee details.
- Real-Time Notifications → WhatsApp messages for borrow, return, and overdue.
- NFC Tagging → To ensure same umbrella borrowed is the one being returned
---

## 🖥️ Hardware (Wokwi Circuit)  
- ESP32 DevKit V1  
- 16x2 I2C LCD (0x27)  
- RTC DS1307/DS3231  
- RGB LED (common cathode)  
- 2 Servo motor  
- Push buttons: Borrow (D4), Return (D5), Fake Return (D19), Students A/B/C (D18/D23/D32)  

See `diagram.json` for the full circuit.  

---

## 🔔 WhatsApp Setup  
1. Get a CallMeBot API key by sending `!apikey` to their WhatsApp bot.  
2. Update in `main.cpp`:  
   ```cpp
   String DEMO_PHONE = "601XXXXXXX";   // Your phone (E.164, no '+')
   String DEMO_APIKEY = "YOUR_API_KEY";

---

## ▶️ How to Run Locally (Firmware)
1. Install VS Code + PlatformIO
2. Clone this repository: git clone https://github.com/yeeqii06/SmartBrella-Hub---Ohmigos.git
3. Open the folder in VS Code with PlatformIO.
4. Required libraries (auto-installed via platformio.ini):
- LiquidCrystal_I2C
- RTClib
- ESP32Servo
5. Update main.cpp with your WhatsApp number and API key.
6. Build and upload to your ESP32 board, or run in Wokwi simulator.
