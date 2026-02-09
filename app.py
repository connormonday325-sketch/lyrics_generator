from flask import Flask, render_template, request, jsonify, send_file
import os
import requests
from fpdf import FPDF
import tempfile

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    mood = request.form.get("mood")
    artist = request.form.get("artist")
    topic = request.form.get("topic")

    if not mood or not artist or not topic:
        return jsonify({"error": "Please fill all fields"}), 400

    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY is missing. Add it on Render Environment Variables."}), 500

    prompt = f"""
Write a LONG song lyrics in the style of {artist}.
Mood: {mood}
Topic: {topic}

Structure:
- Intro
- Verse 1 (long)
- Chorus (catchy and repeatable)
- Verse 2 (long)
- Chorus (repeat)
- Bridge
- Final Chorus (strong)
- Outro

Make it sound modern, musical and emotional.
Add good rhymes.
Make the chorus very catchy.
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a professional songwriter. Write hit song lyrics."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 900
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "error" in result:
            return jsonify({"error": str(result["error"])}), 500

        lyrics = result["choices"][0]["message"]["content"]

        return jsonify({"lyrics": lyrics})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    lyrics = request.form.get("lyrics")

    if not lyrics:
        return jsonify({"error": "No lyrics to download"}), 400

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in lyrics.split("\n"):
        pdf.multi_cell(0, 8, line)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)

    return send_file(temp_file.name, as_attachment=True, download_name="lyrics.pdf")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
