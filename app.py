from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# ==============================
# FREE SMART LYRICS DATABASE
# ==============================

openers = {
    "Trap": [
        "Yeah, uh, let's go",
        "Ayy, straight from the trenches",
        "Uh, money on my mind",
        "They don't know the pain inside",
        "Ayy, we came from nothing",
        "Yeah yeah, gang",
    ],
    "Afrobeats": [
        "Yeah yeah, ooh na na",
        "Omo, listen to the vibe",
        "Ahh, this one na for the street",
        "Baby girl come closer",
        "E choke, e sweet, e loud",
        "Ayy, Lagos nights",
    ],
    "Hip Hop": [
        "Listen up, let me talk my talk",
        "I been grinding all my life",
        "From the bottom, now we rising",
        "I ain't here for the jokes",
        "They doubted me, now they silent",
    ],
    "R&B": [
        "Girl, you got me feeling something",
        "Late night vibes in my mind",
        "I don't wanna lose your love",
        "Your body calling my name",
        "I been thinking 'bout you lately",
    ],
}

hooks = {
    "Trap": [
        "I hustle everyday, no sleep for my eyes",
        "They be hating but I still survive",
        "Money coming fast, I’m feeling alive",
        "I’m chasing the bag, no time for lies",
    ],
    "Afrobeats": [
        "Baby girl, make you whine for me",
        "Tonight we go dance till morning",
        "Your love dey sweet like honey",
        "Omo, this vibe dey make me happy",
    ],
    "Hip Hop": [
        "I came too far, can't go back now",
        "They never believed, look at me now",
        "My dreams big, I won't back down",
        "I write my story, I wear the crown",
    ],
    "R&B": [
        "Girl, your love is all I need",
        "Hold me close and never leave",
        "You got my heart on a string",
        "I’m addicted to the way you breathe",
    ],
}

verses = {
    "Motivational": [
        "Pain in my chest but I smile instead",
        "Too much pressure but I'm still steady",
        "I can't stop till I'm legendary",
        "Every setback made me stronger already",
        "Nobody helped me, I built myself",
    ],
    "Love": [
        "Your body got me losing control",
        "Every time you smile, you heal my soul",
        "I want you close, don’t let me go",
        "Your love is fire, burning slow",
    ],
    "Sad": [
        "I’ve been lonely in a crowded room",
        "Tears fall quietly like rain in June",
        "My heart broke, but I still pretend",
        "I lost myself trying to be your friend",
    ],
    "Party": [
        "Tonight we turn up, no stress allowed",
        "Champagne popping, music loud",
        "Dancing like we don’t care now",
        "All my guys in the club right now",
    ],
}

bridges = [
    "If I fall today, tomorrow I'm better",
    "No more pain, only vibes forever",
    "I pray for blessings, not for pleasure",
    "I came too far to lose my treasure",
    "God dey guide me through the weather",
]

outros = [
    "Na grace, na hustle, na vibes",
    "We go make am, no lies",
    "Forever we rise, we rise",
    "This is my life, my life",
    "Omo, we don win already",
]

# ==============================
# AI MODE PLACEHOLDER (FUTURE)
# ==============================

def ai_generate_lyrics(topic, style, mood, artist):
    # This is where you will later connect OpenAI API
    # For now, we simulate "AI style" using smart randomness

    opener = random.choice(openers.get(style, ["Yeah, let's go"]))
    hook = random.choice(hooks.get(style, ["We keep going strong"]))
    verse_line = random.choice(verses.get(mood, ["I keep pushing everyday"]))
    bridge = random.choice(bridges)
    outro = random.choice(outros)

    lyrics = f"""
🎶 Lyrics AI Generated 🎶

Topic: {topic}
Style: {style}
Mood: {mood}
Artist Inspiration: {artist}

[INTRO]
{opener}

[VERSE 1]
{verse_line}
{random.choice(verses.get(mood, verses["Motivational"]))}
{random.choice(verses.get(mood, verses["Motivational"]))}

[CHORUS]
{hook}
{hook}

[VERSE 2]
{random.choice(verses.get(mood, verses["Motivational"]))}
{random.choice(verses.get(mood, verses["Motivational"]))}
Talking about {topic}, I never fold.

[BRIDGE]
{bridge}

[FINAL CHORUS]
{hook}
{hook}

[OUTRO]
{outro}
""".strip()

    return lyrics


def random_generate_lyrics(topic, style, mood):
    opener = random.choice(openers.get(style, ["Yeah, let's go"]))
    hook = random.choice(hooks.get(style, ["We keep going strong"]))
    verse_line = random.choice(verses.get(mood, ["I keep pushing everyday"]))
    bridge = random.choice(bridges)
    outro = random.choice(outros)

    lyrics = f"""
🎵 Random Lyrics Generated 🎵

Topic: {topic}
Style: {style}
Mood: {mood}

[INTRO]
{opener}

[VERSE]
{verse_line}
{random.choice(verses.get(mood, verses["Motivational"]))}
{random.choice(verses.get(mood, verses["Motivational"]))}

[CHORUS]
{hook}
{hook}

[BRIDGE]
{bridge}

[OUTRO]
{outro}
""".strip()

    return lyrics


# ==============================
# ROUTES
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    topic = data.get("topic", "Love")
    style = data.get("style", "Trap")
    mood = data.get("mood", "Motivational")
    artist = data.get("artist", "Wizkid")
    mode = data.get("mode", "ai")  # ai or random

    if mode == "random":
        lyrics = random_generate_lyrics(topic, style, mood)
    else:
        lyrics = ai_generate_lyrics(topic, style, mood, artist)

    return jsonify({"lyrics": lyrics})


if __name__ == "__main__":
    app.run(debug=True)
