# -*- coding: utf-8 -*-
import os
import requests
from datetime import datetime


OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")


SYSTEM_PROMPT = """You are a concise financial assistant helping a long-term investor
start their day. You receive structured data about their stock portfolio and macro
environment. Your job is to:
1. Write a brief, friendly morning briefing in English (max 400 words total)
2. Flag anything that genuinely matters today (earnings soon, dividend ex-date near,
   relevant news, macro shift)
3. Skip stocks with nothing relevant - only mention what matters
4. Use simple Telegram Markdown: *bold* for stock names, no tables
5. End with a one-line macro snapshot
Keep it scannable. No fluff."""


def build_prompt(news, earnings, dividends, macro):
    today = datetime.utcnow().strftime("%A %d %B %Y")
    lines = ["Today is " + today + ". Here is the portfolio data:\n"]

    lines.append("## NEWS HEADLINES (last 24h)")
    for ticker, data in news.items():
        headlines = data.get("headlines", [])
        if headlines:
            lines.append("\n" + ticker + " (" + data["name"] + "):")
            for h in headlines:
                lines.append("  - " + h)
        else:
            lines.append("\n" + ticker + ": no headlines today")

    lines.append("\n## UPCOMING EARNINGS (next 30 days)")
    if earnings:
        for ticker, info in earnings.items():
            hour = info.get("hour", "")
            if hour == "bmo":
                hour = "before open"
            elif hour == "amc":
                hour = "after close"
            eps = ""
            if info.get("estimate_eps"):
                eps = " - EPS est: " + str(info["estimate_eps"])
            lines.append("  " + ticker + ": " + str(info["date"]) + " " + hour + eps)
    else:
        lines.append("  No earnings in the next 30 days for portfolio stocks.")

    lines.append("\n## UPCOMING DIVIDENDS (next 60 days)")
    if dividends:
        for ticker, info in dividends.items():
            lines.append(
                "  " + ticker + ": ex-date " + str(info["ex_date"]) +
                ", pay-date " + str(info["pay_date"]) +
                ", amount " + str(info.get("amount", "")) +
                " " + str(info.get("currency", ""))
            )
    else:
        lines.append("  No upcoming dividends found.")

    lines.append("\n## MACRO SNAPSHOT")
    lines.append("  EUR/USD: " + str(macro.get("eur_usd", "n/a")))
    lines.append("  US 10Y yield: " + str(macro.get("us_10y", "n/a")))
    lines.append("  S&P 500: " + str(macro.get("sp500", "n/a")))
    lines.append("  " + str(macro.get("fed_note", "")))
    lines.append("  " + str(macro.get("ecb_note", "")))

    return "\n".join(lines)


def call_llm(prompt):
    headers = {
        "Authorization": "Bearer " + OPENROUTER_KEY,
        "Content-Type": "application/json",
        "HTTP-Referer": "stock-agent",
    }
    body = {
        "model": OPENROUTER_MODEL,
        "max_tokens": 600,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body,
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    print("[agent] Response keys: " + str(list(data.keys())))

    choices = data.get("choices", [])
    if not choices:
        print("[agent] ERROR - full response: " + str(data))
        return "Error: no response from LLM."

    message = choices[0].get("message", {})
    content = message.get("content")

    if content is None:
        content = message.get("reasoning", "")

    if not content:
        print("[agent] ERROR - full response: " + str(data))
        return "Error: LLM returned empty content."

    return content.strip()


def run_agent(news, earnings, dividends, macro):
    prompt = build_prompt(news, earnings, dividends, macro)
    print("[agent] Prompt length: " + str(len(prompt.split())) + " words")
    summary = call_llm(prompt)
    return summary
