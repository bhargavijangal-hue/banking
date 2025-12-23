from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

def load_faq(json_path="faq_data.json"):
    if not os.path.exists(json_path):
        return []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("faqs", [])

faq_list = load_faq()

def find_answer(user_msg: str):
    msg = user_msg.lower().strip()
    # exact match
    for item in faq_list:
        q = item.get("question", "").lower().strip()
        if msg == q:
            return item.get("answer")
    # substring / keyword match
    for item in faq_list:
        q = item.get("question", "").lower().strip()
        if q in msg:
            return item.get("answer")
    # fallback
    return "Sorry, I didn't understand that. Could you please rephrase?"

@app.route("/", methods=["GET"])
def home():
    return "Bank FAQ Bot is running. Use POST /chat with JSON {\"message\": \"your question\"}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if (not data) or ("message" not in data):
        return jsonify({"error": "No message provided"}), 400
    user_msg = data["message"]
    answer = find_answer(user_msg)
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)
