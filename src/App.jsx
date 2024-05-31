import React, { useState } from 'react';

function App() {
  const [reviewText, setReviewText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleReviewSubmit = async () => {
    setPrediction(null);
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/', {
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
        setError('Error: ' + response.statusText);
      }
    } catch (error) {
      setError('Error: ' + error.message);
    } finally {
      setIsLoading(false);
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
        <button onClick={handleReviewSubmit} disabled={isLoading}>
          {isLoading ? 'Predicting...' : 'Predict Sentiment'}
        </button>
        {prediction && <p>Sentiment Prediction: {prediction}</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    </>
  );
}

export default App;
