from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import uuid

app = Flask(__name__)

# -------- Generate Lyrics --------
import random
def generate_lyrics(topic, style):
    verses = [
        f"I'm feeling this vibe about {topic}\nEveryday I rise, I can't stop it\nDreams on my mind, I'm chasing the light",
        f"{topic} in my heart, I gotta say\nRhythm in my soul, I pave the way\nStyle {style} making me sway"
    ]
    hook = f"{topic} on my mind, yeah I sing it loud\nStanding so tall, make my people proud"
    return "\n\n".join(random.sample(verses, 1) + [hook])

# -------- Home Route --------
@app.route("/")
def home():
    return "App is running!"

# -------- Generate Lyrics --------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic", "life")
    style = data.get("style", "afrobeats")
    lyrics = generate_lyrics(topic, style)
    return jsonify({"lyrics": lyrics})

# -------- Text to Speech --------
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = f"speech_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    return send_file(filename, as_attachment=True)

# -------- Run --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
