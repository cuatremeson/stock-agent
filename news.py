import os
import requests
from datetime import datetime, timedelta


NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/everything"


def _fetch_headlines(query: str, language: str, days_back: int = 1) -> list[str]:
    from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    params = {
        "q": query,
        "language": language,
        "from": from_date,
        "sortBy": "relevancy",
        "pageSize": 3,
        "apiKey": NEWSAPI_KEY,
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        articles = r.json().get("articles", [])
        return [a["title"] for a in articles if a.get("title")]
    except Exception as e:
        print(f"[news] Error fetching '{query}': {e}")
        return []


def fetch_news_for_portfolio(portfolio: list[dict]) -> dict:
    results = {}
    for stock in portfolio:
        ticker = stock["ticker"]
        name = stock["name"]
        lang = stock["lang"]

        # Spanish stocks: search by company name in Spanish
        # English stocks: search by ticker + company name
        if lang == "es":
            query = f'"{name}"'
        else:
            query = f'"{ticker}" OR "{name}"'

        headlines = _fetch_headlines(query, language=lang)
        results[ticker] = {
            "name": name,
            "lang": lang,
            "headlines": headlines,
        }
    return results
