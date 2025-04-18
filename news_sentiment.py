import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def fetch_news(api_key, query="stock market", language="en", page_size=20):
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'language': language,
        'pageSize': page_size,
        'apiKey': api_key,
        'sortBy': 'publishedAt'
    }
    response = requests.get(url, params=params)
    data = response.json()
    articles = data.get("articles", [])
    return pd.DataFrame([{
        'title': article['title'],
        'description': article['description'],
        'publishedAt': article['publishedAt'],
        'source': article['source']['name'],
        'url': article['url']
    } for article in articles])

def analyze_sentiment(text):
    if not text:
        return 0
    score = analyzer.polarity_scores(text)
    return score['compound']




