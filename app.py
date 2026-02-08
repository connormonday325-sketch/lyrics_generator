from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# =========================
# SMART LYRICS DATABASE
# =========================

afrobeats_openers = [
    "Yeah yeah, ooh na na",
    "Omo, listen to the vibe",
    "Ahh, this one na for the streets",
    "Baby girl come closer",
    "E choke, e sweet, e loud",
    "Ayy, Lagos nights",
    "This one na jam",
]

trap_openers = [
    "Yeah, uh, let's go",
    "Ayy, straight from the trenches",
    "Yeah, I been grinding nonstop",
    "Uh, money on my mind",
    "They don't know the pain inside",
    "Ayy, we came from nothing",
    "Yeah, yeah, gang",
]

hooks = {
    "Afrobeats": [
        "Baby whine for me, make you no dull",
        "I dey hustle every day, I no fit fall",
        "Your love dey make me lose control",
        "If you ride with me, we go ball",
        "I no go lie, you dey make me soft",
        "Dance with me, no time to pause",
    ],
    "Trap": [
        "I been grinding, no sleep, no rest",
        "Money calling, I ain't like the rest",
        "Came from pain, now I'm up next",
        "They be hating, but I stay blessed",
        "I got dreams bigger than the stress",
        "If it's war, then I'm the test",
    ],
    "Drill": [
        "We move silent, we don't make noise",
        "From the block, we was just some boys",
        "Enemies watching, they got no choice",
        "In the streets, you don't play with toys",
        "Real ones with me, no fake deploy",
    ],
    "RnB": [
        "Hold me closer, don't let me go",
        "Your love feels like a slow tempo",
        "I can't lie, you run my soul",
        "Your touch got me losing control",
        "Stay tonight, let the world stay cold",
    ],
    "Gospel": [
        "God dey guide me, I no dey fear",
        "Through the storm, He hold me near",
        "Every blessing, loud and clear",
        "When I fall, He dry my tears",
        "Na His grace bring me here",
    ]
}

verse_lines = {
    "Afrobeats": [
        "Omo I dey pray make the money come fast",
        "All these fake friends, I don leave them for past",
        "If you love me, no go hold back",
        "Big energy, no dey look back",
        "From the ghetto, but my dreams too loud",
        "I dey shine even inside the crowd",
        "My heart pure but the streets too wild",
        "Lagos to London, we go travel miles",
    ],
    "Trap": [
        "I was down bad, now I'm stacking my bread",
        "Pain in my chest but I smile instead",
        "They switched up when they saw me ahead",
        "I got demons in my head",
        "Came from nothing, now I'm fed",
        "I can't stop till I'm legendary",
        "My life movie, no temporary",
        "Too much pressure but I'm still steady",
    ],
    "Drill": [
        "We don't talk much, we just slide",
        "Real ones only on my side",
        "Enemies hate but they can't survive",
        "In the dark, yeah we still thrive",
        "Don't move wrong, you might get fried",
        "Trust no soul, that's the vibe",
        "Too many snakes, I stay wise",
    ],
    "RnB": [
        "Your eyes got me drowning deep",
        "I been dreaming while you asleep",
        "Every moment feels so sweet",
        "I can't lie, you're all I need",
        "If you leave, my heart will bleed",
        "Hold my hand, don't let me freeze",
    ],
    "Gospel": [
        "Even when I'm weak, God makes me strong",
        "Everyday blessings keep me going on",
        "When life gets hard, I still sing my song",
        "Through the fire, I know I belong",
        "No matter what, I won't do wrong",
        "His love keeps me all along",
    ]
}

bridge_lines = [
    "I remember nights I cried, now I'm stronger",
    "They didn't believe, now they calling my number",
    "Life is a test but I'm built for the pressure",
    "If I fall today, tomorrow I'm better",
    "No more pain, only vibes forever",
    "From nothing to something, I'm chasing the treasure",
]

end_lines = [
    "Yeah yeah, we rise again",
    "Omo, we never lose",
    "This life no balance but we still move",
    "Forever we go shine",
    "Na grace, na hustle, na vibes",
    "The story never ends...",
]

# =========================
# HELPER FUNCTION
# =========================
def generate_song(topic, style):
    style = style.strip()

    if style not in verse_lines:
        style = "Trap"

    if style == "Afrobeats":
        opener = random.choice(afrobeats_openers)
    else:
        opener = random.choice(trap_openers)

    chorus = random.choice(hooks[style])

    verse1 = "\n".join(random.sample(verse_lines[style], 4))
    verse2 = "\n".join(random.sample(verse_lines[style], 4))
    bridge = "\n".join(random.sample(bridge_lines, 2))
    outro = random.choice(end_lines)

    lyrics = f"""
🎶 LYRICS GENERATED 🎶

Topic: {topic.title()}
Style: {style}

{opener}

[VERSE 1]
{verse1}

[CHORUS]
{chorus}
{chorus}

[VERSE 2]
{verse2}

[BRIDGE]
{bridge}

[CHORUS]
{chorus}
{chorus}

[OUTRO]
{outro}
""".strip()

    return lyrics

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_lyrics():
    data = request.get_json()

    topic = data.get("topic", "").strip()
    style = data.get("style", "").strip()

    if not topic:
        return jsonify({"lyrics": "❌ Please enter a song topic."})

    lyrics = generate_song(topic, style)
    return jsonify({"lyrics": lyrics})

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
