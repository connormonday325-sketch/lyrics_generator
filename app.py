from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


# ===============================
# RANDOM LYRICS GENERATOR SYSTEM
# ===============================

def generate_ai_lyrics(style, mood, artist):

    intros = [
        f"Yeah yeah...\nThis one na {style} vibe...\nInspired by {artist}...\nWe move!",
        f"Ahhh!\n{style} mode activated...\nFeeling {mood} tonight...\n{artist} inspiration!",
        f"Yo!\nNew jam alert...\n{style} sound...\n{mood} energy...\nLet's go!"
    ]

    hustle_lines = [
        "I dey hustle everyday, no time to sleep",
        "I no fit dull, my dreams too deep",
        "I dey pray make blessings follow me",
        "Everyday na fight, but I still dey breathe",
        "Dem say I no go make am, I prove dem wrong",
        "From the gutter to the glory, I dey move strong",
        "I no dey fear anybody, na God dey guide me",
        "My story go loud, even blind go see me"
    ]

    love_lines = [
        "Baby your love dey make me go crazy",
        "When you smile, my heart dey move lazy",
        "I no fit lie, you be my peace",
        "Your body fire, make my worries cease",
        "Hold me close, no let me fall",
        "If na you, I go answer your call"
    ]

    sad_lines = [
        "Tears for my pillow but I still dey smile",
        "Pain for my chest but I walk in style",
        "Nobody know wetin I face inside",
        "But I still dey stand, I no dey hide",
        "Broken dreams but I still believe",
        "Even in darkness, I go still achieve"
    ]

    flex_lines = [
        "Now dem dey watch me, I don turn star",
        "Big money lifestyle, I don go far",
        "Champagne for my table, blessings in my hand",
        "I dey shine so bright, dem no understand",
        "I no dey beg again, na me dem dey call",
        "Success sweet pass sugar, I no go fall"
    ]

    adlibs = [
        "(yeah yeah!)",
        "(we move!)",
        "(omo!)",
        "(ahh!)",
        "(no cap!)",
        "(straight!)",
        "(e choke!)",
        "(gbedu!)"
    ]

    chorus_templates = [
        f"Money coming fast, I’m feeling alive {random.choice(adlibs)}\n"
        f"Everyday I grind, I dey chase my vibe\n"
        f"No more suffering, I don’t want to cry\n"
        f"I want to live big, I want to touch sky\n"
        f"Blessings on blessings, I dey thank my life\n"
        f"All my enemies dey watch my shine\n"
        f"But I no go fall, I go always rise",

        f"Baby hold me tight, make we vibe tonight {random.choice(adlibs)}\n"
        f"This {style} sound dey burst my mind\n"
        f"I no fit lie, you be my light\n"
        f"Everytime you call, I dey feel alright\n"
        f"Love and money, na wetin I find\n"
        f"I go run am, till the end of time",

        f"Life too hard but I still dey stand {random.choice(adlibs)}\n"
        f"Everyday I pray, I dey hold my ground\n"
        f"Dem dey talk, but I no dey hear sound\n"
        f"My destiny big, I no fit slow down\n"
        f"God dey my back, blessings dey around\n"
        f"I go rise, I no go fall down"
    ]

    # Mood-based verse selection
    if mood.lower() in ["motivational", "hustle", "success"]:
        verse_pool = hustle_lines + flex_lines
    elif mood.lower() in ["love", "romantic", "happy"]:
        verse_pool = love_lines + flex_lines
    elif mood.lower() in ["sad", "pain", "heartbreak"]:
        verse_pool = sad_lines + hustle_lines
    else:
        verse_pool = hustle_lines + love_lines + sad_lines + flex_lines

    # Randomly pick lines
    verse1 = "\n".join(random.sample(verse_pool, 6))
    verse2 = "\n".join(random.sample(verse_pool, 6))
    verse3 = "\n".join(random.sample(verse_pool, 6))

    chorus = random.choice(chorus_templates)

    bridge = f"""
Oh oh oh...
We go rise, we go shine {random.choice(adlibs)}
Oh oh oh...
Everything go align
Oh oh oh...
No more tears, no more pain
Oh oh oh...
Only blessings remain
"""

    lyrics = f"""
[INTRO]
{random.choice(intros)}

[VERSE 1]
{verse1}

[PRE-CHORUS]
Me I no dey fear, I no dey run
If I fall today, tomorrow I go come
God dey my back, blessings dey my front
Anything I want, I go get am once {random.choice(adlibs)}

[CHORUS]
{chorus}

[VERSE 2]
{verse2}

[CHORUS]
{chorus}

[VERSE 3]
{verse3}

[BRIDGE]
{bridge}

[FINAL CHORUS]
{chorus}

[OUTRO]
Yeah yeah...
{artist} inspiration...
{style} mood...
Feeling {mood}...
We made it!
"""

    return lyrics.strip()


# ===============================
# ROUTES
# ===============================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    style = request.form.get("style", "Afrobeats")
    mood = request.form.get("mood", "Motivational")
    artist = request.form.get("artist", "Wizkid")

    lyrics = generate_ai_lyrics(style, mood, artist)

    return jsonify({"lyrics": lyrics})


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
