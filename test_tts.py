# test_tts.py
import pyttsx3

print("Attempting to initialize the TTS engine...")

try:
    engine = pyttsx3.init()
    print("Engine initialized successfully.")

    voices = engine.getProperty('voices')
    if not voices:
        print("WARNING: No voices found on this system.")
    else:
        print(f"Found {len(voices)} voices.")

    engine.say("If you can hear this, the text to speech engine is working.")
    print("Attempting to speak...")
    engine.runAndWait()
    print("Test complete.")

except Exception as e:
    print("\n--- TTS ENGINE FAILED ---")
    print(f"An error occurred: {e}")
    print("-------------------------\n")
    print("This is the root cause of the problem. Please share this full error message.")