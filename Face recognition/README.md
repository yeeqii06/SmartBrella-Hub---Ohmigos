1. Repository Structure

```
.
├─ hub.py               # Enrollment + kiosk (face recognition + GUI + logo)
├─ main.py              # Minimal camera/recognition demo (optional)
├─ faces/               # Enrollment snapshots (created at runtime)
├─ umbrella.db          # SQLite DB (students + encodings); created at runtime
├─ logo.jpg             # Project logo
└─ README.md


2. **Kiosk (Python) — Enrollment & Recognition**
**Features**
- **Enroll mode**: press **SPACE** × `SAMPLES_PER_STUDENT` → small GUI pops up → enter **Matric/Phone/Name** → saved to SQLite.
- **Kiosk mode**: recognizes faces in real‑time, shows **Welcome** pop‑up with logo, sends **UNLOCK** to ESP32 (replace stub).

**Run**
```powershell
# Enroll a new student
python hub.py --mode enroll

# Operate the kiosk
python hub.py --mode kiosk
```

**Config (edit in `hub.py`)**
```python
CAM_INDEX = 0               # webcam index
MATCH_THRESHOLD = 0.60      # raise to 0.70–0.80 if needed
SAMPLES_PER_STUDENT = 5
LOGO_PATH = "logo.jpg"
```
3. **Dependencies**
```bash
pip install opencv-python numpy face_recognition
# Windows build tips for dlib:
pip install cmake
# install MSVC "Desktop development with C++"
pip install dlib==19.24.6
```

4. Data & Privacy
- Face data stored as **128‑D encodings** (not raw images) in **`umbrella.db`**.
- Snapshots in `faces/` are for debugging only — you may disable saving them.
- Do **not** publish real student data. Add to `.gitignore`:
```
umbrella.db
faces/
```
