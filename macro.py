import requests


def _safe_get(url: str, timeout: int = 8) -> dict:
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[macro] Error fetching {url}: {e}")
        return {}


def fetch_eurusd() -> str | None:
    data = _safe_get("https://api.frankfurter.app/latest?from=EUR&to=USD")
    rate = data.get("rates", {}).get("USD")
    return f"{rate:.4f}" if rate else None


def fetch_us10y_yield() -> str | None:
    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        "?series_id=DGS10&api_key=4a9bae9e7a8a62de6b1d73c23c4c3f5a"
        "&sort_order=desc&limit=1&file_type=json"
    )
    data = _safe_get(url)
    obs = data.get("observations", [])
    if obs:
        val = obs[0].get("value", ".")
        if val != ".":
            return f"{float(val):.2f}%"
    return None


def fetch_sp500() -> str | None:
    data = _safe_get(
        "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1d"
    )
    try:
        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return f"{price:,.2f}"
    except Exception:
        return None


def fetch_macro() -> dict:
    return {
        "eur_usd": fetch_eurusd(),
        "us_10y": fetch_us10y_yield(),
        "sp500": fetch_sp500(),
        "fed_note": "Next FOMC: check federalreserve.gov/monetarypolicy/fomccalendars.htm",
        "ecb_note": "Next ECB: check ecb.europa.eu/press/calendars",
    }
