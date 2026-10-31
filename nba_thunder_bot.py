import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

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

STANDINGS = """
🏀 *2026-27 NBA 完整30隊詳細戰績榜* - 截至 10/30

*東岸*:
1. Detroit Pistons 4-1 .800 W1
2. Philadelphia 76ers 5-1 83.3% W2 | 4-1 .800
3. Boston Celtics 4-1 80% W4 | 3-1 .750
4. Toronto Raptors 3-2 60% L1 | 3-1 .750
5. Charlotte Hornets 3-2 .600
6. Cleveland Cavaliers 3-2 .600
7. Atlanta Hawks 3-3 .500 W1
8. New York Knicks 2-3 .400 W2
9-15. Wizards 2-3, Pacers 2-3, Magic 1-3, Bulls 1-4, Bucks 1-4, Heat 1-4, Nets 0-4

*西岸*:
1. Houston Rockets 5-0 1.000 W5
2. Memphis Grizzlies 5-0 1.000 W5
3. OKC Thunder 4-1 .800 L1 | 西北組第1 80% 
4. LA Lakers 4-2 66.7% L1 | 4-1 .800
5. Portland Trail Blazers 3-1 75% L1
6. San Antonio Spurs 3-2 60% W3
7-15. Mavericks 4-2, Timberwolves 4-2, Nuggets 3-2, Warriors 3-3, Suns 1-3, Clippers 1-4, Jazz 1-4, Pelicans 1-4, Kings 0-5
"""

DETAILED_NEWS = """
📰 *NBA 30隊詳細新聞報道 - 10/31*

*⚡ 雷霆重點*:
• Jalen Williams 左腓骨骨折+腳踝脫臼，週四手術成功，韌帶嚴重損傷，預計賽季報銷。25歲。
• Cason Wallace 左肩盂唇撕裂，待手術，精英外線防守者。
• Chet Holmgren 右膝髕腱小撕裂，週五接受生物治療，預計缺席8-10週，2個月以上。對上兩場已缺陣。
• 緊急簽入 Ochai Agbaji 填補名單空缺，之前效力 Jazz/Raptors/Nets。
• 傳有意 Pelicans 的 Herb Jones (防守大鎖) / Trey Murphy III (3D側翼) 作為交易目標，解決傷病危機。

*東岸*:
• 76ers: Jaylen Brown 左髕腱病變 (patellar tendinopathy) 膝頭痛，列為 doubtful 缺陣對 Knicks，今季由 Celtics 交易來。LeBron James 上場對 Knicks 20分9板8助攻關鍵補籃勝98-93，Anfernee Simons 獲更多機會。
• Hawks: Mouhamed Gueye 腳部骨折手術需3-4個月後再評估；Henri Veesaar 右膝前十字韌帶撕裂賽季報銷；Dyson Daniels 場均3.0抄截領先聯盟。
• Cavaliers: Jaylon Tyson 右腳踝扭傷缺陣對 Milwaukee；Meleek Thomas 腳部出戰成疑；Darius Garland 等輪休。
• Knicks: Karl-Anthony Towns 場均13.8板；剛敗給 76ers 93-98。
• Heat: 今夏交易來 Giannis Antetokounmpo，但開季掙扎1-4；Bam Adebayo 抄截11次。

*西岸*:
• Trail Blazers: Ja Morant (由 Grizzlies 交易來) 左大腿二級拉傷，MRI確認至少缺4週，上場對舊主 Grizzlies 103-124落敗時受傷；Robert Williams III 膝傷出戰成疑。
• Jazz: Lauri Markkanen 右手腕扭傷列為 questionable 對 Portland；Walker Kessler 上季阻攻表現。
• Rockets: Kevin Durant 主場對 Thunder焦點戰，5-0開局聯盟最佳；無大傷病。
• Grizzlies: 5-0 完美開局，今晚對 0-5 Kings 挑戰6-0。
• Spurs: Victor Wembanyama 阻攻19次聯盟第1，場均3.8火鍋；今晚主場對 Edwards 缺陣的 Timberwolves (Anthony Edwards 缺陣)。
• Timberwolves: Anthony Edwards 缺陣；Rudy Gobert 場均12.2板。
• Warriors: Stephen Curry 場均28.8分，Luka Dončić Lakers 場均36分領先得分榜，今晚對 Clippers。
• Lakers: Luka Dončić 三分21中，場均5.2三分；LeBron James 今季轉 76ers 後 Lakers 由 Doncic 領軍。
• Pelicans: Zion Williamson 場均3.2抄截聯盟第1，但球隊1-4掙扎。

*傷病潮統計*: 截至10/28，聯盟傷病名單108人，84人因傷病缺陣，Week 1 傷病潮嚴重。
"""

RESULTS = """
📊 *昨日戰果 (10/30-31)*:
• Miami 145-125 Pacers
• Golden State 112-95 Lakers
• Denver 127-120 Suns (Nuggets 127-120)
• Minnesota 127-101 Clippers
• Washington 95-79 Hornets
• Boston 125-111 Bulls
• Detroit 110-94 Nets
• Philadelphia 98-93 Knicks
• Orlando 121-114 Raptors
"""

if __name__ == "__main__":
    extra = ""
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            extra = "\n\n---\n" + f.read()
    except:
        pass

    now = datetime.now().strftime('%Y-%m-%d %H:%M HKT')
    full = f"🏀 *NBA 每日詳細報道 - 戰果+完整排行+30隊詳盡新聞 - 雷霆重點* - {now}\n{RESULTS}\n{STANDINGS}\n{DETAILED_NEWS}{extra}\n\n每日 09:30 + 每小時 自動推送"
    send_long(full)
