import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.env"))

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/")
def home():
    return jsonify({"status": "online", "assistant": "Jarvis"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    command = str(data.get("command", "")).strip()

    if not command:
        return jsonify({"reply": "Please send a command."}), 400

    if not API_KEY:
        return jsonify({"reply": "Gemini API key is not configured."}), 500

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "You are Jarvis, a helpful AI assistant. Reply briefly and clearly in Hinglish when appropriate.\nUser: " + command
                    }
                ]
            }
        ]
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
            return jsonify({"reply": "AI service error.", "details": result}), 502

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({
            "assistant": "Jarvis",
            "command": command,
            "reply": reply
        })

    except Exception as e:
        return jsonify({"reply": "Server error.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
