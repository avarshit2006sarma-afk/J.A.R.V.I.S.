# ==============================
# JARVIS AI - PART 1 (CORE)
# ==============================

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import json
import random
import threading
import time

# ==============================
# INITIALIZATION
# ==============================

engine = pyttsx3.init()
engine.setProperty('rate', 175)
voices = engine.getProperty('voices')

# Try male voice
try:
    engine.setProperty('voice', voices[0].id)
except:
    pass

recognizer = sr.Recognizer()

MEMORY_FILE = "memory.json"

# ==============================
# MEMORY SYSTEM
# ==============================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

memory = load_memory()

# ==============================
# SPEECH SYSTEM
# ==============================

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def speak_async(text):
    threading.Thread(target=speak, args=(text,), daemon=True).start()

# ==============================
# LISTENING SYSTEM
# ==============================

def listen(timeout=5):
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=timeout)
        except:
            return ""

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"YOU: {command}")
        return command
    except:
        return ""

# ==============================
# WAKE WORD DETECTION
# ==============================

WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis"]

def wait_for_wake_word():
    while True:
        cmd = listen(timeout=3)
        for word in WAKE_WORDS:
            if word in cmd:
                return True

# ==============================
# UTILITIES
# ==============================

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%A, %d %B %Y")

def random_response(options):
    return random.choice(options)

# ==============================
# GREETING SYSTEM
# ==============================

def greet_user():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good morning.")
    elif hour < 18:
        speak("Good afternoon.")
    else:
        speak("Good evening.")

    speak("System initialized. Awaiting your command.")

# ==============================
# SMALL TALK SYSTEM
# ==============================

def small_talk(command):

    if "how are you" in command:
        speak(random_response([
            "Operating at full capacity.",
            "All systems are running perfectly.",
            "Better now that you're here."
        ]))
        return True

    if "who are you" in command:
        speak("I am Jarvis. Your personal AI assistant.")
        return True

    if "your creator" in command:
        speak("I was created by Varshit. Obviously.")
        return True

    return False

# ==============================
# MEMORY COMMANDS
# ==============================

def memory_commands(command):

    if "remember that" in command:
        data = command.replace("remember that", "").strip()
        memory["note"] = data
        save_memory(memory)
        speak("Noted.")
        return True

    if "what do you remember" in command:
        speak(memory.get("note", "I don't remember anything yet."))
        return True

    return False
# ==============================
# JARVIS AI - PART 2 (AUTH + GUI)
# ==============================

import cv2
import time
import threading

try:
    import face_recognition
except:
    face_recognition = None

try:
    import tkinter as tk
    from PIL import Image, ImageTk
except:
    tk = None

# ==============================
# FACE RECOGNITION SYSTEM
# ==============================

def recognize_face():
    if face_recognition is None:
        speak("Face recognition module not available. Skipping authentication.")
        return True

    try:
        image = face_recognition.load_image_file("known_face_fixed.jpg")
        known_encoding = face_recognition.face_encodings(image)[0]
    except Exception as e:
        speak("Error loading face data.")
        return False

    cap = cv2.VideoCapture(0)
    start_time = time.time()
    authenticated = False

    speak("Scanning face. Please look at the camera.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)

        for encoding in encodings:
            match = face_recognition.compare_faces([known_encoding], encoding)
            if True in match:
                authenticated = True
                break

        if authenticated:
            break

        if time.time() - start_time > 10:
            break

    cap.release()
    cv2.destroyAllWindows()

    return authenticated

# ==============================
# GUI WAVEFORM SYSTEM
# ==============================

def show_waveform(duration=4):
    if tk is None:
        return

    def run_gui():
        root = tk.Tk()
        root.overrideredirect(True)
        root.wm_attributes("-topmost", True)
        root.config(bg="black")
        root.wm_attributes("-transparentcolor", "black")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        try:
            img = Image.open("waveform.gif")
            frames = []

            while True:
                frame = img.copy()
                frames.append(ImageTk.PhotoImage(frame.convert("RGBA")))
                img.seek(len(frames))
        except:
            root.destroy()
            return

        label = tk.Label(root, bg="black")
        label.pack()

        x = (screen_width - img.width) // 2
        y = screen_height - img.height - 80
        root.geometry(f"{img.width}x{img.height}+{x}+{y}")

        def update(index):
            frame = frames[index]
            label.configure(image=frame)
            index = (index + 1) % len(frames)
            root.after(50, update, index)

        root.after(0, update, 0)
        root.after(duration * 1000, root.destroy)
        root.mainloop()

    threading.Thread(target=run_gui, daemon=True).start()

# ==============================
# LISTENING VISUAL FEEDBACK
# ==============================

def listening_animation():
    # Trigger waveform while listening
    show_waveform(duration=3)

# ==============================
# BACKGROUND SYSTEM THREADS
# ==============================

def background_status_loop():
    while True:
        time.sleep(60)

        # Optional background updates
        # Example: auto-save memory
        save_memory(memory)

def start_background_threads():
    threading.Thread(target=background_status_loop, daemon=True).start()

# ==============================
# STARTUP SEQUENCE
# ==============================

def startup_sequence():

    speak("Initializing security protocols.")

    result = recognize_face()

    if result:
        show_waveform(duration=3)
        speak("Authentication successful.")
        speak("Welcome back, Varshit.")
    else:
        speak("Face not recognized.")
        speak("Access denied.")
        exit()

    # Start background systems
    start_background_threads()

# ==============================
# ENHANCED LISTEN (WITH UI)
# ==============================

def listen_with_ui():
    listening_animation()
    return listen()

# ==============================
# IDLE ANIMATION (OPTIONAL)
# ==============================

def idle_effect():
    # Subtle periodic UI pulse (optional)
    while True:
        time.sleep(120)
        show_waveform(duration=2)

def start_idle_effect():
    threading.Thread(target=idle_effect, daemon=True).start()
# ==============================
# JARVIS AI - PART 3 (COMMAND CORE)
# ==============================

import subprocess
import urllib.parse

# ==============================
# APP PATHS (EDIT IF NEEDED)
# ==============================

APP_PATHS = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vscode": "C:\\Users\\Public\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe"
}

# ==============================
# SYSTEM UTILITIES
# ==============================

def open_application(app_name):
    path = APP_PATHS.get(app_name)

    if path:
        try:
            subprocess.Popen(path)
            speak(f"Opening {app_name}")
        except:
            speak(f"Failed to open {app_name}")
    else:
        speak(f"I don't know how to open {app_name}")

def close_application(app_name):
    os.system(f"taskkill /f /im {app_name}.exe")

def set_volume(level):
    try:
        os.system(f"nircmd.exe setsysvolume {level}")
        speak(f"Volume set to {level}")
    except:
        speak("Volume control failed")

def mute_volume():
    os.system("nircmd.exe mutesysvolume 1")

def unmute_volume():
    os.system("nircmd.exe mutesysvolume 0")

# ==============================
# WEB + SEARCH SYSTEM
# ==============================

def google_search(query):
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    webbrowser.open(url)

def youtube_search(query):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    webbrowser.open(url)

def play_youtube(query):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    webbrowser.open(url)

# ==============================
# FILE SYSTEM COMMANDS
# ==============================

def create_file(name):
    try:
        with open(name, "w") as f:
            f.write("")
        speak(f"File {name} created")
    except:
        speak("Failed to create file")

def read_file(name):
    try:
        with open(name, "r") as f:
            content = f.read()
        speak(content[:500])  # limit speaking
    except:
        speak("Cannot read that file")

# ==============================
# ADVANCED COMMAND PARSER
# ==============================

def handle_advanced_commands(command):

    # ==========================
    # APP CONTROL
    # ==========================
    if "open chrome" in command:
        open_application("chrome")
        return True

    if "open vscode" in command:
        open_application("vscode")
        return True

    if "open notepad" in command:
        open_application("notepad")
        return True

    if "open calculator" in command:
        open_application("calculator")
        return True

    if "close chrome" in command:
        close_application("chrome")
        speak("Closing chrome")
        return True

    # ==========================
    # SYSTEM CONTROL
    # ==========================
    if "shutdown system" in command:
        speak("Shutting down system")
        os.system("shutdown /s /t 1")
        return True

    if "restart system" in command:
        speak("Restarting system")
        os.system("shutdown /r /t 1")
        return True

    if "lock system" in command:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return True

    if "mute" in command:
        mute_volume()
        return True

    if "unmute" in command:
        unmute_volume()
        return True

    if "volume" in command:
        try:
            level = int(''.join(filter(str.isdigit, command)))
            set_volume(level * 655)
            return True
        except:
            speak("Invalid volume level")

    # ==========================
    # SEARCH SYSTEM
    # ==========================
    if "search google for" in command:
        query = command.replace("search google for", "")
        google_search(query)
        speak(f"Searching Google for {query}")
        return True

    if "search youtube for" in command:
        query = command.replace("search youtube for", "")
        youtube_search(query)
        speak(f"Searching YouTube for {query}")
        return True

    if "play" in command:
        query = command.replace("play", "")
        play_youtube(query)
        speak(f"Playing {query}")
        return True

    # ==========================
    # FILE SYSTEM
    # ==========================
    if "create file" in command:
        name = command.replace("create file", "").strip()
        create_file(name)
        return True

    if "read file" in command:
        name = command.replace("read file", "").strip()
        read_file(name)
        return True

    # ==========================
    # DATE / TIME / INFO
    # ==========================
    if "date" in command:
        speak(get_date())
        return True

    if "time" in command:
        speak(get_time())
        return True

    if "battery" in command:
        speak("Battery status feature not implemented yet.")
        return True

    # ==========================
    # FUN / PERSONALITY
    # ==========================
    if "tell me a joke" in command:
        jokes = [
            "Why do programmers hate nature? Too many bugs.",
            "I would tell you a UDP joke, but you might not get it.",
            "Why did the computer show up at work late? It had a hard drive."
        ]
        speak(random.choice(jokes))
        return True

    if "motivate me" in command:
        speak("You didn't come this far to only come this far.")
        return True

    if "insult me" in command:
        speak("I'd insult you, but that would be a waste of my processing power.")
        return True

    # ==========================
    # FALLBACK
    # ==========================
    return False
# ==============================
# JARVIS AI - PART 4 (FINAL CORE)
# ==============================

import os

# ==============================
# LOAD ENV (API KEYS)
# ==============================

def load_env():
    try:
        with open("OpenAI.env.txt") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    except:
        pass

load_env()

# ==============================
# AI BRAIN (CHATGPT)
# ==============================

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except:
    client = None

def ask_ai(prompt):

    if client is None:
        return "AI module not configured."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a smart, slightly sarcastic AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return "Something went wrong with AI."

# ==============================
# MASTER COMMAND ROUTER
# ==============================

def process_command(command):

    if not command:
        return

    # Step 1: small talk
    if small_talk(command):
        return

    # Step 2: memory
    if memory_commands(command):
        return

    # Step 3: advanced system
    if handle_advanced_commands(command):
        return

    # Step 4: exit
    if "exit" in command or "shutdown jarvis" in command:
        speak("Shutting down systems. Goodbye.")
        exit()

    # Step 5: fallback to AI
    response = ask_ai(command)
    speak(response)

# ==============================
# MULTI-COMMAND HANDLING
# ==============================

def split_commands(command):
    separators = [" and ", " then ", ","]
    for sep in separators:
        if sep in command:
            return [c.strip() for c in command.split(sep)]
    return [command]

def process_multiple(command):
    commands = split_commands(command)

    for cmd in commands:
        process_command(cmd)

# ==============================
# RESPONSE PERSONALITY
# ==============================

def acknowledgment():
    return random.choice([
        "Yes?",
        "I'm listening.",
        "Go ahead.",
        "What do you need?",
        "At your service."
    ])

# ==============================
# MAIN LOOP
# ==============================

def run_jarvis():

    startup_sequence()  # from PART 2
    greet_user()        # from PART 1

    start_idle_effect() # background UI

    while True:

        # WAIT FOR WAKE WORD
        wait_for_wake_word()

        speak(acknowledgment())

        # LISTEN WITH UI
        command = listen_with_ui()

        if command:
            process_multiple(command)

# ==============================
# SAFE EXECUTION WRAPPER
# ==============================

def safe_run():
    try:
        run_jarvis()
    except KeyboardInterrupt:
        speak("Manual shutdown detected.")
    except Exception as e:
        print("ERROR:", e)
        speak("A critical error occurred.")

# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    safe_run()
# ==============================
# JARVIS EXTENDED FEATURES (BOOST TO 1K+)
# ==============================

import psutil
import random

# ==============================
# SYSTEM MONITORING
# ==============================

def get_cpu_usage():
    try:
        return psutil.cpu_percent(interval=1)
    except:
        return None

def get_ram_usage():
    try:
        return psutil.virtual_memory().percent
    except:
        return None

def system_status():
    cpu = get_cpu_usage()
    ram = get_ram_usage()

    if cpu is None:
        speak("System monitoring not available.")
        return

    speak(f"CPU usage is {cpu} percent.")
    speak(f"Memory usage is {ram} percent.")

# ==============================
# WEATHER SYSTEM (USING YOUR API)
# ==============================

import requests

def get_weather(city="Vijayawada"):
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        speak("Weather API not configured.")
        return

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()

        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]

        speak(f"It is {temp} degrees with {desc} in {city}")

    except:
        speak("Failed to fetch weather.")

# ==============================
# MUSIC CONTROL (BASIC)
# ==============================

def play_local_music():
    music_dir = os.path.expanduser("~/Music")

    try:
        songs = os.listdir(music_dir)
        song = random.choice(songs)
        os.startfile(os.path.join(music_dir, song))
        speak("Playing music.")
    except:
        speak("No music found.")

# ==============================
# SCREENSHOT SYSTEM
# ==============================

def take_screenshot():
    try:
        import pyautogui
        file_name = f"screenshot_{int(time.time())}.png"
        pyautogui.screenshot(file_name)
        speak("Screenshot taken.")
    except:
        speak("Screenshot failed.")

# ==============================
# NOTE TAKING SYSTEM
# ==============================

def take_note():
    speak("What should I write?")
    content = listen()

    if content:
        with open("notes.txt", "a") as f:
            f.write(content + "\n")

        speak("Note saved.")

# ==============================
# ALARM / TIMER SYSTEM
# ==============================

def set_timer(seconds):
    speak(f"Timer set for {seconds} seconds.")

    def timer_thread():
        time.sleep(seconds)
        speak("Time is up.")

    threading.Thread(target=timer_thread, daemon=True).start()

# ==============================
# ADVANCED PERSONALITY RESPONSES
# ==============================

def emotional_response(command):

    if "i am sad" in command:
        speak("That sucks. But you won't stay here forever.")
        return True

    if "i am happy" in command:
        speak("Good. Stay like that.")
        return True

    if "i am tired" in command:
        speak("Then rest. Even machines need cooldown.")
        return True

    return False

# ==============================
# EXTENDED COMMAND ROUTER
# ==============================

def extended_commands(command):

    # SYSTEM STATUS
    if "system status" in command:
        system_status()
        return True

    # WEATHER
    if "weather" in command:
        get_weather()
        return True

    # MUSIC
    if "play music" in command:
        play_local_music()
        return True

    # SCREENSHOT
    if "screenshot" in command:
        take_screenshot()
        return True

    # NOTES
    if "take note" in command:
        take_note()
        return True

    # TIMER
    if "set timer" in command:
        try:
            seconds = int(''.join(filter(str.isdigit, command)))
            set_timer(seconds)
            return True
        except:
            speak("Invalid timer value.")

    # EMOTIONAL RESPONSES
    if emotional_response(command):
        return True

    return False

# ==============================
# PATCH INTO MAIN ROUTER
# ==============================

# MODIFY your process_command() function like this:

"""
ADD THIS LINE inside process_command():

    if extended_commands(command):
        return
"""

# ==============================
# CONTEXT MEMORY (SMARTER AI)
# ==============================

conversation_history = []

def ask_ai_with_context(prompt):

    if client is None:
        return "AI unavailable."

    conversation_history.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history[-10:]  # last 10 messages
        )

        reply = response.choices[0].message.content

        conversation_history.append({"role": "assistant", "content": reply})

        return reply

    except:
        return "AI failed."

# ==============================
# SMART IDLE THINKING (OPTIONAL)
# ==============================

def idle_thoughts():
    thoughts = [
        "Systems stable.",
        "Awaiting commands.",
        "Monitoring environment.",
        "All processes running smoothly."
    ]

    while True:
        time.sleep(180)
        print("JARVIS (idle):", random.choice(thoughts))

def start_idle_thoughts():
    threading.Thread(target=idle_thoughts, daemon=True).start()