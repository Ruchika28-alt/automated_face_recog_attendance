import face_recognition
import numpy as np
import cv2
import os
from datetime import datetime
import csv

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# --- Automatically load all known faces ---
known_faces_encodings = []
known_faces_names = []

faces_folder = "faces"
os.makedirs(faces_folder, exist_ok=True)  # create if not exists

print("📸 Loading known faces from folder...")

for filename in os.listdir(faces_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        name = os.path.splitext(filename)[0]  # filename without extension
        path = os.path.join(faces_folder, filename)

        try:
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:
                known_faces_encodings.append(encodings[0])
                known_faces_names.append(name)
                print(f"✅ Loaded face for: {name}")
            else:
                print(f"⚠ No face detected in {filename}, skipping...")

        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")

if not known_faces_names:
    print("\n⚠ No faces found! Please add photos to the 'faces' folder first.")
    exit()

students = known_faces_names.copy()

# --- Prepare CSV file for attendance ---
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)
lnwriter.writerow(["Name", "Time"])

print("\n✅ Face recognition system ready.")
print("➡ Press 'Q' to quit.\n")

# --- Start video capture and recognition ---
while True:
    ret, frame = video_capture.read()
    if not ret:
        print("⚠ Camera not detected.")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_faces_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_faces_names[best_match_index]

            # Draw rectangle and label
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Mark attendance
            if name in students:
                students.remove(name)
                time_now = datetime.now().strftime("%H:%M:%S")
                lnwriter.writerow([name, time_now])
                print(f"🟩 Marked {name} present at {time_now}")

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
print("\n✅ Attendance saved successfully.")
