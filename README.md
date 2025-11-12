# automated_face_recog_attendance
# 🎯 Face Recognition Attendance System in Python

This project is a **Face Recognition–based Attendance System** built using **Python**, **OpenCV**, and the **Face Recognition** library.  
It automatically marks attendance by detecting and recognizing faces through your webcam.

---

## 🚀 Features

✅ **Real-Time Face Detection** – Uses your device’s webcam to capture faces live.  
✅ **Automatic Attendance Marking** – Saves recognized names with timestamps in a CSV file.  
✅ **Daily Logs** – Creates a new attendance file for each date automatically.  
✅ **Fast & Accurate Recognition** – Uses `dlib`-based encodings from the `face_recognition` library.  

---

## ⚙️ How It Works

1. **Load Known Faces** – The system loads images from the `faces/` folder and encodes them.  
2. **Start Webcam** – Captures real-time video from your camera.  
3. **Face Detection & Matching** – Matches detected faces with the known encodings.  
4. **Attendance Logging** – Marks the recognized name and time in `Attendance_<date>.csv`.

---
