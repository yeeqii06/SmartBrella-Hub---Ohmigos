# main.py — faithful to the tutorial, with safe RGB conversion for dlib

import os
import sys
import math
import cv2
import numpy as np
import face_recognition


def face_confidence(face_distance: float, face_match_threshold: float = 0.60) -> str:
    """Convert dlib distance to a friendly percentage (style used in the video)."""
    if face_distance is None:
        return "0%"

    range_val = 1.0 - face_match_threshold
    linear_val = (1.0 - face_distance) / (range_val * 2.0)

    if face_distance > face_match_threshold:
        return f"{round(linear_val * 100, 2)}%"
    else:
        value = (linear_val + ((1.0 - linear_val) * ((linear_val - 0.5) ** 0.2))) * 100.0
        return f"{round(value, 2)}%"


class FaceRecognition:
    # runtime state
    face_locations = []
    face_encodings = []
    face_names = []

    known_face_encodings = []
    known_face_names = []

    process_current_frame = True  # process every other frame (save CPU)

    def __init__(self, faces_dir: str = "faces", camera_index: int = 0, match_threshold: float = 0.60):
        self.faces_dir = faces_dir
        self.camera_index = camera_index
        self.match_threshold = match_threshold
        self.encode_faces()

    @staticmethod
    def _pretty_label(filename: str) -> str:
        name = os.path.splitext(filename)[0].replace("_", " ").strip()
        return name if name.isupper() else name.title()

    def encode_faces(self) -> None:
        """Load each image in faces/ and store its first face encoding + label."""
        if not os.path.isdir(self.faces_dir):
            print(f"[ERROR] Faces folder not found: {os.path.abspath(self.faces_dir)}")
            sys.exit(1)

        allowed = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        files = [f for f in os.listdir(self.faces_dir) if os.path.splitext(f)[1].lower() in allowed]
        if not files:
            print(f"[ERROR] No face images in '{self.faces_dir}'. Add your photos first.")
            sys.exit(1)

        for image_name in sorted(files):
            path = os.path.join(self.faces_dir, image_name)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if not encodings:
                print(f"[WARN] No face found in '{image_name}'. Skipping.")
                continue
            self.known_face_encodings.append(encodings[0])
            self.known_face_names.append(self._pretty_label(image_name))

        if not self.known_face_encodings:
            print("[ERROR] Could not encode any faces. Use clear, front-facing photos.")
            sys.exit(1)

        print("[INFO] Loaded known faces:", self.known_face_names)

    def run_recognition(self) -> None:
        """Open the webcam and do live recognition (every other frame)."""
        video_capture = cv2.VideoCapture(self.camera_index)
        if not video_capture.isOpened():
            sys.exit("[ERROR] Video source not found. Try camera_index=1 or check privacy settings.")

        while True:
            ret, frame = video_capture.read()
            if not ret or frame is None:
                print("[WARN] Empty frame from camera; continuing.")
                continue

            if self.process_current_frame:
                # 1/4 size for speed
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # SAFE BGR->RGB (contiguous) for dlib
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                rgb_small_frame = np.ascontiguousarray(rgb_small_frame)

                # Detect + encode
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, self.face_locations
                )

                # Match each face
                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding, tolerance=self.match_threshold
                    )
                    name = "Unknown"
                    conf = "0%"

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    if face_distances.size:
                        best_match_index = int(np.argmin(face_distances))
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                        conf = face_confidence(face_distances[best_match_index], self.match_threshold)

                    self.face_names.append(f"{name} ({conf})")

            # toggle for every-other-frame processing
            self.process_current_frame = not self.process_current_frame

            # Draw (scale back up by 4)
            for (top, right, bottom, left), display_name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                cv2.putText(
                    frame, display_name, (left + 6, bottom - 9),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA
                )

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # If matches are too strict, set match_threshold=0.65 or 0.70.
    fr = FaceRecognition(faces_dir="faces", camera_index=0, match_threshold=0.60)
    fr.run_recognition()
