from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
import os
from fpdf import FPDF
import tempfile

app = Flask(__name__)

# OpenAI client (Reads from Render environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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

    prompt = f"""
Write a LONG song lyrics in the style of {artist}.
Mood: {mood}
Topic: {topic}

Structure:
- Intro (short)
- Verse 1 (long)
- Chorus (catchy and repeatable)
- Verse 2 (long)
- Chorus (repeat again)
- Bridge (short emotional part)
- Final Chorus (strong ending)

Make it sound modern and musical with rhyme.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional songwriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            temperature=0.9
        )

        lyrics = response.choices[0].message.content

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
    app.run(host="0.0.0.0", port=10000)
