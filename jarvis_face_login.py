import face_recognition
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import time
import sys
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Use a male voice
engine.setProperty('voice', voices[0].id)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def show_popup_gif(gif_path, duration=5):
    root = tk.Tk()
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", 'black')
    root.configure(bg='black')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    gif = Image.open(gif_path)
    frames = []

    try:
        while True:
            frame = gif.copy()
            frames.append(ImageTk.PhotoImage(frame.convert("RGBA")))
            gif.seek(len(frames))
    except EOFError:
        pass

    label = tk.Label(root, bg='black')
    label.pack()

    x = int((screen_width - gif.width) / 2)
    y = int((screen_height - gif.height) / 2)
    root.geometry(f"{gif.width}x{gif.height}+{x}+{y}")

    def update(index):
        frame = frames[index]
        label.configure(image=frame)
        index = (index + 1) % len(frames)
        root.after(50, update, index)

    root.after(0, update, 0)

    def close_popup():
        root.destroy()

    root.after(duration * 1000, close_popup)
    root.mainloop()

def recognize_face():
    try:
        image = face_recognition.load_image_file("known_face_fixed.jpg")
        known_encoding = face_recognition.face_encodings(image)[0]
    except Exception as e:
        speak(f"Error loading known face: {e}")
        return False

    cap = cv2.VideoCapture(0)
    start_time = time.time()
    authenticated = False

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding in face_encodings:
            match = face_recognition.compare_faces([known_encoding], encoding)
            if True in match:
                authenticated = True
                break

        if authenticated or time.time() - start_time > 10:
            break

    cap.release()
    cv2.destroyAllWindows()
    return authenticated

# Main
if __name__ == "__main__":
    speak("Starting face recognition...")

    result = recognize_face()

    if result:
        show_popup_gif("waveform.gif", duration=5)
        speak("Welcome back, Varshit.")
        # After this, your assistant can start listening for wake word etc.
    else:
        speak("Face not recognized. Access denied.")
        sys.exit()
