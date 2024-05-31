from flask import Flask, request, jsonify
import joblib
import re
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

model = joblib.load('model.pkl')

def preprocess_text(text):
    text = text.lower()
    text = re.sub('<.*?>', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from request
    data = request.get_json()
    review = data['review']

    preprocessed_review = preprocess_text(review)

    cv = CountVectorizer()
    preprocessed_review_vectorized = cv.transform([preprocessed_review])

    prediction = model.predict(preprocessed_review_vectorized)

    decoded_prediction = 'positive' if prediction[0] == 1 else 'negative'

    return jsonify({'sentiment': decoded_prediction})

if __name__ == '__main__':
    app.run(debug=True)