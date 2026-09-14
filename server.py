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



@app.route("/youtube-search", methods=["GET"])
def youtube_search():
    import os
    import requests as http_requests

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "success": False,
            "message": "Song name nahi mila."
        }), 400

    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        return jsonify({
            "success": False,
            "message": "YOUTUBE_API_KEY Render Environment mein set nahi hai."
        }), 500

    try:
        response = http_requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": 10,
                "videoEmbeddable": "true",
                "regionCode": "IN",
                "relevanceLanguage": "en",
                "key": api_key
            },
            timeout=20
        )

        data = response.json()

        if response.status_code != 200:
            return jsonify({
                "success": False,
                "message": "YouTube search failed.",
                "details": data
            }), response.status_code

        videos = []

        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            title = item.get("snippet", {}).get("title", "")

            if video_id:
                videos.append({
                    "video_id": video_id,
                    "title": title
                })

        if not videos:
            return jsonify({
                "success": False,
                "message": "Playable song nahi mila."
            }), 404

        return jsonify({
            "success": True,
            "videos": videos
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "YouTube search error.",
            "details": str(e)
        }), 500

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json(silent=True) or {}
    command = str(data.get("command", "")).strip()

    if not command:
        return jsonify({
            "reply": "❌ JARVIS: Please send a command."
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
    # JARVIS GREETINGS
    # =====================================================

    greeting_words = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "namaste",
        "namaskar",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if command.lower() in greeting_words:
        return jsonify({
            "assistant": "Jarvis",
            "command": command,
            "reply": "Hello! 👋 Main JARVIS hoon. Batao, main tumhari kya help kar sakta hoon?",
            "source": "local_jarvis"
        })

    # =====================================================
    # NORMAL AI QUESTIONS
    # =====================================================

    if not API_KEY:
        return jsonify({
            "reply": "❌ JARVIS: AI service configuration available nahi hai."
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
                "reply": "❌ JARVIS: AI service error."
            }), 502

        candidates = result.get("candidates", [])

        if not candidates:
            return jsonify({
                "reply": "❌ JARVIS: Mujhe koi response nahi mila."
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
            "reply": "⏳ JARVIS: Response mein thoda time lag raha hai. Please try again."
        }), 504

    except Exception:
        return jsonify({
            "reply": "❌ JARVIS: Server connection error."
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



# ================= GEMINI IMAGE EDITING =================

@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    try:
        import os
        import base64
        import requests as http_requests

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return jsonify({
                "message": "❌ GEMINI_API_KEY Render Environment mein set nahi hai."
            }), 500

        if "image" not in request.files:
            return jsonify({
                "message": "❌ Photo nahi mili."
            }), 400

        uploaded = request.files["image"]
        image_bytes = uploaded.read()

        if not image_bytes:
            return jsonify({
                "message": "❌ Uploaded photo empty hai."
            }), 400

        mime_type = uploaded.mimetype or "image/jpeg"

        prompt = request.form.get(
            "prompt",
            "Create a high-quality artistic version of this photo."
        )

        image_data = base64.b64encode(image_bytes).decode("utf-8")

        payload = {
            "model": "gemini-3.1-flash-image",
            "input": [
                {
                    "type": "image",
                    "mime_type": mime_type,
                    "data": image_data
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ],
            "response_format": {
                "type": "image",
                "mime_type": "image/png",
                "image_size": "1K"
            }
        }

        response = http_requests.post(
            "https://generativelanguage.googleapis.com/v1beta/interactions",
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=300
        )

        if response.status_code != 200:
            print("GEMINI ERROR:", response.status_code)
            print(response.text)

            return jsonify({
                "message": "❌ JARVIS image generation failed.",
                "details": f"API Status: {response.status_code} | {response.text[:1500]}"
            }), 500

        result = response.json()

        # Gemini 3.1 Flash Image returns the generated image
        # in output_image.data
        output_image = result.get("output_image")

        if not output_image:
            print("NO OUTPUT_IMAGE IN GEMINI RESPONSE:")
            print(result)

            return jsonify({
                "message": "❌ JARVIS image return nahi kar saka.",
                "details": str(result)[:1500]
            }), 500

        generated_image = output_image.get("data")
        generated_mime = output_image.get("mime_type", "image/png")

        if not generated_image:
            print("OUTPUT_IMAGE DATA MISSING:")
            print(result)

            return jsonify({
                "message": "❌ JARVIS image data nahi mila.",
                "details": str(result)[:1500]
            }), 500

        image_url = (
            "data:"
            + generated_mime
            + ";base64,"
            + generated_image
        )

        return jsonify({
            "success": True,
            "message": "🖼️ JARVIS ne image create kar di!",
            "image_url": image_url
        })

    except Exception as e:
        print("ANALYZE IMAGE ERROR:", repr(e))

        return jsonify({
            "message": "❌ Image processing error.",
            "details": str(e)
        }), 500

# ================= END GEMINI IMAGE EDITING =================


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
