import sys
import requests
from datetime import datetime, timezone, timedelta
import time

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

def send_split(text, title=""):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing NBA_BOT_TOKEN or NBA_CHAT_ID")
        return
    parts = [text[i:i+MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    for idx, part in enumerate(parts):
        msg = part if idx == 0 else f"{title} (續 {idx+1}/{len(parts)})\n\n" + part
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True}
        r = requests.post(url, json=payload)
        print(f"{title} Part {idx+1}/{len(parts)} {r.status_code}")
        time.sleep(0.8)

HKT = timezone(timedelta(hours=8))
now_hkt = datetime.now(HKT)
now_str = now_hkt.strftime('%Y-%m-%d %H:%M HKT')

# ===== 詳細戰績榜 =====
STANDINGS = f"""
🏀 *2026-27 NBA 完整30隊詳細戰績榜 (7-15詳細)* - {now_str}

*東岸 1-15詳細:*
1. Detroit Pistons 4-1 .800 GB0 H2-0 A2-1 L10 4-1 W1
2. Philadelphia 76ers 4-1 .800 GB0 H2-1 A2-0 L10 4-1 W1 | 大西洋第1 6場5-1 83.3% W2
3. Boston Celtics 3-1 .750 GB0.5 H3-0 A0-1 L10 3-1 W3 | 5場4-1 80% W4
4. Toronto Raptors 3-1 .750 GB0.5 H2-0 A1-1 L10 3-1 W1 | 5場3-2 60% L1
5. Charlotte Hornets 3-2 .600 GB1 H2-1 A1-1 L10 3-2 L1
6. Cleveland Cavaliers 3-2 .600 GB1 H3-0 A0-2 L10 3-2 L1
7. Atlanta Hawks 3-3 .500 GB1.5 H1-2 A2-1 L10 3-3 W1
8. New York Knicks 2-3 .400 GB2 H1-2 A1-1 L10 2-3 W2
9. Washington Wizards 2-3 .400 GB2 H1-1 A1-2 L10 2-3 L2 | 6場3-3 50% W1
10. Indiana Pacers 2-3 .400 GB2 H0-2 A2-1 L10 2-3 L2 | 6場2-4 33.3% L3
11. Orlando Magic 1-3 .250 GB2.5 H0-2 A1-1 L10 1-3 L1 | 5場2-3 40% W1
12. Chicago Bulls 1-4 .200 GB3 H0-2 A1-2 L10 1-4 L3 | 6場1-5 16.7% L4
13. Milwaukee Bucks 1-4 .200 GB3 H1-2 A0-2 L10 1-4 L1 | 5場1-4 20% L1
14. Miami Heat 1-4 .200 GB3 H0-3 A1-1 L10 1-4 W1 | 6場2-4 33.3% W2
15. Brooklyn Nets 0-4 .000 GB3.5 H0-2 A0-2 L10 0-4 L4 | 5場0-5 0% L5

*西岸 1-15詳細:*
1. Houston Rockets 5-0 1.000 GB0 H2-0 A3-0 L10 5-0 W5
2. Memphis Grizzlies 5-0 1.000 GB0 H1-0 A4-0 L10 5-0 W5 | 西南第1 5場5-0 100% W5
3. OKC Thunder 4-1 .800 GB1 H3-0 A1-1 L10 4-1 L1 | 西北組第1 5場4-1 80% L1 | 西岸第3
4. LA Lakers 4-1 .800 GB1 H2-1 A2-0 L10 4-1 W1 | 6場4-2 66.7% L1
5. Portland Trail Blazers 3-1 .750 GB1.5 H1-1 A2-0 L10 3-1 L1 | 4場3-1 75% L1
6. San Antonio Spurs 3-2 .600 GB2 H1-2 A2-0 L10 3-2 W3 | 5場3-2 60% W3
7. Dallas Mavericks 3-2 .600 GB2 H1-1 A2-1 L10 3-2 W2 | 6場4-2 66.7% W3
8. Minnesota Timberwolves 3-2 .600 GB2 H1-1 A2-1 L10 3-2 L2 | 6場4-2 66.7% W1
9. Denver Nuggets 2-2 .500 GB2.5 H1-1 A1-1 L10 2-2 W1 | 5場3-2 60% W2
10. Golden State Warriors 2-3 .400 GB3 H0-1 A2-2 L10 2-3 W2 | 6場3-3 50% W3
11. Phoenix Suns 1-2 .333 GB3 H1-0 A0-2 L10 1-2 L1 | 4場1-3 25% L2
12. LA Clippers 1-3 .250 GB3.5 H1-1 A0-2 L10 1-3 L3 | 5場1-4 20% L4
13. Utah Jazz 1-4 .200 GB4 H1-3 A0-1 L10 1-4 L3 | 5場1-4 20% L3
14. New Orleans Pelicans 1-4 .200 GB4 H1-2 A0-2 L10 1-4 W1 | 5場1-4 20% W1
15. Sacramento Kings 0-5 .000 GB5 H0-2 A0-3 L10 0-5 L5 | 5場0-5 0% L5
"""

NEWS = f"""
📰 *NBA 30隊詳細新聞報道 + 每日戰果* - {now_str}

📊 *昨日戰果 10/30-31*:
Miami 145-125 Pacers | GSW 112-95 Lakers | Denver 127-120 Suns | Minnesota 127-101 Clippers | Washington 95-79 Hornets | Boston 125-111 Bulls | Detroit 110-94 Nets | 76ers 98-93 Knicks (LeBron 20/9/8) | Magic 121-114 Raptors | Dallas 116-111 Rockets | Jazz vs Blazers Live

⚡ *雷霆重點 4-1*:
• Jalen Williams 左腓骨骨折+脫臼手術成功賽季報銷25歲
• Cason Wallace 左肩盂唇撕裂待手術
• Chet Holmgren 右膝髕腱小撕裂生物治療缺8-10週
• 已簽 Ochai Agbaji，傳目標 Herb Jones / Trey Murphy III

*東岸詳細*: 76ers Brown 左髕腱病變缺陣；Hawks Gueye 腳骨折3-4月，Veesaar ACL報銷，Daniels 3.0抄截領先；Cavs Tyson 右踝扭傷；Knicks Towns 13.8板；Wizards Young 61助攻領先；Heat Giannis加盟後1-4；Nets 0-4。

*西岸詳細*: Rockets 5-0無傷；Grizzlies 5-0挑戰6-0對Kings；Blazers Morant 二級拉傷缺4週；Jazz Markkanen 右腕成疑；Spurs Wembanyama 19阻攻聯盟第1場均3.8；Wolves Edwards缺陣Gobert 12.2板；Lakers Doncic 36分領先5.2三分；Pelicans Zion 3.2抄截第1但1-4；Kings Sabonis 16.2板但0-5；傷病潮108人84人缺陣。
"""

HOURLY = f"""
⚡ *NBA 每小時戰況更新* - {now_str}

• 雷霆: 4-1 .800 西北組第1 西岸第3 | 下場 Rockets vs Thunder 今日 08:30 HKT @ Toyota Center | SGA 場均約26分領軍 | 暫無進行中，賽前準備
• 今早7場: Jazz vs Blazers Live, Hornets vs 76ers 06:00, Pelicans vs Hawks 07:00, Grizzlies vs Kings 08:00, Bucks vs Cavs 08:00, Spurs vs Wolves 08:00, Rockets vs Thunder 08:30
• 昨日最終: GSW 112-95 Lakers, Denver 127-120 Suns, Dallas 116-111 Rockets, Miami 145-125 Pacers等

完整30隊詳細榜+詳細新聞 每日 09:30 HKT 推送
"""

def send_daily():
    # Requirement 1: 每日 0930 詳細戰績榜+詳細新聞 (分兩次)
    push1 = f"🏀 *NBA 每日 09:30 - Push 1/2 - 完整30隊詳細戰績榜 (7-15詳細)* - {now_str}\n{STANDINGS}"
    send_split(push1, "完整戰績榜")
    time.sleep(2)
    push2 = f"📰 *NBA 每日 09:30 - Push 2/2 - 30隊詳細新聞+戰果* - {now_str}\n{NEWS}"
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            push2 += "\n\n---\n" + f.read()
    except:
        pass
    send_split(push2, "詳細新聞")
    print("Daily done")

def send_hourly():
    # Requirement 2: 每小時 每場戰況更新
    send_split(HOURLY, "每小時戰況")
    print("Hourly done")

if __name__ == "__main__":
    mode = os.getenv("NBA_MODE", "").lower()  # daily / hourly
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else ""

    # 判斷: 如果係 09:30 HKT 或 mode=daily 就推詳細榜+新聞，否則推每小時戰況
    is_daily_time = (now_hkt.hour == 9 and 25 <= now_hkt.minute <= 40)

    if mode == "daily" or arg == "daily" or is_daily_time:
        print(f"Mode: DAILY at {now_str}")
        send_daily()
    else:
        print(f"Mode: HOURLY at {now_str}")
        send_hourly()

