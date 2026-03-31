PORTFOLIO = [
    {"ticker": "GOOGL", "name": "Alphabet",       "lang": "en"},
    {"ticker": "AMZN",  "name": "Amazon",          "lang": "en"},
    {"ticker": "SAN",   "name": "Banco Santander", "lang": "es"},
    {"ticker": "CPRT",  "name": "Copart",          "lang": "en"},
    {"ticker": "DGE",   "name": "Diageo",          "lang": "en"},
    {"ticker": "FTNT",  "name": "Fortinet",        "lang": "en"},
    {"ticker": "IDR",   "name": "Indra Sistemas",  "lang": "es"},
    {"ticker": "KHC",   "name": "Kraft Heinz",     "lang": "en"},
    {"ticker": "META",  "name": "Meta Platforms",  "lang": "en"},
    {"ticker": "NOV",   "name": "Novo Nordisk",    "lang": "en"},
    {"ticker": "RHI",   "name": "Robert Half",     "lang": "en"},
    {"ticker": "SPGI",  "name": "S&P Global",      "lang": "en"},
    {"ticker": "TEF",   "name": "Telefonica",      "lang": "es"},
    {"ticker": "ZTS",   "name": "Zoetis",          "lang": "en"},
]

SPANISH_TICKERS = [s["ticker"] for s in PORTFOLIO if s["lang"] == "es"]

MACRO_INDICATORS = [
    "EUR/USD exchange rate",
    "US 10-year Treasury yield",
    "S&P 500 index level",
    "Next Fed meeting date",
    "Next ECB meeting date",
]
