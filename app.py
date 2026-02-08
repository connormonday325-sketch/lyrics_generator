from flask import Flask, render_template, request

app = Flask(__name__)

def generate_ai_lyrics(style, mood, artist):
    return f"""
[INTRO]
Yeah yeah...
This one na {style} vibe...
Feeling {mood} tonight...
Inspired by {artist}...

[VERSE 1]
I dey hustle everyday, no time to sleep
I dey pray make blessings follow me deep
Life no easy but I stand my ground
Everyday I rise, I no dey fall down

I remember those days when nobody see
Now my name for the air, everywhere I be
I pray to God make my story never end
I go rise to the top, that's my main trend

[CHORUS]
Money coming fast, I’m feeling alive
Everyday I grind, I dey chase my vibe
No more suffering, I don’t want to cry
I want to live big, I want to touch sky

Money coming fast, I’m feeling alive
Blessings from above, I dey thank my life
All my enemies, dem dey watch my shine
But I no go fall, I go always rise

[VERSE 2]
See the pain for my eyes, but I still dey smile
I don waka long road, I don travel miles
From the ghetto to the stage, I dey break the chain
Turn my struggles into power, turn my tears to gain

Mama tell me say, "my son no give up"
Even if the world dey hard, you go still stand up
Now I dey chase my dream like say na race
And I no go stop until I reach my place

[BRIDGE]
Oh oh oh...
I dey pray for better days
Oh oh oh...
Make the blessings come my way

[CHORUS]
Money coming fast, I’m feeling alive
Everyday I grind, I dey chase my vibe
No more suffering, I don’t want to cry
I want to live big, I want to touch sky

Money coming fast, I’m feeling alive
Blessings from above, I dey thank my life
All my enemies, dem dey watch my shine
But I no go fall, I go always rise

[OUTRO]
Yeah yeah...
{artist} inspiration...
{style} mood...
We move!
"""

def generate_random_lyrics():
    return """
[VERSE]
The sky is bright, the road is long,
I sing my heart in every song.
The world keeps moving, time flies by,
I keep my dreams up in the sky.

[CHORUS]
Oh oh oh, I’m feeling free,
This life is made for you and me.
Oh oh oh, we never stop,
We keep on rising to the top.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    mode = request.form.get("mode")
    style = request.form.get("style")
    mood = request.form.get("mood")
    artist = request.form.get("artist")

    if mode == "ai":
        lyrics = generate_ai_lyrics(style, mood, artist)
    else:
        lyrics = generate_random_lyrics()

    return render_template("index.html", lyrics=lyrics)

if __name__ == "__main__":
    app.run(debug=True)
