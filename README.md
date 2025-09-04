# SmartBrella Hub - Ohmigos

## 🧩 Problem Statement
On university campuses, students often face sudden weather changes such as heavy rain or extreme sun exposure. Without immediate access to umbrellas, they risk discomfort, health issues, and even missing important classes or activities. The lack of a reliable system to ensure that umbrellas are available when needed creates uncertainty and inconvenience for students. Therefore, there is a need for a smart umbrella lending system that automates borrowing and returning while allowing students to check real-time availability through a mobile app, ensuring convenience, accountability, and a better campus experience.

---

## ✅ Proposed Solution
We propose a Smart Umbrella Station powered by ESP32 that enables students to conveniently borrow and return umbrellas using their student card (simulated with buttons in this prototype). The system automatically tracks umbrella availability at each station, records borrow/return times with RTC, and detects overdue returns. To enhance accountability and user experience, students receive real-time WhatsApp notifications (borrow, return, overdue) via CallMeBot. The station integrates an LCD display, RGB LED indicators, and a servo-based locking mechanism for smooth and secure automation. A mobile app is provided to let students check umbrella availability across stations in real time, reducing uncertainty and improving campus convenience.

---

📁 SmartBrella Hub - Ohmigos
 ┣📁 firmware
  ┣ 📄 platformio.ini      # PlatformIO configuration (board, libraries)
  ┣ 📄 wokwi.toml          # Wokwi simulation settings
  ┣ 📄 diagram.json        # Wokwi wiring diagram
  ┣ 📄 README.md           # Project documentation
  ┣ 📂 src                 # Main source code
  ┃    ┗ 📄 main.cpp
  ┣ 📂 lib                 # Custom libraries (currently placeholder only)
  ┃    ┗ 📄 README
  ┣ 📂 test                # Unit tests (currently placeholder only)
  ┃    ┗ 📄 README
 
 ┣📁 Face recognition  
 ├─ hub.py               # Enrollment + kiosk (face recognition + GUI + logo)
├─ main.py              # Minimal camera/recognition demo (optional)
├─ faces/               # Enrollment snapshots (created at runtime)
├─ umbrella.db          # SQLite DB (students + encodings); created at runtime
├─ logo.jpg             # Project logo
└─ README.md
