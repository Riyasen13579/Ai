from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, pyjokes, wolframalpha, wikipedia, requests
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)

# ── Config ────────────────────────────────────────────────────
WEATHER_KEY = os.environ.get("WEATHER_KEY", "c82f080c005596504785007a3ce670cc")
WOLFRAM_ID  = os.environ.get("WOLFRAM_ID",  "K9QWWH-P6Y42K9QYE")
ASSISTANT   = "NOAH CYRUS"

# ── Helpers ───────────────────────────────────────────────────
def get_weather(city):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_KEY}&units=metric", timeout=6).json()
        if r.get("cod") == 200:
            return (r["main"]["temp"], r["main"]["feels_like"],
                    r["main"]["humidity"], r["weather"][0]["description"])
    except: pass
    return None, None, None, None

def wiki(q):
    try: return wikipedia.summary(q, sentences=3)
    except wikipedia.DisambiguationError as e:
        try: return wikipedia.summary(e.options[0], sentences=3)
        except: return "Multiple results — please be more specific."
    except: return "Not found on Wikipedia."

def wolfram(q):
    try: return next(wolframalpha.Client(WOLFRAM_ID).query(q).results).text
    except: return None

# ══════════════════════════════════════════════════════════════
#  COMMAND PROCESSOR  (web-safe — no local PC commands)
# ══════════════════════════════════════════════════════════════
def process(query: str) -> dict:
    """
    Returns dict:
      response : str   — text reply shown in chat
      action   : str   — optional frontend action
      url      : str   — optional URL for action
    """
    q = query.lower().strip()
    if not q:
        return R("Please ask me something.")

    print(f"[NOAH CYRUS] {q}")

    # ── Greetings ─────────────────────────────────────────────
    if any(w in q for w in ["hello","hi ","hey","namaste"]):
        h   = datetime.now().hour
        tod = "morning" if h<12 else "afternoon" if h<17 else "evening"
        return R(f"Good {tod}! I'm {ASSISTANT}, your personal intelligence system. How can I help you?")

    if "how are you" in q or "kaisa hai" in q:
        return R("I'm running at full capacity and ready to assist! What can I do for you?")

    if "your name" in q or "who are you" in q:
        return R(f"I am {ASSISTANT} — Neural Organic Assistant for Advanced Help, "
                 f"Cognitive Yielding Responsive User System. Your personal AI assistant.")

    if "thank" in q or "shukriya" in q:
        return R("You're most welcome! Is there anything else I can help you with?")

    if "bye" in q or "goodbye" in q or "alvida" in q:
        return R("Goodbye! Have a productive day. I'll be here when you need me. 👋")

    # ── Time / Date ───────────────────────────────────────────
    if "time" in q and "weather" not in q:
        return R(f"🕐 The current time is {datetime.now().strftime('%I:%M %p')} (server time).")

    if "date" in q or "today" in q or "aaj" in q:
        return R(f"📅 Today is {datetime.now().strftime('%A, %d %B %Y')}.")

    # ── Weather ───────────────────────────────────────────────
    if "weather" in q or "temperature" in q or "mausam" in q:
        city = q
        for w in ["weather","temperature","mausam","what is the","what's the",
                  " in "," of "," for ","today","current","now","aaj"]:
            city = city.replace(w, "")
        city = city.strip() or "Delhi"
        t, f, h, d = get_weather(city)
        if t:
            return R(f"🌤 Weather in {city.title()}:\n"
                     f"• Condition: {d.capitalize()}\n"
                     f"• Temperature: {t}°C (feels like {f}°C)\n"
                     f"• Humidity: {h}%")
        return R(f"Sorry, couldn't fetch weather for '{city}'. Please check the city name.")

    # ── Joke ──────────────────────────────────────────────────
    if "joke" in q or "funny" in q:
        return R(f"😄 {pyjokes.get_joke()}")

    # ── Open YouTube (web action) ─────────────────────────────
    if "youtube" in q:
        s = q.replace("open youtube","").replace("play on youtube","").replace("youtube","").strip()
        url = f"https://www.youtube.com/results?search_query={s}" if s else "https://www.youtube.com"
        return R(f"▶ Opening YouTube{' for: ' + s if s else ''}...", action="open", url=url)

    # ── Open Google (web action) ──────────────────────────────
    if "google" in q or ("search" in q and "wikipedia" not in q):
        s = (q.replace("open google","").replace("search on google","")
              .replace("search for","").replace("google","").replace("search","").strip())
        url = f"https://www.google.com/search?q={s}" if s else "https://www.google.com"
        return R(f"🔍 {'Searching Google for: ' + s if s else 'Opening Google'}...",
                 action="open", url=url)

    # ── Open News ─────────────────────────────────────────────
    if "news" in q or "khabar" in q:
        return R("📰 Opening latest news...", action="open", url="https://news.google.com")

    # ── Wikipedia ─────────────────────────────────────────────
    if "wikipedia" in q:
        s = q.replace("wikipedia","").replace("search on","").replace("search","").strip()
        if not s: return R("What should I look up on Wikipedia?")
        result = wiki(s)
        return R(f"📖 Wikipedia — {s.title()}:\n\n{result}")

    # ── IP address ────────────────────────────────────────────
    if "ip address" in q or "my ip" in q:
        try: ip = requests.get("https://api.ipify.org", timeout=5).text
        except: ip = "Unavailable"
        return R(f"🌐 Your public IP Address is: {ip}")

    # ── Calculate ─────────────────────────────────────────────
    if "calculate" in q or "compute" in q or "solve" in q or "math" in q:
        words = q.split()
        for kw in ["calculate","compute","solve","math"]:
            if kw in words:
                expr = " ".join(words[words.index(kw)+1:])
                ans  = wolfram(expr)
                if ans: return R(f"🧮 The answer is: {ans}")
        return R("I couldn't calculate that. Please rephrase, e.g. 'calculate 25 times 48'.")

    # ── What / Who / Which ────────────────────────────────────
    for kw in ["what is ","who is ","which is ","what are ","who are ","what was ","who was "]:
        if kw in q:
            subject = q.split(kw, 1)[-1].strip()
            if subject:
                ans = wolfram(subject)
                if ans: return R(f"💡 {ans}")
                result = wiki(subject)
                return R(f"📖 {result}")

    # ── Fallback: open Google search ──────────────────────────
    url = f"https://www.google.com/search?q={query}"
    return R(f"🔍 Let me search that for you...", action="open", url=url)


def R(text, action=None, url=None):
    return {"response": text, "action": action, "url": url}

# ══════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════
@app.route("/")
def root():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/command", methods=["POST"])
def command():
    try:
        data  = request.get_json(force=True, silent=True) or {}
        query = data.get("query", "").strip()
        if not query:
            return jsonify({"response": "Please say or type something.", "action": None, "url": None}), 400
        result = process(query)
        return jsonify(result)
    except Exception as e:
        print(f"[ERR] {e}")
        return jsonify({"response": f"Error: {e}", "action": None, "url": None}), 500

@app.route("/greet")
def greet():
    h = datetime.now().hour
    if   6 <= h < 12: g = f"Good morning! I am {ASSISTANT}. How can I help you today?"
    elif 12 <= h < 17: g = f"Good afternoon! {ASSISTANT} is online and ready."
    elif 17 <= h < 21: g = f"Good evening! {ASSISTANT} here — how can I help?"
    else:              g = f"Hello! {ASSISTANT} is active. What can I do for you?"
    return jsonify({"greeting": g})

@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "name": ASSISTANT})

# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n  {ASSISTANT} — Web Version")
    print(f"  Running on http://0.0.0.0:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
