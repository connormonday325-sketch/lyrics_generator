from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    mood = request.form.get("mood", "Happy")
    artist = request.form.get("artist", "Wizkid")
    topic = request.form.get("topic", "Love")

    lyrics = f"""
[INTRO]
Yeah yeah...
This one na {mood} vibe...
Inspired by {artist}...
Eyy...

[VERSE 1]
I dey think about {topic} for my mind all day
Every little moment, e dey make me wan pray
Life no easy but I still dey maintain
Steady on my grind, no be story I dey claim

I remember those days when nobody believe
Now I dey shine small, see the blessings we receive
If na money, if na fame, if na peace we dey chase
I go still carry {topic} for my heart and my space

[PRE-CHORUS]
Oh my baby no go fear
I go hold you close right here
Even if the night cold pass
We go still survive this year

[CHORUS]
Oh oh oh...
{topic} don catch me for my soul
Oh oh oh...
Na you be the one I want
Oh oh oh...
No go leave me make I fall
This {mood} feeling, e dey burst my heart

[VERSE 2]
Me I no fit lie, you dey give me ginger
Anytime you smile, e dey make me stronger
People talk plenty but I no dey hear
As long as you dey here, everything clear

I dey hustle everyday, no time to relax
But your love na the peace wey I never lack
If the world turn upside down, I go still stand
Cause {topic} na the blessing wey I hold for my hand

[BRIDGE]
If the rain fall, I go cover you
If the pain come, I go fight for you
If dem say love hard, I go prove them wrong
Cause your matter na my favorite song

[FINAL CHORUS]
Oh oh oh...
{topic} don catch me for my soul
Oh oh oh...
Na you be the one I want
Oh oh oh...
No go leave me make I fall
This {mood} feeling, e dey burst my heart

[OUTRO]
Yeah yeah...
{artist} vibes...
{mood} mood...
Talking about {topic}...
Eyy...
"""

    return render_template("index.html", lyrics=lyrics)


if __name__ == "__main__":
    app.run(debug=True)
