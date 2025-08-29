# SmartBrella Hub - Ohmigos
[![Run on Wokwi](https://img.shields.io/badge/Run%20on-Wokwi-blue?logo=wokwi)](https://wokwi.com/projects/new?template=esp32-devkit-v1)  

A smart umbrella station built with **ESP32**. It tracks umbrella loans, detects overdue returns, and sends **WhatsApp notifications** via [CallMeBot](https://www.callmebot.com/). Includes **LCD, RTC, RGB LED, Servo motor**, and button-based student ID simulation.  

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
- Servo motor  
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

📁 YourProject
 ┣ 📄 platformio.ini   # PlatformIO config (board + libraries)
 ┣ 📄 wokwi.toml       # Wokwi simulation settings
 ┣ 📄 diagram.json     # Wokwi circuit diagram
 ┣ 📂 src              # source code (main.cpp)
 ┣ 📂 lib              # Extra libraries (if any)
 ┗ 📄 README.md        # Project documentation

