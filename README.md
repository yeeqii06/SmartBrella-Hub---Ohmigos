
# SmartBrella Hub - Ohmigos

## 🧩 Problem Statement
On university campuses, students often face sudden weather changes such as heavy rain or extreme sun exposure. Without immediate access to umbrellas, they risk discomfort, health issues, and even missing important classes or activities. The lack of a reliable system to ensure that umbrellas are available when needed creates uncertainty and inconvenience for students. Therefore, there is a need for a smart umbrella lending system that automates borrowing and returning while allowing students to check real-time availability through a mobile app, ensuring convenience, accountability, and a better campus experience.

---

## ✅ Proposed Solution
We propose a Smart Umbrella Station powered by ESP32 that enables students to conveniently borrow and return umbrellas using their student card (simulated with buttons in this prototype). The system automatically tracks umbrella availability at each station, records borrow/return times with RTC, and detects overdue returns. To enhance accountability and user experience, students receive real-time WhatsApp notifications (borrow, return, overdue) via CallMeBot. The station integrates an LCD display, RGB LED indicators, and a servo-based locking mechanism for smooth and secure automation. A mobile app is provided to let students check umbrella availability across stations in real time, reducing uncertainty and improving campus convenience.

---

## 📂 Project Structure  

```plaintext
📁 SmartBrella-Hub-Ohmigos
 ┣ 📁 firmware/                # ESP32 firmware (PlatformIO project)
 ┃ ┣ 📄 platformio.ini         # PlatformIO config (board, libraries)
 ┃ ┣ 📄 wokwi.toml             # Wokwi simulation settings
 ┃ ┣ 📄 diagram.json           # Wokwi wiring diagram
 ┃ ┣ 📄 README.md              # Firmware documentation
 ┃ ┣ 📂 src/                   # Main source code
 ┃ ┃ ┗ 📄 main.cpp
 ┃ ┣ 📂 lib/                   # Custom libraries (currently placeholder only)
 ┃ ┃ ┗ 📄 README
 ┃ ┗ 📂 test/                  # Unit tests (currently placeholder only)
 ┃   ┗ 📄 README

 ┣ 📁 face_recognition/        # Python face recognition module
 ┃ ┣ 📄 hub.py                 # Enrollment + kiosk (GUI + recognition + logo)
 ┃ ┣ 📄 main.py                # Minimal recognition demo (optional)
 ┃ ┣ 📂 faces/                 # Enrollment snapshots (runtime, auto-created)
 ┃ ┣ 📄 umbrella.db            # SQLite DB (runtime, auto-created)
 ┃ ┣ 📄 logo.jpg               # Project logo
 ┃ ┗ 📄 README.md              # Face recognition documentation

 ┣📁 face-recognition-system/      # Main project folder
 ┃ ┣ 📄 main.py                   # Tkinter face recognition app (entry point)
 ┃ ┣ 📄 util.py                   # Utility functions (UI helpers, recognition, etc.)
 ┃ ┣ 📄 requirements.txt          # Dependencies for Linux/Mac
 ┃ ┣ 📄 requirements_window.txt   # Dependencies for Windows
 ┃ ┣ 📄 README.md                 # Project documentation
 ┃ ┃
 ┃ ┣ 📁 db/                       # User database (auto-created at runtime)
 ┃ ┃ ┗ 📄 *.pickle                # Pickle files with face embeddings
 ┃ ┃
 ┃ ┣ 📁 logs/                     # Log files (auto-created at runtime)
 ┃ ┃ ┗ 📄 log.txt                 # Attendance / login records
 ┃ ┃
 ┃ ┗ 📁 venv/                     # (Optional) Virtual environment (ignored in Git)


 ┣ 📄 README.md                # Root project overview



