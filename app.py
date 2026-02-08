from flask import Flask
@app.route("/")
def home():
    return render_template("index.html")
app = Flask(__name__)
def generate_ai_lyrics(style, mood, artist):
    return f"""
[INTRO]
Yeah yeah...
This one na {style} vibe...
Feeling {mood} tonight...
Inspired by {artist}...

[VERSE 1]
I dey hustle everyday, no time to slow down
I dey shine for the street, yeah I wear my crown
Life no easy but I stand my ground
Blessings on blessings, my joy no go drown

I remember those days when nobody send
Now my name for the air, everywhere I bend
I pray to God make my story never end
I go rise to the top, that's my main intent

[CHORUS]
Money coming fast, I’m feeling alive
Everyday I grind, I dey chase my vibe
No more suffering, I don’t want to survive
I want to live big, I want to live nice

Money coming fast, I’m feeling alive
Blessings from above, I dey thank my God
All my enemies, dem dey watch my stride
But I no go fall, I go always rise

[VERSE 2]
Omo the street too hard, but I still dey smile
Anytime I fall down, I dey bounce back wild
My mama pray for me, say I be her child
Now I dey make am proud, yeah I go far miles

I no dey trust too much, too many fake friends
Dem go show you love, but dem dey plan your end
So I focus on my grind, money must ascend
Cause na only success be the best revenge

[BRIDGE]
If you see me for the road, just know say I dey fight
I dey push my dreams, I no dey sleep for night
God dey guide my steps, everything go alright
I go win this life, yeah I go shine my light

[FINAL CHORUS]
Money coming fast, I’m feeling alive
Everyday I grind, I dey chase my vibe
No more suffering, I don’t want to survive
I want to live big, I want to live nice

Money coming fast, I’m feeling alive
Blessings from above, I dey thank my God
All my enemies, dem dey watch my stride
But I no go fall, I go always rise

[OUTRO]
Yeah yeah...
This is my life, my life...
Afrobeat vibe...
We move...
"""
