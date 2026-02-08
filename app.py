from flask import Flask, render_template, request, jsonify
import random
import os
from datetime import datetime

app = Flask(__name__)

# ===============================
# LYRICS DATABASE (SMART RANDOM)
# ===============================

OPENERS = {
    "Afrobeats": [
        "Yeah yeah, omo this vibe too sweet",
        "Omo, listen to the sound of the street",
        "Ahh, Lagos nights dey call my name",
        "Baby girl come closer make we dance",
        "E choke, e loud, e sweet, no cap",
        "Na your love dey scatter my brain",
    ],
    "Trap": [
        "Yeah, I been grinding nonstop",
        "Money on my mind, I can’t stop",
        "Came from the bottom now I’m up",
        "They don’t know the pain I felt",
        "I’m chasing dreams, not sleep",
    ],
    "Drill": [
        "Real life, no cap, no acting",
        "Street talk, everybody watching",
        "If I move wrong, dem go chat",
        "Cold heart, but my spirit strong",
    ],
    "Gospel": [
        "Lord I give You all the glory",
        "Your grace has changed my story",
        "Even in the storm I stand",
        "Your mercy keeps holding me",
    ],
    "R&B": [
        "Girl you got me feeling some type way",
        "Late night calls, you on my mind",
        "Your love is sweeter than wine",
        "Hold me close, don’t let go",
    ],
    "Love Song": [
        "Baby I no fit lie, na you I want",
        "Your smile dey make my heart calm",
        "Forever with you, that’s the plan",
        "You be my peace, you be my home",
    ]
}

HOOKS = {
    "Afrobeats": [
        "Na you be my vibe, na you be my vibe",
        "We go dance all night till the morning light",
        "Your love dey make me high, dey make me high",
    ],
    "Trap": [
        "I’m on the road to the top, can’t stop",
        "Money coming fast, yeah I want more",
        "I can’t fold, I can’t break",
    ],
    "Drill": [
        "No love for the fake, no love for the lies",
        "We move silent but we deadly",
        "Street life tough but we ready",
    ],
    "Gospel": [
        "I will praise You every day",
        "Your love never fails me",
        "Jesus You are my strength",
    ],
    "R&B": [
        "Girl I want you close tonight",
        "You and me, no stress, just vibes",
        "Your love is all I need",
    ],
    "Love Song": [
        "You be my one and only",
        "I’ll love you till forever",
        "Your love is my medicine",
    ]
}

BRIDGES = {
    "Afrobeats": [
        "If I fall today, tomorrow I’m better",
        "No more pain, only vibes forever",
        "We go dey alright, no matter the weather",
    ],
    "Trap": [
        "I lost friends but I gained focus",
        "I been through hell, still I’m standing",
        "Hard times made me stronger",
    ],
    "Drill": [
        "Dem wan test me, but I no dey fear",
        "I stay alert, I stay prepared",
        "I no fit lose guard, not here",
    ],
    "Gospel": [
        "Even when I cry, You still hear me",
        "You never leave me alone",
        "Your light is guiding me home",
    ],
    "R&B": [
        "I don’t want nobody else",
        "I just want your heart tonight",
        "You’re the only one I feel",
    ],
    "Love Song": [
        "I’ll fight for you any day",
        "Even if the world turns cold",
        "My love for you won’t fade",
    ]
}

OUTROS = {
    "Afrobeats": [
        "Na grace, na hustle, na vibes",
        "We go dey alright",
        "This love no go end",
    ],
    "Trap": [
        "Yeah, we made it",
        "Still grinding, still winning",
        "Legendary lifestyle",
    ],
    "Drill": [
        "No fear, only action",
        "We keep moving",
        "Street made me",
    ],
    "Gospel": [
        "All glory to God",
        "Jesus is King",
        "Forever I praise",
    ],
    "R&B": [
        "Girl you’re my peace",
        "I’m yours forever",
        "Love don’t die",
    ],
    "Love Song": [
        "Forever you and I",
        "You be my destiny",
        "My heart is yours",
    ]
}

MOODS = {
    "Happy": ["smiling", "dancing", "vibing"],
    "Sad": ["crying", "missing you", "broken inside"],
    "Motivational": ["grinding", "focused", "never giving up"],
    "Romantic": ["in love", "obsessed", "thinking of you"],
    "Street": ["hustling", "surviving", "moving smart"],
}

# ===============================
# PREMIUM CONTROL (LIMIT FREE)
# ===============================

FREE_LIMIT = 3  # free generations per day


def get_today_key():
    return datetime.now().strftime("%Y-%m-%d")


# store in memory (works on Render but resets sometimes)
user_usage = {}


def can_generate(ip):
    today = get_today_key()
    if ip not in user_usage:
        user_usage[ip] = {}

    if today not in user_usage[ip]:
        user_usage[ip][today] = 0

    return user_usage[ip][today] < FREE_LIMIT


def increase_usage(ip):
    today = get_today_key()
    user_usage[ip][today] += 1


# ===============================
# ROUTES
# ===============================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    topic = data.get("topic", "").strip()
    style = data.get("style", "Afrobeats")
    mood = data.get("mood", "Happy")
    artist = data.get("artist", "None")
    mode = data.get("mode", "free")  # free or premium

    user_ip = request.remote_addr

    # premium mode bypass limit
    if mode == "free":
        if not can_generate(user_ip):
            return jsonify({
                "error": True,
                "message": "Free limit reached! Upgrade to Premium for unlimited lyrics."
            })

        increase_usage(user_ip)

    if not topic:
        topic = "love and hustle"

    opener = random.choice(OPENERS.get(style, OPENERS["Afrobeats"]))
    hook = random.choice(HOOKS.get(style, HOOKS["Afrobeats"]))
    bridge = random.choice(BRIDGES.get(style, BRIDGES["Afrobeats"]))
    outro = random.choice(OUTROS.get(style, OUTROS["Afrobeats"]))

    mood_words = random.choice(MOODS.get(mood, MOODS["Happy"]))

    lyrics = f"""
🎵 {topic.upper()} ({style} / {mood})

[INTRO]
{opener}

[VERSE 1]
Talking about {topic}, I’m {mood_words}
Life no easy but I still dey move
Every day I pray make I improve
No time for fake, only truth

[CHORUS]
{hook}
{hook}

[VERSE 2]
Inspired by {artist}, I dey feel the vibe
I no go stop till I touch the sky
Pain in my chest but I smile instead
Too much pressure but I’m still steady

[BRIDGE]
{bridge}
{bridge}

[FINAL CHORUS]
{hook}
{hook}

[OUTRO]
{outro}
""".strip()

    return jsonify({"error": False, "lyrics": lyrics})


# ===============================
# PAYSTACK PLACEHOLDER ROUTE
# ===============================
@app.route("/paystack-key")
def paystack_key():
    # Replace later with your real public key
    return jsonify({"publicKey": "pk_test_xxxxxxxxxxxxxxxxxxxxx"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
