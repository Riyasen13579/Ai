import requests
import wikipedia
import pywhatkit as kit
from decouple import config
import geocoder
import webbrowser

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
    webbrowser.open(f"https://www.youtube.com/results?search_query={video}")

def get_news():
    news_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=c82f080c005596504785007a3ce670cc"
    news = requests.get(news_url).json()

    articles = news["articles"]
    headlines = [article["title"] for article in articles[:5]]
    return headlines       



