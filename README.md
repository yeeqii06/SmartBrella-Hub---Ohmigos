# SmartBrella Hub - Ohmigos

## ▶️ Quick Start (Wokwi Simulator)  
Try the project instantly in your browser:  
👉 [Run SmartBrella on Wokwi](https://wokwi.com/projects/440551645595388929)

---

A smart umbrella station built with **ESP32**. It tracks umbrella loans, detects overdue returns, and sends **WhatsApp notifications** via [CallMeBot](https://www.callmebot.com/). Includes **LCD, RTC, RGB LED, Servo motor**, and button-based student ID simulation.  

## 📁 SmartBrella - Ohmigos
📄 platformio.ini        # PlatformIO configuration (board, libraries)  
📄 wokwi.toml            # Wokwi simulation settings  
📄 diagram.json          # Wokwi wiring diagram  
📄 README.md             # Project documentation  
📂 src                   # Main source code  
  ┗ 📄 main.cpp  
 📂 lib                  # Custom libraries (currently placeholder only)  
  ┗ 📄 README  
📂 test                  # Unit tests (currently placeholder only)  
  ┗ 📄 README  

---

## ⚡ Features  
- Borrow/Return with student ID buttons (A, B, C)  
- LCD shows status + umbrella availability  
- RGB LED (green = available, red = none, blue = processing)  
- Servo lock/unlock when borrowing or returning  
- Overdue detection + WhatsApp reminders  
- Penalty calculation for late returns  
- Works on **real hardware** or **Wokwi simulation**  
- Check availability of umbrella in each station using app  

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

## ▶️ How to Run Locally
1. Install VS Code + PlatformIO
2. Clone this repository: git clone https://github.com/yeeqii06/SmartBrella-Hub---Ohmigos.git
3. Open the folder in VS Code with PlatformIO.
4. Required libraries (auto-installed via platformio.ini):
- LiquidCrystal_I2C
- RTClib
- ESP32Servo
5. Update main.cpp with your WhatsApp number and API key.
6. Build and upload to your ESP32 board, or run in Wokwi simulator.

