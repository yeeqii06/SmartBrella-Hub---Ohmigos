
# SmartBrella Hub - Ohmigos

## 🧩 Problem Statement
On university campuses, students often face sudden weather changes such as heavy rain or extreme sun exposure. Without immediate access to umbrellas, they risk discomfort, health issues, and even missing important classes or activities. The lack of a reliable system to ensure that umbrellas are available when needed creates uncertainty and inconvenience for students. Therefore, there is a need for a smart umbrella sharing system that automates borrowing and returning while allowing students to check real-time availability through a mobile app, ensuring convenience, accountability, and a better campus experience.

---

## ✅ Proposed Solution
Our proposed solution is SmartBrella Hub, a Smart Umbrella Sharing System, designed to make borrowing and returning umbrellas more secure and convenient. The system uses an ESP32 microcontroller as the central controller, connected to a servo motor lock that secures the umbrella when not in use. To ensure only authorized users can access the umbrella, the system integrates face detection technology, simulated through a laptop webcam, which verifies the user’s identity before unlocking. In addition, a mobile application is included to provide real-time monitoring, user login, and borrowing & returning history, making the system accessible and user-friendly. By combining IoT hardware, biometric verification, and mobile integration, the SmartBrella Hub addresses the challenges of umbrella sharing by improving security, accountability, and ease of use.

---

## 🔗 How the System Works
The SmartBrella Hub system is built with three main components working together:

## 📡 Firmware (ESP32) – Controls the umbrella station hardware (servo locks, LCD, LED, RTC)
- Handles borrow/return logic
- Detects overdue umbrellas
- Verify correct umbrellas being returned
- Sends WhatsApp reminders via CallMeBot

## 👤 Face Recognition System (Python) – Provides kiosk-style user identification.
- Students enroll their face once
- Recognition verifies identity when borrowing/returning
- Stores logs and embeddings in a local database

## 📱 SmartBrella App (Flutter) – Mobile app for users.
- Check station availability in real time
- View borrowing & returning history
- Login with their account
- Integrated map to find umbrella stations nearby

Together, these three modules create a complete IoT solution that links hardware, AI-based verification, and a user-friendly mobile interface.

---

## 📂 Project Structure  

```plaintext
📁 SmartBrella-Hub-Ohmigos
┣📁 Documentation/                  
┃ ┣ 📁 System Overview/           # System-level documentation
┃ ┃ ┣ 📄 README.md             
┃ ┃ ┗ 📄 System Overview.svg      # System flowchart
┃ ┣ 📄 Block diagram.png          # High-level block diagram
┃ ┗ 📄 Wiring Diagram.png         # Circuit wiring diagram

 ┣ 📁 Firmware code/              # ESP32 firmware (PlatformIO project)
 ┃ ┣ 📄 platformio.ini            # PlatformIO config (board, libraries)
 ┃ ┣ 📄 wokwi.toml                # Wokwi simulation settings
 ┃ ┣ 📄 diagram.json              # Wokwi wiring diagram
 ┃ ┣ 📄 README.md              
 ┃ ┣ 📂 src/                      # Main source code
 ┃ ┃ ┗ 📄 main.cpp
 ┃ ┣ 📂 lib/                      # Custom libraries (currently placeholder only)
 ┃ ┃ ┗ 📄 README
 ┃ ┗ 📂 test/                     # Unit tests (currently placeholder only)
 ┃   ┗ 📄 README

 ┣ 📁 face-registration-system/    # Face recognition + GUI (Python project)
 ┃ ┣ 📄 main.py                   # Tkinter face recognition app (entry point)
 ┃ ┣ 📄 util.py                   # Utility functions (UI helpers, recognition, etc.)
 ┃ ┣ 📄 requirements.txt          # Dependencies for Linux/Mac
 ┃ ┣ 📄 requirements_window.txt   # Dependencies for Windows
 ┃ ┣ 📄 README.md                 
 ┃ ┣ 📂 db/                       # User database (auto-created at runtime)
 ┃ ┃ ┗ 📄 *.pickle                # Pickle files with face embeddings
 ┃ ┣ 📂 logs/                     # Log files (auto-created at runtime)
 ┃ ┃ ┗ 📄 log.txt                 # Attendance / login records
 ┃ ┗ 📂 venv/                     # (Optional) Virtual environment (ignored in Git)

 ┣ 📁 SmartBrella_App/            # Flutter mobile application
 ┃ ┣ 📂 lib/                      # Main Flutter source code
 ┃ ┃ ┣ 📂 screens/                # UI screens (borrow/return, home, map, etc.)
 ┃ ┃ ┃ ┣ 📄 borrow_return.dart    # Borrow/return umbrella screen
 ┃ ┃ ┃ ┣ 📄 home_page.dart        # Main dashboard screen
 ┃ ┃ ┃ ┣ 📄 loading_page.dart     # Loading/splash screen
 ┃ ┃ ┃ ┣ 📄 map_screen.dart       # Map integration (umbrella stations)
 ┃ ┃ ┃ ┣ 📄 orders_model.dart     # Data model for orders
 ┃ ┃ ┃ ┣ 📄 order_store.dart      # State management for orders
 ┃ ┃ ┃ ┣ 📄 orders_page.dart      # Orders history screen
 ┃ ┃ ┃ ┣ 📄 station_store.dart    # State management for umbrella stations
 ┃ ┃ ┃ ┣ 📄 success_page.dart     # Success confirmation screen
 ┃ ┃ ┃ ┣ 📄 register_page.dart    # User registration screen
 ┃ ┃ ┃ ┗ 📂 assets/               # App assets (images, icons, etc.)
 ┃ ┃ ┃   ┗ 📄 logo.png
 ┃ ┃ ┗ 📄 main.dart               # App entry point
 ┃ ┣ 📄 pubspec.yaml              # Flutter dependencies & assets config
 ┃ ┣ 📄 README.md

 ┣ 📄 README.md                   # Root project overview
```



