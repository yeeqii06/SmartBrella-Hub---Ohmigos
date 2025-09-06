
# SmartBrella Hub - Ohmigos

## 🧩 Problem Statement
On university campuses, students often face sudden weather changes such as heavy rain or extreme sun exposure. Without immediate access to umbrellas, they risk discomfort, health issues, and even missing important classes or activities. The lack of a reliable system to ensure that umbrellas are available when needed creates uncertainty and inconvenience for students. Therefore, there is a need for a smart umbrella lending system that automates borrowing and returning while allowing students to check real-time availability through a mobile app, ensuring convenience, accountability, and a better campus experience.

---

## ✅ Proposed Solution
Our proposed solution is the Smart Umbrella System, designed to make borrowing and returning umbrellas more secure and convenient. The system uses an ESP32 microcontroller as the central controller, connected to a servo motor lock that secures the umbrella when not in use. To ensure only authorized users can access the umbrella, the system integrates face detection technology, simulated through a laptop webcam, which verifies the user’s identity before unlocking. In addition, a mobile application is included to provide real-time monitoring, user registration, and borrowing history, making the system accessible and user-friendly. By combining IoT hardware, biometric verification, and mobile integration, the Smart Umbrella System addresses the challenges of umbrella sharing by improving security, accountability, and ease of use.

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


┣ 📁 SmartBrella_App/            # Flutter mobile application
 ┃ ┣ 📁 lib/
 ┃ ┃ ┣ 📁 screens/
 ┃ ┃ ┃ ┣ 📄 borrow_return.dart
 ┃ ┃ ┃ ┣ 📄 home_page.dart
 ┃ ┃ ┃ ┣ 📄 loading_page.dart 
 ┃ ┃ ┃ ┣ 📄 map_screen.dart 
 ┃ ┃ ┃ ┣ 📄 orders_model.dart 
 ┃ ┃ ┃ ┣ 📄 order_store.dart 
 ┃ ┃ ┃ ┣ 📄 orders_page.dart
 ┃ ┃ ┃ ┣ 📄 station_store.dart  
 ┃ ┃ ┃ ┣ 📄 success_page.dart 
 ┃ ┃ ┃ ┣ 📄 register_page.dart
 ┃ ┃ ┃ ┗ 📁 assets/
 ┃ ┃ ┃   ┗ 📄 logo.png
 ┃ ┃ ┗ 📄 main.dart
 ┃ ┣ 📁 pubspec.yaml 

 ┣ 📄 README.md                # Root project overview



