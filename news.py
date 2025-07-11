import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

API_KEY = ""
NEWS_URL = "https://newsapi.org/v2/everything"

def get_news(ticker):
    params = {
        "q": ticker,
        "sortBy": "publishedAt",
        "language" : "en",
        "apiKey": API_KEY
    }
    response = requests.get(NEWS_URL, params=params)
    data = response.json()
    analyzer = SentimentIntensityAnalyzer()
    results = []

    for article in data.get("articles", [])[:5]:
        title = article['title']
        url = article['url']
        published = article['publishedAt']
        score = analyzer.polarity_scores(title)['compound']
        results.append({
            "title": title,
            "url": url,
            "published": datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y %H:%M"),
            "sentiment": score
        })

    return results
