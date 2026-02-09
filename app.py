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
        "model": "llama3-8b-8192",
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
