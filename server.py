import os
import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dotenv import load_dotenv
from local_vision import analyze_image

load_dotenv(os.path.expanduser("~/.env"))

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
#                 JARVIS CREATOR PROFILE
# =========================================================

CREATOR_PROFILE = {
    "name": "Piyush Katel",

    "role": [
        "PB AI — JARVIS ke developer",
        "JARVIS project ke designer",
        "AI aur coding project par kaam karne wale student"
    ],

    "project": {
        "name": "PB AI — JARVIS",
        "type": "Personal AI Assistant",
        "purpose": (
            "Ek personal AI assistant banana jo conversation, "
            "web information, study help, voice interaction, "
            "music, browser access, smart commands aur "
            "programming-related tasks mein help kar sake."
        )
    },

    "technologies": [
        "Python",
        "Flask",
        "HTML",
        "CSS",
        "JavaScript",
        "GitHub",
        "GitHub Pages",
        "Render",
        "Gemini AI",
        "Termux"
    ],

    "jarvis_features": [
        "AI conversation",
        "Web search",
        "Study assistance",
        "Voice command system",
        "Music and YouTube related features",
        "Browser access",
        "Time and date",
        "Calculator",
        "Battery information",
        "Notes and tasks",
        "Smart commands",
        "Programming assistance",
        "Self-programming feature",
        "Cloud web interface",
        "Mobile browser access",
        "Computer browser access"
    ],

    "development": (
        "Piyush Katel ne JARVIS ko ek personal AI assistant project "
        "ke roop mein develop kiya hai. Project mein Python aur "
        "Flask backend, web frontend, GitHub-based development, "
        "cloud deployment aur Gemini AI integration ka use kiya gaya hai."
    ),

    "ai_information": (
        "JARVIS ke AI responses ke liye Gemini AI service ka use "
        "kiya ja sakta hai. Gemini JARVIS ka owner nahi hai. "
        "JARVIS project ke developer aur designer Piyush Katel hain."
    ),

    "privacy": (
        "Private information jaise ghar ka exact address, family details, "
        "phone number, passwords, API keys aur private credentials "
        "JARVIS ke public profile mein reveal nahi kiye jaate."
    )
}


# =========================================================
#              CREATOR QUESTION DETECTION
# =========================================================

def is_creator_question(q):
    q = q.lower().strip()

    keywords = [
        "owner",
        "your owner",
        "creator",
        "your creator",
        "maker",
        "your maker",
        "developer",
        "your developer",
        "who made you",
        "who created you",
        "who developed you",
        "who built you",
        "who is your owner",
        "who is your creator",
        "who is your developer",

        "kisne banaya",
        "kisne banaya hai",
        "tumhe kisne banaya",
        "tumko kisne banaya",
        "tumhara owner",
        "tumhare owner",
        "tumhara creator",
        "tumhare creator",
        "tumhe kisne develop",
        "tumko kisne develop",
        "banane wala",

        "piyush katel",
        "piyush kaun hai",
        "who is piyush",
        "piyush ke bare",
        "piyush ke baare",
        "piyush ke bare mein",
        "piyush ke baare mein"
    ]

    return any(word in q for word in keywords)


# =========================================================
#          SMART CREATOR PROFILE ANSWER SYSTEM
# =========================================================

def creator_answer(q):
    q = q.lower().strip()
    name = CREATOR_PROFILE["name"]

    # ---- OWNER / CREATOR ----
    if (
        "owner" in q
        or "creator" in q
        or "maker" in q
        or "kisne banaya" in q
        or "who made" in q
        or "who created" in q
        or "who built" in q
    ):
        return (
            f"Mere PB AI — JARVIS project ke developer aur designer "
            f"{name} hain. Unhone JARVIS ko design aur develop kiya hai. "
            f"JARVIS ek personal AI assistant project hai jisme AI chat, "
            f"web access, study help, voice interaction, music, browser "
            f"aur programming-related features hain."
        )

    # ---- DEVELOPER ----
    if (
        "developer" in q
        or "developed" in q
        or "developer kaun" in q
        or "develop kisne" in q
        or "develop kiya" in q
    ):
        return (
            f"{name} PB AI — JARVIS ke developer aur designer hain. "
            f"Unhone Python, Flask, web technologies, GitHub, cloud "
            f"deployment aur AI integration ka use karke JARVIS project "
            f"develop kiya hai."
        )

    # ---- WHO IS PIYUSH ----
    if "piyush" in q:
        return (
            f"{name} PB AI — JARVIS ke developer aur designer hain. "
            f"Woh coding aur AI projects par kaam karte hain. "
            f"Unka main project PB AI — JARVIS hai, jo ek personal AI "
            f"assistant hai. Is project mein AI conversation, web search, "
            f"study assistance, voice commands, music, browser access, "
            f"smart commands aur programming features par kaam kiya gaya hai."
        )

    # ---- TECHNOLOGY ----
    if (
        "technology" in q
        or "technologies" in q
        or "coding" in q
        or "kis mein banaya" in q
        or "what technology" in q
    ):
        return (
            f"{name} ke JARVIS project mein Python, Flask, HTML, CSS, "
            f"JavaScript, GitHub, GitHub Pages, Render, Termux aur "
            f"Gemini AI jaise technologies ka use kiya gaya hai."
        )

    # ---- JARVIS PROJECT ----
    if (
        "project" in q
        or "jarvis" in q
        or "what did he build" in q
        or "kya banaya" in q
    ):
        return (
            f"{name} ka main project PB AI — JARVIS hai. "
            f"JARVIS ek personal AI assistant hai jo AI chat, web search, "
            f"study help, voice interaction, music, browser access, "
            f"smart commands aur programming-related features provide karta hai."
        )

    # ---- GENERAL SAFE PROFILE ----
    return (
        f"{name} PB AI — JARVIS ke developer aur designer hain. "
        f"Unhone JARVIS ko ek personal AI assistant ke roop mein develop kiya hai. "
        f"Project mein Python, Flask, web technologies, GitHub, cloud hosting "
        f"aur Gemini AI integration ka use kiya gaya hai. "
        f"JARVIS mein AI chat, web search, study help, voice commands, "
        f"music, browser access, smart commands aur programming features hain."
    )


# =========================================================
#                       HOME
# =========================================================

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "assistant": "Jarvis"
    })


# =========================================================
#                       ASK
# =========================================================

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json(silent=True) or {}
    command = str(data.get("command", "")).strip()

    if not command:
        return jsonify({
            "reply": "Please send a command."
        }), 400

    # =====================================================
    # IMPORTANT:
    # Creator/Owner/Piyush questions NEVER go to Gemini.
    # Jarvis answers them from its local Creator Profile.
    # =====================================================

    if is_creator_question(command):
        return jsonify({
            "assistant": "Jarvis",
            "command": command,
            "reply": creator_answer(command),
            "source": "local_creator_profile"
        })

    # =====================================================
    # NORMAL AI QUESTIONS
    # =====================================================

    if not API_KEY:
        return jsonify({
            "reply": "Gemini API key is not configured."
        }), 500

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.6-flash:generateContent"
    )

    prompt = (
        "You are PB AI — JARVIS, a helpful AI assistant. "
        "Reply briefly and clearly in Hinglish when appropriate. "
        "Do not claim Tony Stark is your real-world creator. "
        "Do not invent private information about the developer. "
        "User: " + command
    )

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    try:

        response = requests.post(
            url,
            params={"key": API_KEY},
            json=payload,
            timeout=30
        )

        result = response.json()

        if response.status_code != 200:
            return jsonify({
                "reply": "AI service error."
            }), 502

        candidates = result.get("candidates", [])

        if not candidates:
            return jsonify({
                "reply": "AI ne koi response nahi diya."
            }), 502

        reply = (
            candidates[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "Sorry, mujhe response nahi mila.")
        )

        return jsonify({
            "assistant": "Jarvis",
            "command": command,
            "reply": reply
        })

    except requests.Timeout:
        return jsonify({
            "reply": "AI response mein thoda time lag raha hai. Please try again."
        }), 504

    except Exception:
        return jsonify({
            "reply": "Server connection error."
        }), 500



# =========================================================
#              JARVIS LOCAL IMAGE ANALYSIS
# =========================================================

@app.route("/ask-image", methods=["POST"])
def ask_image():
    try:
        image = request.files.get("image")

        if image is None:
            return jsonify({
                "assistant": "Jarvis",
                "reply": "Please upload an image."
            }), 400

        allowed = {
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/gif"
        }

        if image.mimetype not in allowed:
            return jsonify({
                "assistant": "Jarvis",
                "reply": "JPG, PNG, WEBP ya GIF image upload karo."
            }), 400

        os.makedirs("uploads", exist_ok=True)

        filename = secure_filename(image.filename or "jarvis_image.jpg")
        image_path = os.path.join("uploads", filename)

        image.save(image_path)

        result = analyze_image(image_path)

        # Temporary file remove
        try:
            os.remove(image_path)
        except Exception:
            pass

        return jsonify({
            "assistant": "Jarvis",
            "reply": result,
            "source": "local_vision"
        })

    except Exception as e:
        print("LOCAL IMAGE ERROR:", e)
        return jsonify({
            "assistant": "Jarvis",
            "reply": "JARVIS image ko locally process nahi kar saka."
        }), 500

# =========================================================
#                       START
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
