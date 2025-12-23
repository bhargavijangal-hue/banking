FAQs = [
    {"question": "What are your account opening requirements?",
     "answer": "To open an account you need a valid ID, proof of address, and initial deposit."},

    {"question": "How do I reset my online banking password?",
     "answer": "You can reset your password by clicking ‘Forgot Password’ on the login screen."},

    {"question": "What are your customer service hours?",
     "answer": "Customer support is available from 8AM to 8PM every day."},

    {"question": "How do I check my account balance?",
     "answer": "Log into the app or visit our website to view your balance."},
]
import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from faq_data import FAQs

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.post("/chat")
def chatbot():
    data = request.json
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    # Build initial prompt to help the model answer FAQs
    faq_prompt = "Here are the FAQs and answers:\n"
    for faq in FAQs:
        faq_prompt += f"Q: {faq['question']}\nA: {faq['answer']}\n\n"

    prompt = f"""{faq_prompt}
    User query: {user_msg}
    Answer:"""

    # Call OpenAI’s Chat Completion or GPT model
    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.2
    )

    answer = response.choices[0].message["content"].strip()

    return jsonify({"user": user_msg, "reply": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
