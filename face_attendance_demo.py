import cv2
import mediapipe as mp
import sqlite3
from datetime import datetime

# --- STEP 1: Initialize Mediapipe Face Detection ---
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# --- STEP 2: Initialize webcam ---
video_capture = cv2.VideoCapture(0)
print("📷 Starting camera... Press 'q' to quit")

# --- STEP 3: Connect to SQLite database ---
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# --- STEP 4: Main loop ---
while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Camera not available")
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame for face detection
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            # Draw bounding box
            mp_drawing.draw_detection(frame, detection)

            # Mark attendance (demo: using a fixed name "Greena")
            c.execute(
                "INSERT INTO attendance (name, timestamp) VALUES (?, ?)",
                ("Greena", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            cv2.putText(frame, "Greena - Marked!", 
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Face Detection Attendance', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- STEP 5: Cleanup ---
video_capture.release()
cv2.destroyAllWindows()
conn.close()
print("👋 Exiting program")
