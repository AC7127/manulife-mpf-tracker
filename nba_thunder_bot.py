import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

STANDINGS_TEXT = """
🏀 *2026-27 NBA 完整30隊詳細戰績榜* - 截至 10/30

*東岸 Eastern Conference:*
1. Detroit Pistons 4-1 .800 W1
2. Philadelphia 76ers 4-1 .800 W1 | 6場5-1 83.3% W2
3. Boston Celtics 3-1 .750 W3 | 5場4-1 80% W4
4. Toronto Raptors 3-1 .750 W1 | 5場3-2 60% L1
5. Charlotte Hornets 3-2 .600 L1
6. Cleveland Cavaliers 3-2 .600 L1
7. Atlanta Hawks 3-3 .500 W1
8. New York Knicks 2-3 .400 W2
9. Washington Wizards 2-3 .400 L2
10. Indiana Pacers 2-3 .400 L2
11. Orlando Magic 1-3 .250 L1
12. Chicago Bulls 1-4 .200 L3
13. Milwaukee Bucks 1-4 .200 L1
14. Miami Heat 1-4 .200 W1
15. Brooklyn Nets 0-4 .000 L4 | 5場0-5 L5

*西岸 Western Conference:*
1. Houston Rockets 5-0 1.000 W5
2. Memphis Grizzlies 5-0 1.000 W5 | 5場5-0 100% W5
3. OKC Thunder 4-1 .800 L1 | 西北組第1 5場4-1 80% L1
4. LA Lakers 4-1 .800 W1 | 6場4-2 66.7% L1
5. Portland Trail Blazers 3-1 .750 L1 | 4場3-1 75% L1
6. San Antonio Spurs 3-2 .600 W3
7. Dallas Mavericks 3-2 .600 W2 | 6場4-2 66.7% W3
8. Minnesota Timberwolves 3-2 .600 L2 | 6場4-2 66.7% W1
9. Denver Nuggets 2-2 .500 W1 | 5場3-2 60% W2
10. Golden State Warriors 2-3 .400 W2 | 6場3-3 50% W3
11. Phoenix Suns 1-2 .333 L1 | 4場1-3 25% L2
12. LA Clippers 1-3 .250 L3 | 5場1-4 20% L4
13. Utah Jazz 1-4 .200 L3 | 5場1-4 20% L3
14. New Orleans Pelicans 1-4 .200 W1 | 5場1-4 20% W1
15. Sacramento Kings 0-5 .000 L5 | 5場0-5 L5
"""

def send_long(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing env")
        return
    parts = [text[i:i+MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    for idx, part in enumerate(parts):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": part, "parse_mode": "Markdown", "disable_web_page_preview": True}
        r = requests.post(url, json=payload)
        print(f"Part {idx+1}/{len(parts)} {r.status_code}")

if __name__ == "__main__":
    # 嘗試讀取每日報告
    extra = ""
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            extra = "\n\n" + f.read()
    except:
        extra = ""

    # 戰果
    results = """
📊 *昨日戰果 (10/30-31)*:
• Miami 145-125 Pacers
• Golden State 112-95 Lakers
• Denver 127-120 Suns
• Minnesota 127-101 Clippers
• Washington 95-79 Hornets
• Boston 125-111 Bulls
"""

    # 組合：戰果 + 完整榜 + 雷霆重點 + 30隊快訊
    final = f"🏀 *NBA 每日戰果+30隊完整排行榜 - 雷霆重點* - {datetime.now().strftime('%Y-%m-%d %H:%M HKT')}\n{results}\n{STANDINGS_TEXT}\n\n⚡ *雷霆重點*:\n• Jalen Williams 左小腿骨折+脫臼 賽季報銷\n• Cason Wallace 左肩盂唇撕裂\n• Chet Holmgren 右膝髕腱撕裂 8-10週\n• 已簽 Ochai Agbaji\n\n🔥 *30隊快訊*: Trail Blazers Morant缺4週, Cavs Tyson缺陣, Jazz Markkanen成疑{extra}"

    send_long(final)
