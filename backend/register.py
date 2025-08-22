import face_recognition
import cv2
import pickle
import sys
import os

# Check if username is provided
if len(sys.argv) < 2:
    print("❌ Username required")
    sys.exit(1)

username = sys.argv[1]

# Create encodings file if it doesn’t exist
ENCODINGS_FILE = "encodings.pkl"
if not os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "wb") as f:
        pass

# Capture face from webcam
cap = cv2.VideoCapture(0)
print(f"📸 Capturing face for {username}. Please look at the camera...")

ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Failed to capture image")
    sys.exit(1)

# Encode face
face_locations = face_recognition.face_locations(frame)
encodings = face_recognition.face_encodings(frame, face_locations)

if encodings:
    # Save encoding with username
    with open(ENCODINGS_FILE, "ab") as f:
        pickle.dump({username: encodings[0]}, f)
    print(f"✅ Registered {username}")
else:
    print("❌ No face detected. Try again.")
