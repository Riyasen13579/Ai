# main.py
import pyttsx3
import pyjokes
import speech_recognition as sr
import os
import imdb
import wolframalpha
import subprocess as sp
from datetime import datetime
from decouple import config
from constant import random_text
from random import choice
from utils import find_my_ip, search_on_google, search_on_wikipedia, youtube, get_news
import requests


engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')
API_KEY = "c82f080c005596504785007a3ce670cc"

def get_temperature(city):
    api_key = "c82f080c005596504785007a3ce670cc"  # Your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == 200:
        temp = data["main"]["temp"]
        return temp
    else:
        return None
    
def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        print(f"Good morning {USER}")
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        print(f"Good afternoon {USER}")
        speak(f"Good afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        print(f"Good evening {USER}")
        speak(f"Good evening {USER}")
    print(f"I am {HOSTNAME}. How may i assist you Ma'am?.. ")
    speak(f"I am {HOSTNAME}. How may i assist you Ma'am?.. ")

    
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=6)  
    try:
        print("Recognizing....")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            print(choice(random_text))
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                print("Good night Ma'am,take care!")
                speak("Good night Ma'am,take care!")
            else:
                print("Have a good day Ma'am!")
                speak("Have a good day Ma'am!")
            exit()

    except Exception:
        print("Sorry I couldn't understand. Can you please repeat that?")
        speak("Sorry I couldn't understand. Can you please repeat that?")
        queri = 'None'
    return queri 



if __name__ == '__main__':
        greet_me()
        while True:

                query = take_command().lower()
                if "how are you" in query:
                    print("I am absolutely fine Ma'am. What about you..??")
                    speak("I am absolutely fine Ma'am. What about you")

                elif "i am also good" in query:
                    print("Good to hear that...Ma'am")
                    speak("Good to hear that...Ma'am")

                elif "Why your name is Noaah Cyrus??"in query:
                    print("NOAAH CYRUS stands for Neural Organic Assistant for Advanced Help Cognitive Yielding Responsive User System")
                    speak("NOAAH CYRUS stands for Neural Organic Assistant for Advanced Help Cognitive Yielding Responsive User System")

                elif "temperature" in query or "weather" in query:
                    print("Please tell me the city name to get the temperature.")
                    speak("Please tell me the city name to get the temperature.")
                    city = take_command().lower()
                    temp = get_temperature(city)
                    if temp is not None:
                        response = f"The current temperature in {city} is {temp} degrees Celsius."
                        print(response)
                        speak(response)
                    else:
                        response = "Sorry, I couldn't fetch the weather for that city."
                        print(response)
                        speak(response)

                elif "joke"in query:
                    print("Cracking a joke...Ma'am")
                    speak("Cracking a joke...Ma'am")
                    joke = pyjokes.get_joke()
                    print(joke)
                    speak(joke)

                elif "open command prompt" in query:
                    print("Opening command prompt")
                    speak("Opening command prompt")
                    os.system('start cmd')
                
                elif "open camera" in query:
                    print("Opening camera Ma'am")
                    speak("Opening camera Ma'am")
                    sp.run('start microsoft.windows.camera:', shell=True) 

                elif "open notepad" in query:
                    print("Opening Notepad for you Ma'am")
                    speak("Opening Notepad for you Ma'am")
                    notepad_path = "C:\\Windows\\notepad.exe"
                    os.startfile(notepad_path)

                elif "file practice" in query:
                    print("Opening file practice for you Ma'am")
                    speak("Opening file practice for you Ma'am")
                    file_explorer = "C:\\Users\\This PC\\Desktop\\practice"
                    os.startfile(file_explorer)
                
                
                elif 'ip address' in query:
                    ip_address = find_my_ip()
                    speak(
                        f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                    print(f'Your IP Address is {ip_address}')
                
                elif "open youtube" in query:
                    print("What do you want to play on youtube Ma'am?")
                    speak("What do you want to play on youtube Ma'am?")
                    video = take_command().lower()
                    youtube(video)

                elif "open google" in query:
                    print(f"What do you want to search on google {USER}")
                    speak(f"What do you want to search on google {USER}")
                    query = take_command().lower()
                    search_on_google(query)

                elif "wikipedia" in query:
                    print("what do you want to search on wikipedia Ma'am?")
                    speak("what do you want to search on wikipedia Ma'am?")
                    search = take_command().lower()
                    results = search_on_wikipedia(search)
                    print(f"According to wikipedia,{results}")
                    speak(f"According to wikipedia,{results}")
                    print("I have printed this already on terminal")
                    speak("I have printed this already on terminal")
                    


                elif "give me news" in query:
                    print(f"I am reading out the latest headline of today,Ma'am")
                    speak(f"I am reading out the latest headline of today,Ma'am")
                    speak(get_news())
                    print("I am printing it on screen Ma'am")
                    speak("I am printing it on screen Ma'am")
                    print(*get_news(), sep='\n')

                
                elif "movie" in query:
                    movies_db = imdb.IMDb()
                    print("Please tell me the movie name:")
                    speak("Please tell me the movie name:")
                    text = take_command()
                    movies = movies_db.search_movie(text)
                    print("searching for" + text)
                    speak("searching for" + text)
                    print("I found these")
                    speak("I found these")
                    for movie in movies:
                        title = movie["title"]
                        year = movie["year"]
                        print(f"{title}-{year}")
                        speak(f"{title}-{year}")
                        info = movie.getID()
                        movie_info = movies_db.get_movie(info)
                        rating = movie_info["rating"]
                        cast = movie_info["cast"]
                        actor = cast[0:5]
                        plot = movie_info.get('plot outline', 'plot summary not available')
                        print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                            f"The plot summary of movie is {plot}")
                        
                        speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                            f"The plot summary of movie is {plot}")

                        

                elif "calculate" in query:
                    app_id = "K9QWWH-P6Y42K9QYE"
                    client = wolframalpha.Client(app_id)
                    ind = query.lower().split().index("calculate")
                    text = query.split()[ind + 1:]
                    result = client.query(" ".join(text))
                    try:
                        ans = next(result.results).text
                        print("The answer is " + ans)
                        speak("The answer is " + ans)
                        
                    except StopIteration:
                        print("I couldn't find that . Please try again")
                        speak("I couldn't find that . Please try again")


                elif 'what is' in query or 'who is' in query or 'which is' in query:
                    app_id = "K9QWWH-P6Y42K9QYE"
                    client = wolframalpha.Client(app_id)
                    try:

                        ind = query.lower().index('what is') if 'what is' in query.lower() else \
                            query.lower().index('who is') if 'who is' in query.lower() else \
                                query.lower().index('which is') if 'which is' in query.lower() else None

                        if ind is not None:
                            text = query.split()[ind + 2:]
                            res = client.query(" ".join(text))
                            ans = next(res.results).text
                            print("The answer is " + ans)
                            speak("The answer is " + ans)
                            
                        else:
                            print("I couldn't find that. Please try again.")
                            speak("I couldn't find that. Please try again.")
                    except StopIteration:
                        print("I couldn't find that. Please try again.")
                        speak("I couldn't find that. Please try again.")
           