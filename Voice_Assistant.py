# import tkinter as tk
from logging import exception
from time import strftime
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia 
import webbrowser
import os
import random

Character = "Ankit"
myName = "Robo"


def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    
def wishMe():
    hour = datetime.datetime.now().hour
    if hour>=0 and hour<12:
        say(f"Good Morning! {Character}")
    elif hour>=12 and hour<18:
        say(f"Good Afternoon! {Character}")
    else:
        say(f"Good Evening! {Character}")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        print("Recognizing...")
        r.pause_threshold = 1
        audio = r.listen(source)  # Corrected: Now you are capturing audio
        try:
            query = r.recognize_google (audio, language='en-in')
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None
        
def open_app(app_name):
    apps = {
        "chrome":r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "vscode":r"C:\Program Files\Microsoft VS Code\Code.exe",
        "github":r''' 'C:\Program Files\Google\Chrome\Application\chrome_proxy.exe'  --profile-directory="Profile 3" --app-id=mjoklplbddabcmpepnokjaffbmgbkkgg''',
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "spotify": r"C:\Users\ankit\AppData\Roaming\Spotify\Spotify.exe",
    }
    app_path = apps.get(app_name.lower())
    if app_path:
        os.startfile(app_path)
    else:
        print(f"Sorry, I couldn't find {app_name}. Try another name.")
        
def execute_command(query):
    """Executes the command received from the user."""
    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.org",
        "google": "https://www.google.com"
    }
    query = query.lower().strip()  # Convert to lowercase and remove extra spaces

    for site, url in sites.items():
        if f"open {site}" in query:
            say(f"Opening {site}.")
            webbrowser.open(url)
            return True
    # todo : add a feature for play specific song
    if "play music" in query:
        say("Playing your music.")
        # musicpath = r"C:\Users\ankit\OneDrive\Music\Finding Her - Kushagra 320 Kbps.mp3"
        music_dir = "C:\\Users\\ankit\\OneDrive\\Music"
        songs = os.listdir(music_dir)
            # say(f"Playing {songs[0]}")
        os.startfile(os.path.join(music_dir, songs[random.randint(0, len(songs)-1)]))
        # os.startfile(musicpath)
        return True

    if "the time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")  # This shows hour, minute, and AM/PM
        say(f"Sir, the time is {current_time}")
        return True

    if "open app" in query:
        say("Which app do you want to open?")
        app_name = takecommand()
        if app_name:
            open_app(app_name)
        return True
    return False  # No command was executed
        
if __name__ == "__main__":
    wishMe()
    say(f"Hello, I am {myName} your voice assistant. How can I help you?")
    while True:
        query = takecommand()

        # Skip loop if nothing was understood
        if query is None:
            continue
        
        query = query.lower()

        # exit command
        if "exit" in query or "quit" in query:
            say("Goodbye, see you soon!")
            break

        if "wikipedia" in query:
            try:
                query = query.replace("wikipedia", "")
                say("Searching Wikipedia...")
                result = wikipedia.summary(query, sentences=2)
                say("According to Wikipedia")
                print(result)
                say(result)
            except Exception:
                say("Sorry, I couldn't fetch results from Wikipedia.")
            continue  # move to next loop

        # normal execution
        executed = execute_command(query)

        # if no command matched, search google
        if not executed:
            say("I am searching it on Google")
            search = 'https://www.google.com/search?q=' + query
            webbrowser.open(search)