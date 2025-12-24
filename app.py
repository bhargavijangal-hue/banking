import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Load FAQ data
df = pd.read_csv("BankFAQs.csv")

# 2. Prepare embedding vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["question"])

print("📌 Banking FAQ Bot is ready! Ask your questions (type EXIT to quit).")

while True:
    user_input = input("\nYou: ")

    if user_input.strip().lower() == "exit":
        print("Bot: Thank you! Have a great day! 😊")
        break

    # 3. Transform user query into vector
    query_vec = vectorizer.transform([user_input])

    # 4. Compute similarity with FAQ questions
    similarities = cosine_similarity(query_vec, X)
    idx = np.argmax(similarities)

    # 5. Simple threshold to check match quality
    if similarities[0][idx] < 0.3:
        print("Bot: Sorry, I’m not sure about that. Can you rephrase?")
    else:
        response = df.iloc[idx]["answer"]
        print(f"Bot: {response}")
