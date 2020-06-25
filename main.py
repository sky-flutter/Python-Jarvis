from weather import Weather
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import subprocess
from db import DbOperation
from slack_message import SlackMessage
from threading import Timer
import os

rhythmbox_path = "/usr/bin/rhythmbox"
recognizer = sr.Recognizer()
engine = pyttsx3.init()
rate = engine.getProperty("rate")
voice = engine.getProperty("voices")
engine.setProperty("voices",voice[11].id)
engine.setProperty("rate", 160)
slackMessage = SlackMessage()
db_op = DbOperation()
def speak(textData):
    engine.say(textData)
    engine.runAndWait()


def takeCommand():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        if audio is not None:
            try:
                userSaid = recognizer.recognize_google(audio, language="en-in")
                handleCommand(userSaid)
            except Exception as e:
                return None
    return userSaid


def handleCommand(command):
    userSaid = command.lower()
    if "wikipedia" in userSaid:
        speak("Searching on wikipedia")
        summary = wikipedia.summary(userSaid.replace("wikipedia", ""), sentences=2)
        speak(summary)
    elif "google" in userSaid:
        speak("Opening google")
        webbrowser.open("http://www.google.com")
    elif "youtube" in userSaid:
        speak("Opening youtube")
        webbrowser.open("http://www.youtube.com")
    elif "play song" in userSaid:
        speak("Playing music")
        filename = "/home/aakash/Music/AajRoLenDe.mp3"
        subprocess.call([rhythmbox_path, filename])
    elif "open visual" in userSaid:
        speak("Opening a visual studio code")
        os.system("code .")
    elif "weather" in userSaid:
        speak("Getting current weather...")
        weather = Weather()
        result = weather.getLocationKey()
        speak(result)
    elif "message" in userSaid:
        speak("Whom do you want to send message?")
        userName = takeCommand()
        while userName is None:
            speak("Please say that again")
            userName = takeCommand()
        speak("Searching users in slack")
        user_id = check_user(userName)
        speak("What message do you want to send?")
        message = takeCommand()
        while message is None:
            speak("Please say that again")
            message = takeCommand()
        speak("Sending message")
        ack = slackMessage.sendMessage(user_id,message)
        speak(ack)
    else:
        print(userSaid)

def check_user(user):
    user_id = db_op.get_user_id(user)
    while user_id is None:
        speak("Could not find user. Please say that again")
        userName = takeCommand()
        check_user(userName)
    print(user_id)
    return user_id

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")

    speak("How may I help you.")





if __name__ == "__main__":
    wishMe()
    while True:
        if takeCommand() is None:
            speak("Please say that again")
