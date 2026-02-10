import json
import os
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from fpdf import FPDF
import tempfile

app = Flask(__name__)

STATS_FILE = "stats.json"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def load_stats():
    if not os.path.exists(STATS_FILE):
        return {
            "visits": 0,
            "lyrics_generated": 0,
            "unique_visitors": 0,
            "daily_stats": {},
            "visitor_ips": [],
            "visitor_countries": {},
            "last_visit": None
        }

    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "visits": 0,
            "lyrics_generated": 0,
            "unique_visitors": 0,
            "daily_stats": {},
            "visitor_ips": [],
            "visitor_countries": {},
            "last_visit": None
        }


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)


def get_client_ip():
    # Render sometimes uses proxy headers
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr


def get_country_from_ip(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == "success":
            return data.get("country", "Unknown")
        return "Unknown"
    except:
        return "Unknown"


def update_daily_stats(stats, action_type):
    today = datetime.now().strftime("%Y-%m-%d")

    if today not in stats["daily_stats"]:
        stats["daily_stats"][today] = {
            "visits": 0,
            "lyrics_generated": 0
        }

    stats["daily_stats"][today][action_type] += 1


@app.route("/")
def home():
    stats = load_stats()

    # Count visit
    stats["visits"] += 1
    update_daily_stats(stats, "visits")

    # Track IP + unique visitors
    ip = get_client_ip()
    if ip not in stats["visitor_ips"]:
        stats["visitor_ips"].append(ip)
        stats["unique_visitors"] += 1

        # Track country
        country = get_country_from_ip(ip)
        if country not in stats["visitor_countries"]:
            stats["visitor_countries"][country] = 0
        stats["visitor_countries"][country] += 1

    # Save last visit time
    stats["last_visit"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_stats(stats)

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    mood = request.form.get("mood")
    artist = request.form.get("artist")
    topic = request.form.get("topic")

    if not mood or not artist or not topic:
        return jsonify({"lyrics": "Please fill all fields."})

    if not GROQ_API_KEY:
        return jsonify({"lyrics": "Error: GROQ_API_KEY not found. Add it in Render environment variables."})

    prompt = f"""
Write a very long Afrobeats song lyrics in the style of {artist}.
Mood: {mood}
Topic: {topic}

Requirements:
- Must be very long (at least 4 verses)
- Must include a strong catchy chorus (repeat chorus twice)
- Include intro, verse 1, chorus, verse 2, chorus, bridge, verse 3, chorus, outro
- Use Nigerian slang and smooth rhymes
- Make it sound like a real hit song
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a professional Afrobeats songwriter."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 1500
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" not in result:
            return jsonify({"lyrics": f"Error: {result}"})

        lyrics = result["choices"][0]["message"]["content"]

        # Count generated lyrics
        stats = load_stats()
        stats["lyrics_generated"] += 1
        update_daily_stats(stats, "lyrics_generated")
        save_stats(stats)

        return jsonify({"lyrics": lyrics})

    except Exception as e:
        return jsonify({"lyrics": f"Error: {str(e)}"})


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    lyrics = request.form.get("lyrics")

    if not lyrics:
        return "No lyrics provided", 400

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in lyrics.split("\n"):
        pdf.multi_cell(0, 10, line)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)

    return send_file(temp_file.name, as_attachment=True, download_name="lyrics.pdf")


@app.route("/stats")
def stats():
    return jsonify(load_stats())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
