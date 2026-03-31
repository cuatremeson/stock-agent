import os
import requests
from datetime import datetime, timedelta


FINNHUB_KEY = os.getenv("FINNHUB_KEY")
BASE_URL = "https://finnhub.io/api/v1"


def _get(endpoint: str, params: dict) -> dict | list:
    params["token"] = FINNHUB_KEY
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[finnhub] Error {endpoint}: {e}")
        return {}


def fetch_earnings(tickers: list[str], days_ahead: int = 30) -> dict:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    future = (datetime.utcnow() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    data = _get("/calendar/earnings", {"from": today, "to": future})
    earnings_list = data.get("earningsCalendar", [])

    results = {}
    ticker_set = set(tickers)
    for item in earnings_list:
        sym = item.get("symbol")
        if sym in ticker_set:
            results[sym] = {
                "date": item.get("date"),
                "estimate_eps": item.get("epsEstimate"),
                "hour": item.get("hour", ""),
            }
    return results


def fetch_dividends(tickers: list[str], days_ahead: int = 60) -> dict:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    future = (datetime.utcnow() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    results = {}
    for ticker in tickers:
        data = _get("/stock/dividend", {"symbol": ticker, "from": today, "to": future})
        if isinstance(data, list) and data:
            next_div = data[0]
            results[ticker] = {
                "ex_date": next_div.get("exDate"),
                "pay_date": next_div.get("payDate"),
                "amount": next_div.get("amount"),
                "currency": next_div.get("currency", ""),
            }
    return results
