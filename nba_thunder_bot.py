import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

STANDINGS = """
🏀 *2026-27 NBA 完整30隊詳細戰績榜* - 截至 10/30

*東岸 Eastern Conference (詳細):*
1. Detroit Pistons 4-1 .800 GB0 Home2-0 Away2-1 L10 4-1 W1
2. Philadelphia 76ers 4-1 .800 GB0 Home2-1 Away2-0 L10 4-1 W1 | 大西洋第1 6場5-1 83.3% W2
3. Boston Celtics 3-1 .750 GB0.5 Home3-0 Away0-1 L10 3-1 W3 | 5場4-1 80% W4
4. Toronto Raptors 3-1 .750 GB0.5 Home2-0 Away1-1 L10 3-1 W1 | 5場3-2 60% L1
5. Charlotte Hornets 3-2 .600 GB1 Home2-1 Away1-1 L10 3-2 L1
6. Cleveland Cavaliers 3-2 .600 GB1 Home3-0 Away0-2 L10 3-2 L1
7. Atlanta Hawks 3-3 .500 GB1.5 Home1-2 Away2-1 L10 3-3 W1
8. New York Knicks 2-3 .400 GB2 Home1-2 Away1-1 L10 2-3 W2
9. Washington Wizards 2-3 .400 GB2 Home1-1 Away1-2 L10 2-3 L2 | 6場3-3 50% W1
10. Indiana Pacers 2-3 .400 GB2 Home0-2 Away2-1 L10 2-3 L2 | 6場2-4 33.3% L3
11. Orlando Magic 1-3 .250 GB2.5 Home0-2 Away1-1 L10 1-3 L1 | 5場2-3 40% W1
12. Chicago Bulls 1-4 .200 GB3 Home0-2 Away1-2 L10 1-4 L3 | 6場1-5 16.7% L4
13. Milwaukee Bucks 1-4 .200 GB3 Home1-2 Away0-2 L10 1-4 L1 | 5場1-4 20% L1
14. Miami Heat 1-4 .200 GB3 Home0-3 Away1-1 L10 1-4 W1 | 6場2-4 33.3% W2
15. Brooklyn Nets 0-4 .000 GB3.5 Home0-2 Away0-2 L10 0-4 L4 | 5場0-5 0% L5

*西岸 Western Conference (詳細):*
1. Houston Rockets 5-0 1.000 GB0 Home2-0 Away3-0 L10 5-0 W5
2. Memphis Grizzlies 5-0 1.000 GB0 Home1-0 Away4-0 L10 5-0 W5 | 西南第1 5場5-0 100% W5
3. OKC Thunder 4-1 .800 GB1 Home3-0 Away1-1 L10 4-1 L1 | 西北組第1 5場4-1 80% L1 | 西岸第3
4. LA Lakers 4-1 .800 GB1 Home2-1 Away2-0 L10 4-1 W1 | 6場4-2 66.7% L1
5. Portland Trail Blazers 3-1 .750 GB1.5 Home1-1 Away2-0 L10 3-1 L1 | 4場3-1 75% L1
6. San Antonio Spurs 3-2 .600 GB2 Home1-2 Away2-0 L10 3-2 W3 | 5場3-2 60% W3
7. Dallas Mavericks 3-2 .600 GB2 Home1-1 Away2-1 L10 3-2 W2 | 6場4-2 66.7% W3
8. Minnesota Timberwolves 3-2 .600 GB2 Home1-1 Away2-1 L10 3-2 L2 | 6場4-2 66.7% W1
9. Denver Nuggets 2-2 .500 GB2.5 Home1-1 Away1-1 L10 2-2 W1 | 5場3-2 60% W2
10. Golden State Warriors 2-3 .400 GB3 Home0-1 Away2-2 L10 2-3 W2 | 6場3-3 50% W3
11. Phoenix Suns 1-2 .333 GB3 Home1-0 Away0-2 L10 1-2 L1 | 4場1-3 25% L2
12. LA Clippers 1-3 .250 GB3.5 Home1-1 Away0-2 L10 1-3 L3 | 5場1-4 20% L4
13. Utah Jazz 1-4 .200 GB4 Home1-3 Away0-1 L10 1-4 L3 | 5場1-4 20% L3
14. New Orleans Pelicans 1-4 .200 GB4 Home1-2 Away0-2 L10 1-4 W1 | 5場1-4 20% W1
15. Sacramento Kings 0-5 .000 GB5 Home0-2 Away0-3 L10 0-5 L5 | 5場0-5 0% L5

註: 第7-10名 Play-In，第11-15名 Out，雷霆西北組第1 西岸第3。
"""

DETAILED_NEWS = """
📰 *NBA 30隊詳細新聞 - 10/31*

⚡ 雷霆: Jalen Williams 左小腿骨折+脫臼手術成功賽季報銷25歲；Cason Wallace 左肩盂唇撕裂待手術；Chet Holmgren 右膝髕腱小撕裂生物治療缺8-10週；已簽 Ochai Agbaji；傳目標 Herb Jones / Trey Murphy III。
東岸: 76ers Brown 左髕腱病變缺陣，LeBron 20分9板8助勝Knicks 98-93；Hawks Gueye 腳骨折3-4月，Veesaar ACL報銷，Daniels 場均3.0抄截領先；Cavs Tyson 右踝扭傷缺陣對Bucks，Thomas 腳成疑；Knicks Towns 13.8板；Heat Giannis加盟後1-4掙扎。
西岸: Blazers Morant 左大腿二級拉傷缺4週；Jazz Markkanen 右腕成疑；Rockets 5-0 領先；Grizzlies 5-0 挑戰6-0對Kings；Spurs Wembanyama 19阻攻聯盟第1場均3.8；Wolves Edwards缺陣Gobert 12.2板；Warriors Curry 28.8分，Lakers Doncic 36分領先得分榜5.2三分；Pelicans Zion 3.2抄截第1但1-4；傷病潮108人上榜84人缺陣。
"""

RESULTS = """
📊 *昨日戰果 10/30-31*:
Miami 145-125 Pacers | GSW 112-95 Lakers | Denver 127-120 Suns | Minnesota 127-101 Clippers | Washington 95-79 Hornets | Boston 125-111 Bulls | Detroit 110-94 Nets | 76ers 98-93 Knicks | Magic 121-114 Raptors
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
        print(f"Part {idx+1}/{len(parts)} {r.status_code} {r.text[:100]}")

if __name__ == "__main__":
    extra = ""
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            extra = "\n\n---\n" + f.read()
    except:
        pass
    now = datetime.now().strftime('%Y-%m-%d %H:%M HKT')
    full = f"🏀 *NBA 每日詳細報道 - 完整30隊戰績(7-15詳細)+新聞* - {now}\n{RESULTS}\n{STANDINGS}\n{DETAILED_NEWS}{extra}"
    send_long(full)
