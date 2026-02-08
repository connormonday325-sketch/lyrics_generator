from flask import Flask, render_template, request, jsonify, send_file
import os
import openai
from fpdf import FPDF
import uuid

app = Flask(__name__)

# OpenAI API Key from Render Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    mood = data.get("mood", "Happy")
    artist = data.get("artist", "Wizkid")
    topic = data.get("topic", "Love")

    prompt = f"""
Write a full Nigerian Afrobeats song lyrics.
Mood: {mood}
Artist inspiration: {artist}
Topic: {topic}

Make it very long with:
- Intro
- Verse 1
- Chorus
- Verse 2
- Chorus
- Bridge
- Final Chorus
- Outro

Add some Pidgin English and catchy lines.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional songwriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.9
        )

        lyrics = response["choices"][0]["message"]["content"]

        return jsonify({"lyrics": lyrics})

    except Exception as e:
        return jsonify({"lyrics": f"Error generating lyrics: {str(e)}"})


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    data = request.get_json()
    lyrics = data.get("lyrics", "")

    if lyrics.strip() == "":
        return jsonify({"error": "No lyrics provided"}), 400

    # Create PDF file
    filename = f"lyrics_{uuid.uuid4().hex}.pdf"
    filepath = os.path.join("/tmp", filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in lyrics.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf.output(filepath)

    return send_file(filepath, as_attachment=True, download_name="AI_Lyrics.pdf")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
