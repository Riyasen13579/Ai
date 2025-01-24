import requests
import wikipedia
import pywhatkit as kit
from decouple import config
import geocoder

def get_location():
    g = geocoder.ip('me')  # Get location based on IP address
    city = g.city  # City name
    return city

def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def search_on_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)

def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=india&category=business&apiKey=1a6cb749df2042b7a59d8036e5ab77bd").json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]        



