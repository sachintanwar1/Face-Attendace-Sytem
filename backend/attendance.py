import face_recognition
import cv2
import pickle
import csv
import os
from datetime import datetime

ENCODINGS_FILE = "encodings.pkl"
CSV_FILE = "attendance.csv"

# Load all known encodings
known_faces = {}
if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "rb") as f:
        try:
            while True:
                data = pickle.load(f)
                known_faces.update(data)
        except EOFError:
            pass
else:
    print("❌ No registered users found.")
    exit()

# Start webcam
cap = cv2.VideoCapture(0)
print("📸 Taking attendance. Look at the camera...")

ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Failed to capture image")
    exit()

# Find faces in frame
face_locations = face_recognition.face_locations(frame)
face_encodings = face_recognition.face_encodings(frame, face_locations)

recognized_users = []

for face_encoding in face_encodings:
    for username, known_encoding in known_faces.items():
        match = face_recognition.compare_faces([known_encoding], face_encoding)[0]
        if match:
            recognized_users.append(username)

if not recognized_users:
    print("❌ No known faces detected.")
    exit()

# Save attendance in CSV
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M:%S")

# Create CSV if not exists
file_exists = os.path.isfile(CSV_FILE)
with open(CSV_FILE, "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["Name", "Date", "Time"])
    for user in recognized_users:
        writer.writerow([user, date_str, time_str])

print(f"✅ Attendance marked for: {', '.join(recognized_users)}")
