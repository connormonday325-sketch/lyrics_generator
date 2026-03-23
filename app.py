from flask import Flask, request, jsonify, send_file
from gtts import gTTS

app = Flask(__name__)

# -------- Generate Lyrics --------
def generate_lyrics(topic, style):
    return f"""
Style: {style}

Verse 1:
I'm feeling this vibe about {topic}
Everyday I rise, I can't stop it
Dreams on my mind, I'm chasing the light

Hook:
{topic} on my mind, yeah I sing it loud
Standing so tall, make my people proud
"""

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
        return jsonify({"error": "No text"}), 400

    tts = gTTS(text=text[:300], lang="en")
    tts.save("speech.mp3")

    return send_file("speech.mp3")

# -------- Run --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
