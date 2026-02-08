from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# Example lyrics database (Random Mode)
random_lyrics_list = [
    "I'm chasing dreams in the night, never gonna stop.",
    "Money on my mind, yeah I'm rising to the top.",
    "Heart full of pain but I still keep moving strong.",
    "I came from nothing, now I'm writing my own song.",
    "Street lights shining, but my vision is brighter.",
    "I was down before, now I'm climbing higher."
]

# AI Lyrics Generator (Smart Mode)
def generate_ai_lyrics(style, mood, artist):
    return f"""[VERSE 1]
In the {mood.lower()} nights, I feel the vibe,
Living like {artist}, yeah I survive.
This {style.lower()} flow, it’s deep in my soul,
I'm chasing my dreams, I’m taking control.

[CHORUS]
I won't fall down, I won't lose my way,
Every single night, I'm here to stay.
Life moves fast, but I'm feeling alive,
In this {style.lower()} sound, I will survive.

[VERSE 2]
I came too far, I won't go back,
All my pain turned into a track.
{artist} inspired, I’m breaking the rules,
I'm making my moves, I'm playing it cool.

[BRIDGE]
Talking about street life, I never fold,
My story is real, my heart is gold.

[FINAL CHORUS]
Money coming fast, I'm feeling alive,
Money coming fast, I'm feeling alive.

[OUTRO]
This is my life, my life.
"""

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    mode = request.form.get("mode")
    style = request.form.get("style")
    mood = request.form.get("mood")
    artist = request.form.get("artist")

    if mode == "random":
        lyrics = random.choice(random_lyrics_list)
        lyrics = f"[RANDOM LYRICS]\n{lyrics}"
    else:
        lyrics = generate_ai_lyrics(style, mood, artist)

    return jsonify({"lyrics": lyrics})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
