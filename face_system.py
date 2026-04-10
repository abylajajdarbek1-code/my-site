import cv2
import face_recognition
import serial
import time
import tkinter as tk
from tkinter import simpledialog
import requests

# ===== Telegram =====
TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot8650433445:AAHlNoff0Qgevb4RYYzmZCUhX7CcPEDgX4o/sendMessage"
    requests.post(url, data={"chat_id": 7858293359, "text": msg})

# ===== Arduino =====
arduino = serial.Serial('COM9', 9600)
time.sleep(2)

# ===== Face база =====
img = face_recognition.load_image_file("faces/aidarbek.jpg")
known_encoding = face_recognition.face_encodings(img)[0]

# ===== Камера =====
cap = cv2.VideoCapture(0)

# ===== PIN =====
correct_pin = "1234"
attempts = 0

# ===== FACE ФУНКЦИЯ =====
def face_id():
    global attempts

    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_encodings(rgb)

    if len(faces) > 0:
        match = face_recognition.compare_faces([known_encoding], faces[0])

        if match[0]:
            status_label.config(text="ДОСТУП")
            arduino.write(b'1')
            send_telegram("Доступ открыт ✅")
            attempts = 0
        else:
            error()

    else:
        status_label.config(text="Лицо не найдено")

# ===== PIN ФУНКЦИЯ =====
def pin_code():
    global attempts

    pin = simpledialog.askstring("PIN", "Введите PIN:")

    if pin == correct_pin:
        status_label.config(text="ДОСТУП")
        arduino.write(b'1')
        send_telegram("Доступ по PIN ✅")
        attempts = 0
    else:
        error()

# ===== ҚАТЕ =====
def error():
    global attempts

    attempts += 1
    status_label.config(text="ОШИБКА")
    arduino.write(b'0')
    send_telegram("Ошибка доступа ❌")

    if attempts >= 3:
        status_label.config(text="🚨 СИГНАЛ")
        arduino.write(b'2')
        send_telegram("🚨 ВЗЛОМ!")

# ===== GUI =====
root = tk.Tk()
root.title("Security System")
root.geometry("500x500")

title = tk.Label(root, text="SECURITY SYSTEM", font=("Arial", 14))
title.pack(pady=10)

btn_face = tk.Button(root, text="Face ID", command=face_id, width=20)
btn_face.pack(pady=5)

btn_pin = tk.Button(root, text="PIN Code", command=pin_code, width=20)
btn_pin.pack(pady=5)

status_label = tk.Label(root, text="STATUS", font=("Arial", 12))
status_label.pack(pady=20)

root.mainloop()

cap.release()
arduino.close()
