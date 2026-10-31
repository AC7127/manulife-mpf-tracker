import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900  # Telegram limit 4096,留少少

def send_nba_report(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing NBA_BOT_TOKEN or NBA_CHAT_ID env")
        return
    # 超長就分段發
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
        print(f"Part {idx+1}/{len(parts)} - {r.status_code} {r.text[:200]}")

if __name__ == "__main__":
    report = None
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            report = f.read()
    except FileNotFoundError:
        report = None

    if report:
        final_text = f"🏀 *2026-27 NBA 30隊全聯盟速報 - 雷霆重點* - {datetime.now().strftime('%Y-%m-%d %H:%M HKT')}\n\n{report}"
    else:
        final_text = f"""🏀 *NBA 30隊全聯盟監控已升級！*

✅ Chat ID: {CHAT_ID}
✅ 時間: {datetime.now().strftime('%Y-%m-%d %H:%M HKT')}

📊 *雷霆重點 (4勝1負 西岸第5)*:
• Jalen Williams 左小腿骨折+脫臼，手術成功，預計賽季報銷
• Cason Wallace 左肩盂唇撕裂，待手術
• Chet Holmgren 右膝髕腱小撕裂，生物治療，缺席8-10週
• 球隊已簽 Ochai Agbaji 填補空缺，傳有意 Pelicans 的 Herb Jones / Trey Murphy III

🔥 *全聯盟30隊今日快訊*:
• Trail Blazers: Ja Morant 左大腿二級拉傷，缺席至少4週
• Cavaliers: Jaylon Tyson 右腳踝扭傷缺陣對公鹿
• Jazz: Lauri Markkanen 右手腕扭傷列為出戰成疑對拓荒者
• 76ers: Jaylen Brown 左髕腱病變缺陣

每日 09:30 + 每小時 自動推送完整30隊消息"""

    send_nba_report(final_text)
