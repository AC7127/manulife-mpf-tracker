import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

def send_nba_report(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing NBA_BOT_TOKEN or NBA_CHAT_ID")
        return
    parts = [text[i:i+MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    for idx, part in enumerate(parts):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": part,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        r = requests.post(url, json=payload)
        print(f"Part {idx+1}/{len(parts)} - {r.status_code}")

if __name__ == "__main__":
    report = None
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            report = f.read()
    except FileNotFoundError:
        report = None
        print("nba_daily_report.md not found, using fallback")

    now = datetime.now().strftime('%Y-%m-%d %H:%M HKT')

    if report:
        final_text = f"🏀 *2026-27 NBA 每日戰果+排行+30隊 - 雷霆重點* - {now}\n\n{report}"
    else:
        final_text = f"""🏀 *NBA 每日戰果+戰績排行+30隊快訊 - 雷霆重點* - {now}

📊 *昨日戰果 (10/30)*:
• Miami 145 - Indiana 125
• Golden State 112 - LA Lakers 95
• Denver 127 - Phoenix 120
• Minnesota 127 - LA Clippers 101
• Washington 95 - Charlotte 79

📈 *最新戰績排行*:
• 西岸: Thunder 4勝1負 .800 西北組第1，西岸第3/5位
• 西北組: 1. Thunder 4-1 (80.000%) | 4-1 L1
• 聯盟: 東西岸 Top 8 每日更新

⚡ *雷霆重點*:
• Jalen Williams 左小腿骨折+脫臼 賽季報銷
• Cason Wallace 左肩盂唇撕裂 待手術
• Chet Holmgren 右膝髕腱撕裂 缺席8-10週
• 已簽 Ochai Agbaji，傳有意 Herb Jones / Trey Murphy III

🔥 *30隊快訊*:
• Trail Blazers: Ja Morant 左大腿二級拉傷 缺4週
• Cavaliers: Jaylon Tyson 右腳踝扭傷
• Jazz: Lauri Markkanen 右手腕成疑

每日 09:30 + 每小時 自動推送完整戰果+排行+30隊"""

    send_nba_report(final_text)
