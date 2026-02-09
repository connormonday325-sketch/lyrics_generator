from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not found. Add it on Render Environment Variables.")

client = OpenAI(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    mood = request.form.get("mood")
    artist = request.form.get("artist")
    topic = request.form.get("topic")

    prompt = f"""
Write a long song lyrics with this style:

Mood: {mood}
Artist style: {artist}
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

Make the chorus catchy and repeated.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional songwriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=900
        )

        lyrics = response.choices[0].message.content
        return jsonify({"lyrics": lyrics})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
