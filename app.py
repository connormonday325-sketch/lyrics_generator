from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
from openai import OpenAI

app = Flask(__name__)

# OpenAI Client (New Version)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_lyrics(style, mood, artist):
    prompt = f"""
Write a long {style} song lyrics with intro, verse 1, pre-chorus, chorus, verse 2, bridge, final chorus and outro.
Mood: {mood}
Inspired by: {artist}
Make it catchy and modern.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional songwriter."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def home():
    lyrics = ""

    if request.method == "POST":
        style = request.form.get("style")
        mood = request.form.get("mood")
        artist = request.form.get("artist")

        lyrics = generate_ai_lyrics(style, mood, artist)

    return render_template("index.html", lyrics=lyrics)


@app.route("/download", methods=["POST"])
def download_pdf():
    lyrics = request.form.get("lyrics")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in lyrics.split("\n"):
        pdf.multi_cell(0, 10, line)

    file_path = "lyrics.pdf"
    pdf.output(file_path)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
