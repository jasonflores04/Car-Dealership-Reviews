"""
Sentiment Analyzer API
----------------------
A simple Flask-based API that uses NLTK's SentimentIntensityAnalyzer
to classify text as positive, negative, or neutral.

Endpoints:
 - GET / -> Welcome message
 - GET /analyze/<text> -> Analyze sentiment of input text

Example:
    GET /analyze/I love this car
    Response: {"sentiment": "positive"}
"""

from flask import Flask
from nltk.sentiment import SentimentIntensityAnalyzer
import json

# Initialize Flask app
app = Flask("Sentiment Analyzer")

# Initialize Sentiment Analyzer (VADER from NLTK)
sia = SentimentIntensityAnalyzer()


@app.get('/')
def home():
    """
    Root endpoint
    Returns a welcome message and usage instructions.
    """
    return "Welcome to the Sentiment Analyzer. \
    Use /analyze/text to get the sentiment"


@app.get('/analyze/<input_txt>')
def analyze_sentiment(input_txt):
    """
    Analyze sentiment of input text using VADER.

    Args:
        input_txt (str): The input text to analyze

    Returns:
        JSON: Sentiment classification as one of:
              {"sentiment": "positive"}
              {"sentiment": "negative"}
              {"sentiment": "neutral"}
    """
    # Get polarity scores from NLTK
    scores = sia.polarity_scores(input_txt)
    print(scores)

    # Extract sentiment scores
    pos = float(scores['pos'])
    neg = float(scores['neg'])
    neu = float(scores['neu'])

    # Determine dominant sentiment
    res = "positive"
    print("pos neg nue ", pos, neg, neu)
    if (neg > pos and neg > neu):
        res = "negative"
    elif (neu > neg and neu > pos):
        res = "neutral"

    # Format result as JSON string
    res = json.dumps({"sentiment": res})
    print(res)
    return res


if __name__ == "__main__":
    # Run Flask app in debug mode
    app.run(debug=True)