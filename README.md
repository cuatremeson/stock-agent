📊 Stock Agent
AI-powered Telegram bot that delivers a daily morning briefing on your stock portfolio — news, earnings, dividends, and macro data, all summarized by an LLM.
How It Works
Every morning at a scheduled time, the agent:

Fetches news headlines for each stock in your portfolio via NewsAPI
Checks earnings calendar (next 30 days) and dividends (next 60 days) via Finnhub
Pulls macro data — EUR/USD rate, US 10-Year Treasury yield, S&P 500 level
Sends everything to an LLM (via OpenRouter) which produces a concise, scannable summary
Delivers the briefing to your Telegram chat

Portfolio
The default portfolio includes stocks like Alphabet, Amazon, Meta, Novo Nordisk, Banco Santander, Telefónica, and others. Edit config.py to customize it with your own tickers.
Tech Stack

Python 3.10+
OpenRouter — LLM inference (default model: google/gemma-3-12b-it:free)
NewsAPI — news headlines
Finnhub — earnings & dividend calendar
FRED API — US 10-Year Treasury yield
Frankfurter API — EUR/USD exchange rate
APScheduler — cron-based scheduling
python-telegram-bot — message delivery

Project Structure
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
Quick Start
1. Clone the repo
bashgit clone https://github.com/cuatremeson/stock-agent.git
cd stock-agent
2. Install dependencies
bashpip install -r requirements.txt
3. Set up environment variables
bashcp .env.example .env
Fill in your .env file:
VariableDescriptionTELEGRAM_BOT_TOKENYour Telegram bot token (from @BotFather)TELEGRAM_CHAT_IDChat ID where briefings will be sentNEWSAPI_KEYFree API key from newsapi.orgFINNHUB_KEYFree API key from finnhub.ioOPENROUTER_KEYAPI key from openrouter.aiOPENROUTER_MODELLLM model to use (default: google/gemma-3-12b-it:free)RUN_HOURHour to run the briefing (24h format, Madrid timezone)RUN_MINUTEMinute to run the briefing
4. Run
Run once immediately:
bashpython main.py --now
Run on schedule (default: 9:00 Madrid time):
bashpython main.py
Customization

Change your portfolio — edit the PORTFOLIO list in config.py
Change the schedule — set RUN_HOUR and RUN_MINUTE in .env
Switch the LLM model — change OPENROUTER_MODEL in .env to any model available on OpenRouter
Adjust the briefing style — modify SYSTEM_PROMPT in orchestrator.py

License
MIT
