from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Lyrics templates (basic AI style generator)
def generate_lyrics(topic, style, mood, artist):
    intro = f"🎶 Lyrics Generated 🎶\nTopic: {topic}\nStyle: {style}\nMood: {mood}\nInspired by: {artist}\n\n"

    # Mood-based lines
    mood_lines = {
        "Happy": [
            "Smile on my face, I feel alive,",
            "We dancing all night, we feeling the vibe,",
            "No stress today, we rise and shine,",
            "Good energy, everything fine,"
        ],
        "Sad": [
            "Tears in my eyes but I hide the pain,",
            "Lonely nights and the pouring rain,",
            "Memories hurt, I can’t explain,",
            "I call your name but it feels in vain,"
        ],
        "Romantic": [
            "Girl you the reason my heart beats fast,",
            "Your love so real, I hope it lasts,",
            "Hold me close, don’t let me pass,",
            "You my future, forget the past,"
        ],
        "Motivational": [
            "No sleep, no rest, I’m chasing my dream,",
            "Came from the dirt but I got a big team,",
            "Hard work daily, nothing is free,",
            "I’m on my way, just wait and see,"
        ],
        "Angry": [
            "They talk too much but they don’t know me,",
            "Fake love around, I cut them slowly,",
            "I’ve been betrayed, now I move lonely,",
            "No more chances, you can’t control me,"
        ],
        "Party": [
            "Lights go up, we turning insane,",
            "Champagne vibes, no time for shame,",
            "Dance all night, forget the pain,",
            "We run the city, we own the game,"
        ]
    }

    # Style-based chorus templates
    style_chorus = {
        "Afrobeats": "Ohh we dey vibe, we dey groove,\nBad energy make we remove,\nMoney dey come, blessings approve,\nWe go shine, nothing to lose.\n",
        "Amapiano": "Gbedu dey burst, we dey dance slow,\nFeel the rhythm make your body go,\nAll my people dem dey show,\nTonight we party till tomorrow.\n",
        "Trap": "I been hustling all night, no sleep,\nBig dreams yeah I gotta keep,\nMoney calling, I’m too deep,\nIn the streets yeah I move discreet.\n",
        "Hip-Hop": "I spit real bars, no cap in my flow,\nFrom the struggle now I glow,\nThey wanna stop me but I say no,\nI keep rising, watch me grow.\n",
        "Drill": "In the ends where it get cold,\nHeart so dark, my story bold,\nI move fast, I can’t be sold,\nReal ones stand, never fold.\n",
        "Pop": "We can fly, we can shine,\nYou and me yeah we divine,\nHold my hand, you’ll be fine,\nThis love story feels like mine.\n",
        "RnB": "Slow wine baby, feel my touch,\nYou got my heart, I need you much,\nLate night talks, I miss you so much,\nYour love strong, it’s a magic clutch.\n",
        "Gospel": "Jehovah guide me every day,\nBlessings follow, I pray I stay,\nNo weapon formed shall ever slay,\nI give Him praise in every way.\n",
        "Reggae": "One love, one heart, we stay strong,\nThrough the struggle we move along,\nLife is hard but we sing this song,\nIn Jah we trust, we don’t do wrong.\n",
        "Dancehall": "Gyal come wine, move your waistline,\nTonight is yours, tonight is mine,\nBadman style with the bassline,\nWe party hard till the sunrise shine.\n"
    }

    # Default if missing
    mood_pick = mood_lines.get(mood, mood_lines["Motivational"])
    chorus = style_chorus.get(style, style_chorus["Afrobeats"])

    verse1 = "\n🔥 Verse 1:\n" + "\n".join(random.sample(mood_pick, 4)) + "\n"
    chorus_block = "\n🎤 Chorus:\n" + chorus + "\n"
    verse2 = "\n🔥 Verse 2:\n" + "\n".join(random.sample(mood_pick, 4)) + "\n"
    outro = f"\n✨ Outro:\n{topic} on my mind, I never stop,\n{style} vibes make the whole world pop!\n"

    return intro + verse1 + chorus_block + verse2 + outro


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    topic = data.get("topic", "").strip()
    style = data.get("style", "").strip()
    mood = data.get("mood", "").strip()
    artist = data.get("artist", "").strip()

    if not topic or not style or not mood:
        return jsonify({"lyrics": "❌ Please provide Topic, Style and Mood."})

    if not artist:
        artist = "Unknown Artist"

    lyrics = generate_lyrics(topic, style, mood, artist)

    return jsonify({"lyrics": lyrics})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
