from flask import Flask, render_template, request

app = Flask(__name__)

def generate_ai_lyrics(style, mood, artist):
    return f"""
[INTRO]
Yeah yeah...
This one na {style} vibe...
Feeling {mood} tonight...
Inspired by {artist}...
We move!

[VERSE 1]
I dey hustle everyday, no time to sleep
I dey pray make blessings follow me deep
Life no easy but I stand my ground
Even when dem laugh, I no back down

I remember those days when nobody see
Now my name for the air, everywhere I be
From the gutter to the glory, I dey climb
Now my destiny don enter my time

[PRE-CHORUS]
Me I no dey fear, I no dey run
If I fall today, tomorrow I go come
God dey my back, blessings dey my front
Anything I want, I go get am once

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
My heart full of pain but I still dey dance
Because I know say my story get chance
Dem say I no go make am, dem talk too much
Now I dey collect blessing, dem dey look and touch

Street no get mercy, but I get grace
I dey run my race, I no slow my pace
Anytime I pray, I dey feel the fire
Every single day, I dey go higher

[PRE-CHORUS]
Me I no dey fear, I no dey run
If I fall today, tomorrow I go come
God dey my back, blessings dey my front
Anything I want, I go get am once

[CHORUS]
Money coming fast, I’m feeling alive
Everyday I grind, I dey chase my vibe
No more suffering, I don’t want to cry
I want to live big, I want to touch sky

Money coming fast, I’m feeling alive
Blessings from above, I dey thank my life
All my enemies, dem dey watch my shine
But I no go fall, I go always rise

[VERSE 3]
Now I dey flex small, but I still dey humble
Because I know say life fit make man stumble
I no dey trust anybody too much
I just dey focus, I just dey clutch

My mama prayers dey cover my head
Even when my pocket empty like bread
I go make am, I swear on my soul
This {style} sound dey heal my whole

[BRIDGE]
Oh oh oh...
We go rise, we go shine
Oh oh oh...
Everything go align
Oh oh oh...
No more tears, no more pain
Oh oh oh...
Only blessings remain

[FINAL CHORUS]
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
Feeling {mood}...
We made it!
"""

@app.route("/", methods=["GET", "POST"])
def home():
    lyrics = ""
    if request.method == "POST":
        style = request.form.get("style")
        mood = request.form.get("mood")
        artist = request.form.get("artist")
        lyrics = generate_ai_lyrics(style, mood, artist)

    return render_template("index.html", lyrics=lyrics)

if __name__ == "__main__":
    app.run(debug=True)
