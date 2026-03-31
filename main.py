import os
import traceback
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

load_dotenv()

from config import PORTFOLIO
from fetchers.news import fetch_news_for_portfolio
from fetchers.calendar import fetch_earnings, fetch_dividends
from fetchers.macro import fetch_macro
from agent.orchestrator import run_agent
from bot.sender import send_message, send_error_alert


def run_daily_briefing():
    print("[main] Starting daily briefing run...")
    try:
        tickers = [s["ticker"] for s in PORTFOLIO]

        print("[main] Fetching news...")
        news = fetch_news_for_portfolio(PORTFOLIO)

        print("[main] Fetching earnings calendar...")
        earnings = fetch_earnings(tickers)

        print("[main] Fetching dividends...")
        dividends = fetch_dividends(tickers)

        print("[main] Fetching macro data...")
        macro = fetch_macro()

        print("[main] Running LLM agent...")
        summary = run_agent(news, earnings, dividends, macro)

        header = "📊 *Morning Portfolio Briefing*\n\n"
        send_message(header + summary)
        print("[main] Done.")

    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"[main] ERROR:\n{error_msg}")
        send_error_alert(str(e))


if __name__ == "__main__":
    run_hour = int(os.getenv("RUN_HOUR", 9))
    run_minute = int(os.getenv("RUN_MINUTE", 0))

    # Run once immediately if you pass --now
    import sys
    if "--now" in sys.argv:
        print("[main] Running immediately (--now flag)...")
        run_daily_briefing()
    else:
        madrid = pytz.timezone("Europe/Madrid")
        scheduler = BlockingScheduler(timezone=madrid)
        scheduler.add_job(
            run_daily_briefing,
            trigger=CronTrigger(hour=run_hour, minute=run_minute, timezone=madrid),
        )
        print(f"[main] Scheduler started. Will run at {run_hour:02d}:{run_minute:02d} Madrid time.")
        print("[main] Press Ctrl+C to stop.")
        try:
            scheduler.start()
        except KeyboardInterrupt:
            print("[main] Stopped.")
