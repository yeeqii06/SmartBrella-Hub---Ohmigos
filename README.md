# SmartBrella Hub - Ohmigos

## ▶️ Quick Start (Wokwi Simulator)  
Try the project instantly in your browser:  
👉 [Run SmartBrella on Wokwi](https://wokwi.com/projects/440551645595388929)

---

## 🧩 Problem Statement
On university campuses, students often face sudden weather changes such as heavy rain or extreme sun exposure. Without immediate access to umbrellas, they risk discomfort, health issues, and even missing important classes or activities. The lack of a reliable system to ensure that umbrellas are available when needed creates uncertainty and inconvenience for students. Therefore, there is a need for a smart umbrella lending system that automates borrowing and returning while allowing students to check real-time availability through a mobile app, ensuring convenience, accountability, and a better campus experience.

---

## ✅ Proposed Solution
We propose a Smart Umbrella Station powered by ESP32 that enables students to conveniently borrow and return umbrellas using their student card (simulated with buttons in this prototype). The system automatically tracks umbrella availability at each station, records borrow/return times with RTC, and detects overdue returns. To enhance accountability and user experience, students receive real-time WhatsApp notifications (borrow, return, overdue) via CallMeBot. The station integrates an LCD display, RGB LED indicators, and a servo-based locking mechanism for smooth and secure automation. A mobile app is provided to let students check umbrella availability across stations in real time, reducing uncertainty and improving campus convenience.

---

## ⚡ Key Features  
- Borrow/Return with Student ID → Simulated via buttons (A, B, C).
- LCD Display → Shows borrowing/return status and umbrella availability.
- RGB LED Indicators → Green = available, Red = unavailable.
- Servo Lock/Unlock → Controls umbrella access during borrow/return.
- Overdue Detection → RTC-based tracking with WhatsApp reminders.
- Penalty Calculation → Late returns automatically logged with fee details.
- Real-Time Notifications → WhatsApp messages for borrow, return, and overdue.
- App Integration → Students can check umbrella availability in each station.

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

## 📱 Mobile App (Frontend Design)  
We are developing a companion app that will:  
- Show real-time umbrella availability at each station  
- Sync with the ESP32 station data  

This will make the SmartBrella ecosystem more user-friendly and scalable for campus-wide deployment.  

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

