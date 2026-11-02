import os
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

# ===== 詳細戰績榜 - 全繁體 =====
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
3. OKC Thunder 4-2 .667 GB1 H3-0 A1-2 L10 4-2 L2 | 西北組第2 6場4-2 66.7% L2 | 西岸第7
4. LA Lakers 5-2 .714 GB1 H3-1 A2-1 L10 5-2 W1 | 7場5-2 71.4% W1
5. Portland Trail Blazers 4-1 .800 GB1 H2-1 A2-0 L10 4-1 W1 | 5場4-1 80% W1
6. San Antonio Spurs 4-2 .667 GB1.5 H2-2 A2-0 L10 4-2 W1 | 6場4-2 66.7% W1
7. Golden State Warriors 4-3 .571 GB2 H1-1 A3-2 L10 4-3 W4 | 7場4-3 57.1%
8. Dallas Mavericks 4-2 .667 GB1.5 H2-1 A2-1 L10 4-2 W1 | 6場4-2 66.7% W1
9. Denver Nuggets 3-2 .600 GB2 H1-1 A2-1 L10 3-2 W1 | 5場3-2 60% W1
10. Minnesota Timberwolves 4-3 .571 GB2 H2-1 A2-2 L10 4-3 L1 | 7場4-3 57.1%
11. Phoenix Suns 2-3 .400 GB3 H1-0 A1-3 L10 2-3 L1 | 5場2-3 40% L1
12. LA Clippers 1-4 .200 GB4 H1-1 A0-3 L10 1-4 L1 | 5場1-4 20% L1
13. Utah Jazz 1-5 .167 GB4.5 H1-3 A0-2 L10 1-5 L4 | 6場1-5 16.7% L4
14. New Orleans Pelicans 2-4 .333 GB3.5 H2-2 A0-2 L10 2-4 W1 | 6場2-4 33.3% W1
15. Sacramento Kings 0-6 .000 GB5.5 H0-2 A0-4 L10 0-6 L6 | 6場0-6 0% L6
"""

NEWS = f"""
📰 *NBA 30隊詳細新聞報導 + 每日戰果* - {now_str}

📊 *昨日戰果 11/01-11/02*:
火箭 119-98 雷霆 (火箭6-0大勝) | 灰熊 136-105 國王 (灰熊6-0) | 拓荒者 112-90 爵士 | 76人 109-104 黃蜂 (Maxey 38分) | 鵜鶘 121-99 鷹隊 | 馬刺 121-111 灰狼 (Wemby 43分6阻攻) | 騎士 136-111 公鹿 | 賽爾提克 108-97 魔術 (綠軍5-1) | 籃網 98-90 溜馬 (籃網首勝) | 勇士 124-112 快艇 (新秀Lendeborg 37分) | 湖人 131-125 暴龍 (Doncic 45分15籃板)

⚡ *雷霆重點 4-2*:
• Jalen Williams 左腓骨骨折+腳踝脫臼手術成功賽季報銷25歲
• Cason Wallace 左肩盂唇撕裂待手術
• Chet Holmgren 右膝髕腱小撕裂生物治療缺席8-10週
• 已簽下 Ochai Agbaji，傳目標 Herb Jones / Trey Murphy III
• 昨日作客火箭大敗吞下2連敗，SGA 26分領軍

*東岸詳細*: 76人 Brown 左髕腱病變缺陣，Maxey得分王；鷹隊 Gueye 腳部骨折3-4個月，Veesaar ACL報銷，Daniels 3.0抄截領先聯盟；騎士 Tyson 右踝扭傷；尼克 Towns 13.8籃板；巫師 Young 61助攻領先；熱火 Giannis加盟後1-4掙扎；籃網1-5首勝。

*西岸詳細*: 火箭6-0無傷病，Jabari Smith 30分+Smart 24分大勝雷霆；灰熊6-0挑戰7連勝對鵜鶘；拓荒者 Morant 二級拉傷缺陣4週；爵士 Markkanen 右腕成疑；馬刺 Wembanyama 19阻攻聯盟第1場均3.8阻攻；灰狼 Edwards缺陣Gobert 12.2籃板；湖人 Doncic 36分領先得分榜5.2三分；鵜鶘 Zion 3.2抄截聯盟第1但1-4；國王 Sabonis 16.2籃板但0-6墊底；聯盟傷病潮108人84人缺陣。
"""

HOURLY = f"""
⚡ *NBA 每小時戰況更新* - {now_str}

• 雷霆: 4-2 .667 西北組第2 西岸第7 | 下場 Cavs vs Thunder 明早 08:00 HKT @ Rocket Arena | SGA 場均約26分領軍 | 昨日98-119大敗火箭吞2連敗
• 今晚焦點: Magic @ Celtics 已完 97-108，Nets @ Pacers 已完 98-90，Warriors @ Clippers 已完 124-112，Lakers @ Raptors 已完 131-125
• 明早焦點: 雷霆 @ 騎士 08:00 HKT 爭取止連敗

完整30隊詳細榜+詳細新聞 每日 09:30 HKT 推送
"""

def send_daily():
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
    print("Daily done - 全繁體")

def send_hourly():
    send_split(HOURLY, "每小時戰況")
    print("Hourly done - 全繁體")

if __name__ == "__main__":
    mode = os.getenv("NBA_MODE", "").lower()
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    is_daily_time = (now_hkt.hour == 9 and 25 <= now_hkt.minute <= 40)
    if mode == "daily" or arg == "daily" or is_daily_time:
        print(f"Mode: DAILY at {now_str} - 全繁體版")
        send_daily()
    else:
        print(f"Mode: HOURLY at {now_str} - 全繁體版")
        send_hourly()

