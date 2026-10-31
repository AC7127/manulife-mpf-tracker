
import os
import requests

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")

def send_nba_report(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    r = requests.post(url, json=payload)
    print(r.json())

if __name__ == "__main__":
    # 範例：你之後可以將 Meta AI 生成嘅速報內容寫入 report.md 再讀取
    with open("nba_daily_report.md", "r", encoding="utf-8") as f:
        report = f.read()
    
    # 加上雷霆重點標題
    final_text = f"🏀 *2026-27 NBA 雷霆重點速報*\n\n{report}"
    send_nba_report(final_text)
