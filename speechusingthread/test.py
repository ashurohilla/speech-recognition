import threading
import time
import speech_recognition as sr


class listen(threading.Thread):

    def __init__(self):

        self.playmusicobject = playmusic()
        self.r  = sr.Recognizer()

        self.listening()

    def listening(self):

        while 1:
            self.objectspeak = speak()
            self.apiobject = googleAPI()
            print("say something")
            time.sleep(0.5)
            with sr.Microphone() as source:
                # self.objectspeak.speaking("say something")
                self.audio = self.r.listen(source)


    def checkingAudio(self):
        time.sleep(0.5)

        try:
            a = str(self.r.recognize_google(self.audio))
            a = str(self.r.recognize_google(self.audio))
            print(a)

            if a in greetings:
                self.objectspeak.speaking("I am good how are you?")

            if a in music:
                print("playing music")
                self.playmusicobject.play()
            if a in stop:
                print("stopping")
                self.playmusicobject.b()

            if a in api:
                self.apiobject.distance()

            else:
                print("error")

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


class speak:
    THIS IS A PYTTS class




class googleAPI:
    GOOGLE DISTANCE API function calculates distance between 2 places

class playmusic:

    def play(self):
        self.objectspeak = speak()
        playsound.playsound('C:UserslegionDownloadsMusicmerimeri.mp3')

    def b(self):
        self.objectspeak.speaking("music stopped")

while 1:
    t1 = threading.Thread(target=listen())
    t2 = threading.Thread(target= listen.checkingAudio())
    t1.join()
    t2.join() 