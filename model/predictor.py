from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import os
import re

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "random_forest_model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "TfidfVectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

stop_words = set(stopwords.words("english"))


def clean_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = ' '.join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    return text


@app.route("/", methods=["POST", "GET"])
def predict():
    try:
        data = request.json
        review = data.get("review", "")

        if not review:
            return jsonify({"error": "No review provided"}), 400

        review = review.apply(clean_text)

        review_vectorized = vectorizer.transform([review]).toarray()
        prediction = model.predict(review_vectorized)
        sentiment = "positive" if prediction[0] == 1 else "negative"

        return jsonify({"sentiment": sentiment})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
