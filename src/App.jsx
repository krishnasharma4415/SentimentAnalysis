import React, { useState } from 'react';  
import './App.css';

function App() {
  const [count, setCount] = useState(0);
  const [reviewText, setReviewText] = useState('');
  const [prediction, setPrediction] = useState('');

  const handleReviewSubmit = async () => {
    // Make API call to Flask backend
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ review: reviewText })
      });
      
      if (response.ok) {
        const data = await response.json();
        setPrediction(data.sentiment);
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <>
      <div className="card">
        <textarea
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          placeholder="Enter review text..."
        />
        <button onClick={handleReviewSubmit}>Predict Sentiment</button>
        <p>Sentiment Prediction: {prediction}</p>
      </div>
    </>
  );
}

export default App;
