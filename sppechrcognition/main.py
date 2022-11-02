from email import message
from email.mime import audio
from http.client import responses
from mailbox import MaildirMessage
from pydoc import cli
from re import search
import re
from typing import Mapping
import webbrowser
from neuralintents import GenericAssistant
from numpy import true_divide
import speech_recognition
import pyttsx3 as tts
import sys
import random
import smtplib
import time
from paho.mqtt import client as mqtt_client
global hello
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'test'
password = 'test'


# connecting to the mqtt.
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
# publishing data to raspberrry pi


def publish(client):
    time.sleep(1)
    result = client.publish(topic, hello)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{hello}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


#client = connect_mqtt()

recognizer = speech_recognition.Recognizer()
speaker = tts.init()
voices = speaker.getProperty('voices')
speaker.setProperty('rate', 150)
speaker.setProperty('voice', voices[1].id)
todo_list = ["go shoping ", "clean room ", " record video"]


def create_note():
    global recognizer
    speaker.say("what do you want to write on to your note?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with speech_recognition.Microphone()as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                note = recognizer.recognize_google(audio)
                note = note.lower()
                speaker.say("chose a file name")
                speaker.runAndWait()
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"i succesffully createdd the note{filename}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say(" i did not under stand what you say please try again")
            speaker.runAndWait()


def add_todo():
    global recognizer
    speaker.say("what to do do you want to add")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                item = recognizer.recognize_google(audio)
                item = item.lower()
                todo_list.append(item)
                done = True
                speaker.say(f"i added {item} the item in the list")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("i did not understand pleadse try again")
            speaker.runAndWait


def show_todo():
    speaker.say("the items on your list are the following")
    for item in todo_list:
        speaker.say(item)
        speaker.runAndWait()


def coco():
    speaker.say("yes sir?")
    speaker.runAndWait()

def open_youtube():
    webbrowser.open("youtube.com")
    speaker.say("what you want to watch")
    speaker.runAndWait()

    # searching teachnique


"""def control_on():
    speaker.say("taking action on it")
    speaker.runAndWait()
    global hello
    hello = "lightson"
    publish(client)

def control_off():
    speaker.say("taking action on it")
    speaker.runAndWait()
    global hello
    hello = "lightsof"
    #publish(client)"""

def open_chrome():
    path = "C:/Program Files/Google\Chrome/Application/chrome.exe  %s"

    speaker.say("what you want to search")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                search = recognizer.recognize_google(audio)
                print = (search)
                webbrowser.get(path).open(search)
                done = True
                speaker.say(f"your search is ready sir")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("i did not understand pleadse try again")
            speaker.runAndWait
def openvisualstudio():
    path = ""
    speaker.say("which code file do you want to run")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with speech_recognition.Microphone()as mic:
                recognizer.adjust_for_ambient_noise(mic , duration = 0.2)
                audio = recognizer.listen(mic)
                search = recognizer.recognize_google(audio)
                print ("is this whta you want to search")
                speaker.say(f"opening viual studio code")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer= speech_recognition.Recognizer()
            speaker.say("i did not understand iehat you say ")
            speaker.runAndWait                  

def send_email():
    try:
        speaker.say("What should I say?")
        with speech_recognition.Microphone()as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            content = recognizer.recognize_google(audio)
            print(content)
            to = "pkatreja@gmail.com"
            speaker.say("sending the emai")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('ashishrohilla510@gmail.com', 'Ashish@321')
            server.sendmail('atrejachestha@gmail.com', to, content)
            server.close()
            speaker.say("email has been sent!")

    except Exception as e:
        print(e)
        speaker("Sorry my friend. I am not able to send this email")



Mapping = {
    "greetings": coco,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todo": show_todo,
    "exit": quit,
    "youtube": open_youtube,
    "chrome": open_chrome,
    "send_email": send_email,
    "visualstudio":openvisualstudio 
}
assistant = GenericAssistant('sppechrcognition/intents.json', intent_methods=Mapping)
assistant.train_model()
while True:
    try:
        with speech_recognition.Microphone()as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("listening")
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message = message.lower()
            assistant.request(message)
            print (message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
