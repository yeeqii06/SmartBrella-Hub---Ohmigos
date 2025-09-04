# hub.py — Smart Umbrella Hub: enrollment (with GUI form) + kiosk + Welcome pop-up + logo
# Run:
#   python hub.py --mode enroll   # capture samples + GUI form (Matric/Phone/Name)
#   python hub.py --mode kiosk    # recognize & (stub) unlock

import os, io, time, argparse, sqlite3, textwrap
import cv2
import numpy as np
import face_recognition

# ----------------- CONFIG -----------------
DB_PATH = "umbrella.db"
SNAP_DIR = "faces"
CAM_INDEX = 0
MATCH_THRESHOLD = 0.60          # 0.55..0.80 (higher = more forgiving)
SAMPLES_PER_STUDENT = 5         # captures during enrollment

# Pop-up (ms) and re-welcome cooldown (s)
POPUP_WIDTH, POPUP_HEIGHT = 420, 150
WELCOME_MS = 2000
REWELCOME_COOLDOWN = 30.0

# Logo settings
LOGO_PATH = "logo.jpg"          # your file saved as logo.jpg
LOGO_MAX_W = 140
LOGO_MAX_H = 140
# ------------------------------------------


# ======== DB helpers ========
def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            matric TEXT PRIMARY KEY,
            phone  TEXT,
            name   TEXT,
            created_at INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS encodings (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            matric TEXT NOT NULL,
            blob   BLOB NOT NULL,
            FOREIGN KEY(matric) REFERENCES students(matric) ON DELETE CASCADE
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_enc_matric ON encodings(matric)")
    conn.commit()
    return conn

def np_to_blob(arr: np.ndarray) -> bytes:
    import io as _io
    buf = _io.BytesIO()
    np.save(buf, arr.astype(np.float32))
    return buf.getvalue()

def blob_to_np(blob: bytes) -> np.ndarray:
    import io as _io
    buf = _io.BytesIO(blob)
    buf.seek(0)
    return np.load(buf)


# ======== Face bank (in-memory) ========
class FaceBank:
    """matric -> stacked encodings; fast best-match per identity."""
    def __init__(self):
        self.bank = {}  # dict[str, np.ndarray (N,128)]

    def clear(self):
        self.bank.clear()

    def load(self, conn: sqlite3.Connection):
        self.clear()
        buckets = {}
        for matric, blob in conn.execute("SELECT matric, blob FROM encodings"):
            buckets.setdefault(matric, []).append(blob_to_np(blob))
        for m, arrs in buckets.items():
            self.bank[m] = np.vstack(arrs).astype(np.float32) if arrs else np.zeros((0, 128), np.float32)

    def names(self):
        return list(self.bank.keys())

    def best_match(self, enc: np.ndarray):
        """Return (matric, best_distance). Lower distance = better match."""
        best_m, best_d = None, None
        for m, vecs in self.bank.items():
            if vecs.size == 0:
                continue
            dists = face_recognition.face_distance(vecs, enc)  # (N,)
            d = float(np.min(dists))
            if best_d is None or d < best_d:
                best_m, best_d = m, d
        return best_m, best_d


# ======== Utils ========
def bgr_to_rgb_contig(bgr: np.ndarray) -> np.ndarray:
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return np.ascontiguousarray(rgb)

def mask_phone(phone: str) -> str:
    if not phone:
        return "-"
    return phone[:3] + "*" * max(0, len(phone) - 6) + phone[-3:]

def overlay_multiline(img, text, org=(10, 30), scale=0.7, color=(255, 255, 255), thick=2, line_gap=24):
    y = org[1]
    for line in textwrap.wrap(text, width=50):
        cv2.putText(img, line, (org[0], y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA)
        y += line_gap


# ======== Logo helpers ========
def _load_logo():
    # IMREAD_UNCHANGED will read alpha if PNG; JPG comes as BGR (3ch)
    logo = cv2.imread(LOGO_PATH, cv2.IMREAD_UNCHANGED)
    if logo is None:
        return None
    h, w = logo.shape[:2]
    scale = min(LOGO_MAX_W / max(1, w), LOGO_MAX_H / max(1, h), 1.0)
    if scale < 1.0:
        logo = cv2.resize(logo, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    # ensure RGBA (add full alpha if 3ch)
    if logo.ndim == 3 and logo.shape[2] == 3:
        alpha = np.full((logo.shape[0], logo.shape[1], 1), 255, dtype=np.uint8)
        logo = np.concatenate([logo, alpha], axis=2)
    return logo

def _paste_rgba(dst_bgr: np.ndarray, x: int, y: int, rgba: np.ndarray, alpha_scale: float = 1.0):
    """Alpha-blend RGBA onto BGR frame at (x,y). Clips as needed."""
    h, w = rgba.shape[:2]
    x2, y2 = x + w, y + h
    if x >= dst_bgr.shape[1] or y >= dst_bgr.shape[0]:
        return
    if x < 0:
        rgba = rgba[:, -x:]; w = rgba.shape[1]; x = 0; x2 = w
    if y < 0:
        rgba = rgba[-y:, :]; h = rgba.shape[0]; y = 0; y2 = h
    if x2 > dst_bgr.shape[1]:
        rgba = rgba[:, :dst_bgr.shape[1] - x]; x2 = dst_bgr.shape[1]; w = rgba.shape[1]
    if y2 > dst_bgr.shape[0]:
        rgba = rgba[:dst_bgr.shape[0] - y, :]; y2 = dst_bgr.shape[0]; h = rgba.shape[0]
    if h <= 0 or w <= 0:
        return

    overlay_rgb = rgba[:, :, :3].astype(np.float32)
    overlay_a = (rgba[:, :, 3].astype(np.float32) / 255.0) * alpha_scale
    overlay_a = overlay_a[..., None]  # (h,w,1)

    roi = dst_bgr[y:y2, x:x2].astype(np.float32)
    blended = overlay_a * overlay_rgb + (1.0 - overlay_a) * roi
    dst_bgr[y:y2, x:x2] = blended.astype(np.uint8)


# ======== Pop-up manager ========
class Popup:
    def __init__(self, title="Welcome"):
        self.title = title
        self.img = None
        self.deadline = 0.0
        self.logo = _load_logo()

    def show_welcome(self, main_text: str, sub_text: str = "", ms: int = WELCOME_MS):
        card = np.full((POPUP_HEIGHT, POPUP_WIDTH, 3), 30, np.uint8)
        cv2.rectangle(card, (0, 0), (POPUP_WIDTH - 1, POPUP_HEIGHT - 1), (90, 90, 255), 2)
        cv2.putText(card, "Welcome!", (18, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(card, main_text, (18, 85), cv2.FONT_HERSHEY_DUPLEX, 0.8, (180, 255, 180), 1, cv2.LINE_AA)
        if sub_text:
            cv2.putText(card, sub_text, (18, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (220, 220, 220), 1, cv2.LINE_AA)

        if self.logo is not None:
            lx = POPUP_WIDTH - self.logo.shape[1] - 12
            ly = 10
            _paste_rgba(card, lx, ly, self.logo, alpha_scale=1.0)

        self.img = card
        self.deadline = time.time() + ms / 1000.0

    def pump(self):
        if self.img is None:
            return
        if time.time() <= self.deadline:
            cv2.imshow(self.title, self.img)
            cv2.waitKey(1)
        else:
            try:
                cv2.destroyWindow(self.title)
            except:
                pass
            self.img = None
            self.deadline = 0.0


# ======== GUI form (Tkinter) ========
def collect_student_info_gui():
    """
    Opens a small Tkinter window to collect Matric / Phone / Name.
    Returns (matric, phone, name) or (None, None, None) if cancelled or Tk not available.
    """
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except Exception:
        # Tkinter not available
        return None, None, None

    root = tk.Tk()
    root.title("SmartBrella Enrollment")
    root.geometry("360x220")
    root.resizable(False, False)

    # Center window on screen
    try:
        root.eval('tk::PlaceWindow . center')
    except Exception:
        pass

    frm = ttk.Frame(root, padding=16)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Matric No *").grid(row=0, column=0, sticky="w")
    e_m = ttk.Entry(frm, width=28)
    e_m.grid(row=0, column=1, sticky="w")

    ttk.Label(frm, text="Phone No").grid(row=1, column=0, sticky="w", pady=(8,0))
    e_p = ttk.Entry(frm, width=28)
    e_p.grid(row=1, column=1, sticky="w", pady=(8,0))

    ttk.Label(frm, text="Name").grid(row=2, column=0, sticky="w", pady=(8,0))
    e_n = ttk.Entry(frm, width=28)
    e_n.grid(row=2, column=1, sticky="w", pady=(8,0))

    btns = ttk.Frame(frm)
    btns.grid(row=3, column=0, columnspan=2, pady=16)

    result = {"ok": False, "matric": None, "phone": None, "name": None}

    def submit():
        m = e_m.get().strip()
        p = e_p.get().strip()
        n = e_n.get().strip()
        if not m:
            messagebox.showerror("Missing field", "Matric No is required.")
            return
        result.update(ok=True, matric=m, phone=p, name=n or None)
        root.destroy()

    def cancel():
        root.destroy()

    ttk.Button(btns, text="Cancel", command=cancel).pack(side="left", padx=6)
    ttk.Button(btns, text="Submit", command=submit).pack(side="left", padx=6)

    # Enter submits
    root.bind("<Return>", lambda _e: submit())

    root.mainloop()

    if result["ok"]:
        return result["matric"], result["phone"], result["name"]
    return None, None, None


# ======== Enrollment ========
def enroll_student():
    os.makedirs(SNAP_DIR, exist_ok=True)
    conn = ensure_db()

    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        print("[ERROR] Cannot open camera.")
        return

    popup = Popup("Welcome (Enroll)")
    print("[INFO] Enrollment mode — Press SPACE to capture, Q to cancel")

    captured_encs, shots = [], 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok or frame is None:
                continue

            # Optional watermark on enroll view
            logo_rgba = _load_logo()
            if logo_rgba is not None:
                _paste_rgba(frame, 10, 10, logo_rgba, alpha_scale=0.9)

            overlay_multiline(frame, f"Enroll: SPACE to capture ({shots}/{SAMPLES_PER_STUDENT}) | Q to cancel", (10, 30))
            cv2.imshow("Enroll Student", frame)
            popup.pump()

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                print("[INFO] Enrollment canceled.")
                return
            if k == 32:  # SPACE
                rgb = bgr_to_rgb_contig(frame)
                locs = face_recognition.face_locations(rgb, number_of_times_to_upsample=2, model="hog")
                if not locs:
                    print("[WARN] No face detected, try again (closer/better light).")
                    continue
                areas = [(b - t) * (r - l) for (t, r, b, l) in locs]
                t, r, b, l = locs[int(np.argmax(areas))]

                encs = face_recognition.face_encodings(rgb, [(t, r, b, l)], num_jitters=2)
                if not encs:
                    print("[WARN] Could not extract features, try again.")
                    continue

                captured_encs.append(encs[0])
                shots += 1

                # save snapshot (audit)
                crop = frame[max(0, t):min(frame.shape[0], b), max(0, l):min(frame.shape[1], r)]
                cv2.imwrite(os.path.join(SNAP_DIR, f"enroll_{int(time.time())}_{shots}.jpg"), crop)

                print(f"[OK] Captured {shots}/{SAMPLES_PER_STUDENT}")
                if shots >= SAMPLES_PER_STUDENT:
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    # === GUI form instead of terminal input ===
    matric, phone, name = collect_student_info_gui()
    if not matric:
        print("[INFO] Enrollment aborted (no data provided).")
        return

    cur = conn.cursor()
    now = int(time.time())
    cur.execute(
        "INSERT INTO students(matric, phone, name, created_at) VALUES(?,?,?,?) "
        "ON CONFLICT(matric) DO UPDATE SET phone=excluded.phone, name=COALESCE(excluded.name, students.name)",
        (matric, phone, name, now),
    )
    for e in captured_encs:
        cur.execute("INSERT INTO encodings(matric, blob) VALUES (?, ?)", (matric, np_to_blob(e)))
    conn.commit()
    conn.close()

    # One-time welcome after enrollment
    popup.show_welcome(main_text=(name or matric), sub_text="Enrollment successful!", ms=WELCOME_MS)
    while time.time() <= popup.deadline:
        popup.pump()
        time.sleep(0.02)
    print(f"[DONE] Enrolled {matric} with {len(captured_encs)} samples.")


# ======== Kiosk (recognize + unlock) ========
def unlock_stub(matric: str):
    """Replace with your ESP32 serial write, e.g.:
        import serial
        SER = serial.Serial('COM6', 115200, timeout=0.5)
        SER.write(f'UNLOCK {matric}\\n'.encode())
    """
    print(f"[UNLOCK] Slot unlocked for {matric}")

def kiosk():
    conn = ensure_db()
    bank = FaceBank()
    bank.load(conn)
    meta = {m: (n, p) for (m, p, n) in conn.execute("SELECT matric, phone, name FROM students")}

    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        print("[ERROR] Cannot open camera.")
        return

    popup = Popup("Welcome")
    last_welcomed = {}  # matric -> last welcome time
    logo_rgba = _load_logo()

    print("[INFO] Kiosk mode — R: reload DB, Q: quit")
    print(f"[INFO] Loaded identities: {bank.names()}")

    try:
        while True:
            ok, frame = cap.read()
            if not ok or frame is None:
                continue

            if logo_rgba is not None:
                _paste_rgba(frame, 10, 10, logo_rgba, alpha_scale=0.9)

            rgb = bgr_to_rgb_contig(frame)
            locs = face_recognition.face_locations(rgb, number_of_times_to_upsample=1, model="hog")
            encs = face_recognition.face_encodings(rgb, locs)

            for (t, r, b, l), enc in zip(locs, encs):
                matric, dist = bank.best_match(enc) if enc is not None else (None, None)

                if matric is not None and dist is not None and dist <= MATCH_THRESHOLD:
                    name, phone = meta.get(matric, (None, None))
                    label = name or matric
                    color = (0, 200, 0)
                    cv2.rectangle(frame, (l, t), (r, b), color, 2)
                    cv2.rectangle(frame, (l, b - 38), (r, b), color, -1)
                    cv2.putText(frame, f"{label} ({matric}) d={dist:.3f}", (l + 6, b - 10),
                                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(frame, f"Phone: {mask_phone(phone)}", (l + 6, b + 22),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

                    # Welcome pop-up with cooldown
                    now = time.time()
                    if matric not in last_welcomed or (now - last_welcomed[matric]) > REWELCOME_COOLDOWN:
                        popup.show_welcome(main_text=label, sub_text="Have a nice day!", ms=WELCOME_MS)
                        last_welcomed[matric] = now
                        unlock_stub(matric)
                else:
                    color = (0, 0, 255)
                    cv2.rectangle(frame, (l, t), (r, b), color, 2)
                    cv2.rectangle(frame, (l, b - 38), (r, b), color, -1)
                    cv2.putText(frame, "Unknown", (l + 6, b - 10),
                                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

            overlay_multiline(frame, f"KIOSK | Thr={MATCH_THRESHOLD:.2f}   (R: reload, Q: quit)", (10, 28))
            cv2.imshow("Smart Umbrella Hub", frame)
            popup.pump()

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
            elif k == ord('r'):
                print("[INFO] Reloading DB...")
                bank.load(conn)
                meta = {m: (n, p) for (m, p, n) in conn.execute("SELECT matric, phone, name FROM students")}
                print(f"[INFO] Loaded: {bank.names()}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        conn.close()


# ======== CLI ========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Umbrella Hub")
    parser.add_argument("--mode", choices=["enroll", "kiosk"], required=True)
    args = parser.parse_args()

    os.makedirs(SNAP_DIR, exist_ok=True)

    if args.mode == "enroll":
        enroll_student()
    else:
        kiosk()
