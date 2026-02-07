from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_lyrics():
    data = request.get_json()
    topic = data.get("topic", "")
    style = data.get("style", "")

    lyrics = f"""🎶 Lyrics Generated 🎶

Topic: {topic}
Style: {style}

Verse 1:
I was thinking 'bout you in the midnight rain,
Heart on fire but I feel the pain,
Dreams so loud, but they fade away,
Still I’m fighting just to stay.

Chorus:
Ohhh we rise, we fall,
But the music saves us all,
In the dark we shine,
Yeah your love is mine.

Verse 2:
City lights and a broken phone,
Still I walk this road alone,
But I hear your voice in every beat,
And it pulls me back to my feet.

Outro:
So I sing, so I fly,
Even when the tears don’t dry.
"""

    return jsonify({"lyrics": lyrics})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
