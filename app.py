from flask import Flask, request, jsonify, send_file, render_template
from gtts import gTTS
import uuid
import random
import os

app = Flask(__name__)

# -------- Generate Lyrics --------
def generate_lyrics(topic, style):
    verses = [
        f"I'm feeling this vibe about {topic}\nEveryday I rise, I can't stop it\nDreams on my mind, I'm chasing the light",
        f"{topic} in my heart, I gotta say\nRhythm in my soul, I pave the way\nStyle {style} making me sway"
    ]
    hook = f"{topic} on my mind, yeah I sing it loud\nStanding so tall, make my people proud"
    return "\n\n".join(random.sample(verses, 1) + [hook])

# -------- Home Page --------
@app.route("/")
def home():
    return render_template("index.html")

# -------- Generate + TTS --------
@app.route("/generate_song", methods=["POST"])
def generate_song():
    data = request.get_json()
    topic = data.get("topic", "life")
    style = data.get("style", "afrobeats")

    lyrics = generate_lyrics(topic, style)

    filename = f"speech_{uuid.uuid4().hex}.mp3"
    tts_audio = gTTS(text=lyrics, lang="en")
    tts_audio.save(filename)

    return jsonify({
        "lyrics": lyrics,
        "audio": f"/audio/{filename}"
    })

# -------- Serve Audio --------
@app.route("/audio/<filename>")
def audio(filename):
    return send_file(filename)

# -------- Run --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
