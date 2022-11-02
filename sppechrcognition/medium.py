import speech_recognition
import pyaudio
recognizer = speech_recognition.Recognizer()
while True:
    try:
        with speech_recognition.Microphone()as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("listening")
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message = message.lower()
            print (message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()

