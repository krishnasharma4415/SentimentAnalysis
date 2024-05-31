from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'count_vectorizer.pkl')

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

stop_words = set(stopwords.words('english'))

def remove_html(text):
    return BeautifulSoup(text, "html.parser").get_text()

def remove_stopwords(text):
    return ' '.join(word for word in text.split() if word not in stop_words)

@app.route('/', methods=['POST'])
def predict():
    try:
        data = request.json
        review = data.get('review', '')

        if not review:
            return jsonify({'error': 'No review provided'}), 400

        review = review.lower()
        review = remove_html(review)
        review = remove_stopwords(review)

        review_vectorized = vectorizer.transform([review]).toarray()

        prediction = model.predict(review_vectorized)
        sentiment = 'positive' if prediction[0] == 1 else 'negative'

        return jsonify({'sentiment': sentiment})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.run(debug=True)


# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return( "Hello World" )
    
# app.run()