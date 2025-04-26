import requests
import pandas as pd
from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

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
        return "Neutral"
    result = sentiment_pipeline(text[:512])[0]  # BERT models have 512 token limit
    label = result['label']
    if label == 'POSITIVE':
        return "Positive"
    elif label == 'NEGATIVE':
        return "Negative"
    else:
        return "Neutral"




