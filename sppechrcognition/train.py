import pyttsx3
#A python library which will help us to convert text to speech. In short, it is a text-to-speech library.
#It works offline, and it is compatible with Python 2 as well the Python 3
import datetime
import speech_recognition as sr
import webbrowser
import os
import wikipedia
import smtplib
#Speech API developed by Microsoft.
#Helps in synthesis and recognition of voice
engine = pyttsx3.init()
engine.setProperty("rate", 178) #getting details of the current voice
#Voice id helps us to select different voices.
#voice[0].id = Male voice
#voice[1].id = Female voice

def speak(audio):
   engine.say(audio) 
   engine.runAndWait() #Without this command, speech will not be audible to us.
if __name__=="__main__" :
    speak("Hello! Hope you all are doing well.")
def wishme():
   hour = int(datetime.datetime.now().hour)
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("Welcome! Please tell me how may I help you")
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('atrejachestha@gmail.com', 'password')
    server.sendmail('atrejachestha@gmail.com', to, content)
    server.close()

def takeCommand():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.
    except Exception as e:
        # print(e)  use only if you want to print the error!
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower() #Converting user query into lower case
        # Logic for executing tasks based on query
        if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'play music' in query:
            music_dir = 'D:\\music'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Ma'am, the time is {strTime}")
        elif 'email to papa' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "pkatreja@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")
        