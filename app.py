    from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import os

app = Flask(__name__)

# -------- Generate Lyrics --------
def generate_lyrics(topic, style):
    return f"""
Style: {style}

Verse 1:
I’m feeling this vibe about {topic}
Everyday I rise, I can’t stop it
Dreams on my mind, I’m chasing the light
Everything I want, I go get it tonight

Hook:
{topic} on my mind, yeah I sing it loud
Standing so tall, make my people proud
No fear, no doubt, I’m breaking through
This is my moment, yeah I’m coming through
"""

# -------- Home Route --------
@app.route("/")
def home():
    return "Lyrics Generator App is Running!"

# -------- Generate Lyrics API --------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic", "life")
    style = data.get("style", "afrobeats")

    lyrics = generate_lyrics(topic, style)

    return jsonify({"lyrics": lyrics})

# -------- Text to Speech --------
@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = "speech.mp3"

    # limit text to avoid crash
    tts = gTTS(text=text[:500], lang='en')
    tts.save(filename)

    return send_file(filename, as_attachment=False)

# -------- Run App --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
