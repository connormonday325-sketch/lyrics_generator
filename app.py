import os
import requests
import tempfile
import psycopg2
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file

from fpdf import FPDF

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")


# -------------------------
# DATABASE FUNCTIONS
# -------------------------
def get_db_connection():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL not found. Add it in Render Environment Variables.")

    return psycopg2.connect(DATABASE_URL)


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # table to store counters
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id SERIAL PRIMARY KEY,
            visits INTEGER DEFAULT 0,
            lyrics_generated INTEGER DEFAULT 0,
            pdf_downloads INTEGER DEFAULT 0
        );
    """)

    # table to store history logs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id SERIAL PRIMARY KEY,
            action TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
        );
    """)

    # ensure stats table has one row
    cur.execute("SELECT COUNT(*) FROM stats;")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("INSERT INTO stats (visits, lyrics_generated, pdf_downloads) VALUES (0, 0, 0);")

    conn.commit()
    cur.close()
    conn.close()


def log_action(action):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO history (action, timestamp) VALUES (%s, %s);",
        (action, datetime.now())
    )

    conn.commit()
    cur.close()
    conn.close()


def increment_stat(stat_name):
    conn = get_db_connection()
    cur = conn.cursor()

    if stat_name == "visits":
        cur.execute("UPDATE stats SET visits = visits + 1 WHERE id = 1;")
        log_action("visit")

    elif stat_name == "lyrics_generated":
        cur.execute("UPDATE stats SET lyrics_generated = lyrics_generated + 1 WHERE id = 1;")
        log_action("lyrics_generated")

    elif stat_name == "pdf_downloads":
        cur.execute("UPDATE stats SET pdf_downloads = pdf_downloads + 1 WHERE id = 1;")
        log_action("pdf_download")

    conn.commit()
    cur.close()
    conn.close()


def get_stats():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT visits, lyrics_generated, pdf_downloads FROM stats WHERE id = 1;")
    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "visits": row[0],
        "lyrics_generated": row[1],
        "pdf_downloads": row[2]
    }


def get_history(limit=50):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT action, timestamp FROM history ORDER BY timestamp DESC LIMIT %s;", (limit,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"action": r[0], "timestamp": str(r[1])} for r in rows]


# -------------------------
# ROUTES
# -------------------------
@app.route("/")
def home():
    increment_stat("visits")
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

        # increment counter
        increment_stat("lyrics_generated")

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

    # increment counter
    increment_stat("pdf_downloads")

    return send_file(temp_file.name, as_attachment=True, download_name="lyrics.pdf")


# -------------------------
# STATS ENDPOINTS
# -------------------------
@app.route("/stats", methods=["GET"])
def stats():
    return jsonify(get_stats())


@app.route("/history", methods=["GET"])
def history():
    limit = request.args.get("limit", 50)
    return jsonify(get_history(int(limit)))


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
