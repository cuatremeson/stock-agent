# 📊 Stock Agent

AI-powered Telegram bot that delivers a daily morning briefing on your stock portfolio — news, earnings, dividends, and macro data, all summarized by an LLM.

## How It Works

Every morning at a scheduled time, the agent:

1. **Fetches news** headlines for each stock in your portfolio via [NewsAPI](https://newsapi.org/)
2. **Checks earnings calendar** (next 30 days) and **dividends** (next 60 days) via [Finnhub](https://finnhub.io/)
3. **Pulls macro data** — EUR/USD rate, US 10-Year Treasury yield, S&P 500 level
4. **Sends everything to an LLM** (via [OpenRouter](https://openrouter.ai/)) which produces a concise, scannable summary
5. **Delivers the briefing** to your Telegram chat

## Portfolio

The default portfolio includes stocks like Alphabet, Amazon, Meta, Novo Nordisk, Banco Santander, Telefónica, and others. Edit `config.py` to customize it with your own tickers.

## Tech Stack

- **Python 3.10+**
- **OpenRouter** — LLM inference (default model: `google/gemma-3-12b-it:free`)
- **NewsAPI** — news headlines
- **Finnhub** — earnings & dividend calendar
- **FRED API** — US 10-Year Treasury yield
- **Frankfurter API** — EUR/USD exchange rate
- **APScheduler** — cron-based scheduling
- **python-telegram-bot** — message delivery

## Project Structure

```
stock-agent/
├── main.py            # Entry point, scheduler setup
├── config.py          # Portfolio tickers & macro indicators
├── orchestrator.py    # LLM prompt builder & OpenRouter API call
├── news.py            # NewsAPI fetcher
├── events.py          # Finnhub earnings & dividends fetcher
├── macro.py           # Macro data fetcher (EUR/USD, 10Y, S&P 500)
├── sender.py          # Telegram message sender
├── .env.example       # Environment variables template
└── requirements.txt   # Python dependencies
```

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/cuatremeson/stock-agent.git
cd stock-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Fill in your `.env` file:

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (from [@BotFather](https://t.me/BotFather)) |
| `TELEGRAM_CHAT_ID` | Chat ID where briefings will be sent |
| `NEWSAPI_KEY` | Free API key from [newsapi.org](https://newsapi.org/) |
| `FINNHUB_KEY` | Free API key from [finnhub.io](https://finnhub.io/) |
| `OPENROUTER_KEY` | API key from [openrouter.ai](https://openrouter.ai/) |
| `OPENROUTER_MODEL` | LLM model to use (default: `google/gemma-3-12b-it:free`) |
| `RUN_HOUR` | Hour to run the briefing (24h format, Madrid timezone) |
| `RUN_MINUTE` | Minute to run the briefing |

### 4. Run

**Run once immediately:**

```bash
python main.py --now
```

**Run on schedule (default: 9:00 Madrid time):**

```bash
python main.py
```

## Customization

- **Change your portfolio** — edit the `PORTFOLIO` list in `config.py`
- **Change the schedule** — set `RUN_HOUR` and `RUN_MINUTE` in `.env`
- **Switch the LLM model** — change `OPENROUTER_MODEL` in `.env` to any model available on OpenRouter
- **Adjust the briefing style** — modify `SYSTEM_PROMPT` in `orchestrator.py`

## License

MIT
