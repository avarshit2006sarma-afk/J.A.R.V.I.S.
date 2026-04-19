import speech_recognition as sr

r = sr.Recognizer()
r.energy_threshold = 300  # Make it more sensitive

with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source, timeout=5, phrase_time_limit=5)
    print("Got audio!")

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
