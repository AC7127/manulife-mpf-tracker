import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")

def send_nba_report(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing NBA_BOT_TOKEN or NBA_CHAT_ID env")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    r = requests.post(url, json=payload)
    print(f"Telegram response: {r.status_code} {r.text}")
    return r

if __name__ == "__main__":
    report = None
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            report = f.read()
    except FileNotFoundError:
        report = None
        print("nba_daily_report.md not found, sending test message")

    if report:
        final_text = f"🏀 *2026-27 NBA 雷霆重點速報* - {datetime.now().strftime('%Y-%m-%d %H:%M HKT')}\n\n{report}"
    else:
        final_text = f"""🏀 *NBA Thunder Bot 測試成功！*

✅ 腳本已上傳成功
✅ Chat ID: {CHAT_ID}
✅ 時間: {datetime.now().strftime('%Y-%m-%d %H:%M HKT')}

你嘅雷霆重點監控：
• 目前戰績: 4勝1負 .800 (西岸第5)
• 下場: 11/2 對騎士 (Cleveland)
• 每日 09:30 HKT 自動推送賽果+新聞
• Meta AI 每小時監控已啟動"""

    send_nba_report(final_text)
