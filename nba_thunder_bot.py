import os
import requests
from datetime import datetime
import time

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

def send_split(text, title=""):
    """分段發送同一個大報告"""
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing env")
        return
    parts = [text[i:i+MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    for idx, part in enumerate(parts):
        # 每段加標題 (只有第一段顯示完整標題，其他顯示 續)
        if idx == 0:
            msg = part
        else:
            msg = f"{title} (續 {idx+1}/{len(parts)})\n\n" + part
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True}
        r = requests.post(url, json=payload)
        print(f"Push {title} Part {idx+1}/{len(parts)} {r.status_code}")
        time.sleep(0.8)  # 避免 Telegram 限速

# ========== Push 1: 完整30隊詳細戰績榜 ==========
STANDINGS_PUSH = """
🏀 *2026-27 NBA 完整30隊詳細戰績榜* - 截至 10/30

*東岸 Eastern Conference (1-15詳細):*
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

*西岸 Western Conference (1-15詳細):*
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

註: 第7-10名 Play-In，第11-15名 Out。雷霆西北組第1 西岸第3/5。
"""

# ========== Push 2: 30隊詳細新聞 + 戰果 ==========
NEWS_PUSH = """
📰 *NBA 30隊詳細新聞報道 + 每日戰果* - 10/31

📊 *昨日戰果 10/30-31*:
• Miami 145-125 Pacers
• Golden State 112-95 Lakers
• Denver 127-120 Suns
• Minnesota 127-101 Clippers
• Washington 95-79 Hornets
• Boston 125-111 Bulls
• Detroit 110-94 Nets
• Philadelphia 98-93 Knicks
• Orlando 121-114 Raptors
• Dallas 116-111 Rockets

⚡ *雷霆重點 (4-1)*:
• Jalen Williams 左腓骨骨折+腳踝脫臼，週四手術成功，韌帶嚴重損傷，預計賽季報銷，25歲。
• Cason Wallace 左肩盂唇撕裂，待手術，精英外線防守者。
• Chet Holmgren 右膝髕腱小撕裂，週五生物治療，缺8-10週，2個月以上，對上兩場已缺陣。
• 緊急簽入 Ochai Agbaji 填補名單空缺，之前效力 Jazz/Raptors/Nets。
• 傳有意 Pelicans 的 Herb Jones (防守大鎖) / Trey Murphy III (3D側翼) 作為交易目標，解決傷病危機。

*東岸詳細新聞*:
• 76ers: Jaylen Brown 左髕腱病變 (patellar tendinopathy) 膝頭痛，doubtful 缺陣對 Knicks，今季由 Celtics 交易來。LeBron James 上場20分9板8助關鍵補籃勝 Knicks 98-93，Anfernee Simons 獲更多機會。
• Celtics: 3-1 .750，W4，Tatum/Brown 分開後重建。
• Hawks: Mouhamed Gueye 腳部骨折手術需3-4個月後再評估；Henri Veesaar 右膝ACL撕裂賽季報銷；Dyson Daniels 場均3.0抄截領先聯盟，Trae Young 轉 Wizards 後由 Johnson 領軍。
• Cavaliers: Jaylon Tyson 右腳踝扭傷缺陣對 Milwaukee；Meleek Thomas 腳部出戰成疑。
• Knicks: Karl-Anthony Towns 場均13.8板；剛敗給76ers 93-98。
• Wizards: Trae Young 61助攻領先；3-3 .500。
• Pacers: Haliburton 場均9.5助攻。
• Magic: 1-3掙扎。
• Bulls: Josh Giddey 40助攻；1-4。
• Bucks: Myles Turner 13阻攻；1-4。
• Heat: 今夏交易來 Giannis Antetokounmpo，但開季1-4掙扎，Bam Adebayo 11抄截。
• Nets: 0-4全敗，0-5 L5。

*西岸詳細新聞*:
• Rockets: Kevin Durant 主場對 Thunder焦點戰，5-0開局聯盟最佳無大傷病，Houston 5-0 W5。
• Grizzlies: 5-0完美開局，今晚對0-5 Kings挑戰6-0，Ja Morant 已轉 Blazers。
• Blazers: Ja Morant (由 Grizzlies 交易來) 左大腿二級拉傷，MRI確認至少缺4週，上場對舊主103-124落敗時受傷；Robert Williams III 膝傷成疑；Toumani Camara 場均4.0三分。
• Lakers: Luka Dončić 場均36分領先得分榜，三分21中場均5.2三分，144分總分第2；LeBron轉76ers後由Doncic領軍。
• Spurs: Victor Wembanyama 19阻攻聯盟第1，場均3.8火鍋，今晚主場對 Edwards 缺陣的 Timberwolves。
• Timberwolves: Anthony Edwards 缺陣；Rudy Gobert 場均12.2板；Edwards 場均33.3分第2。
• Mavericks: Luka已轉湖人，Cooper Flagg 場均2.8抄截；6場4-2 66.7% W3。
• Nuggets: Jokić 場均9.0助攻；Jamal Murray 場均4.0三分。
• Warriors: Stephen Curry 場均28.8分第3；今晚對 Clippers。
• Suns: 1-3 25%掙扎 L2。
• Clippers: Kris Dunn 2.8抄截；1-4 L4。
• Jazz: Lauri Markkanen 右手腕扭傷列questionable對 Portland；Walker Kessler 12阻攻；1-4 L3。
• Pelicans: Zion Williamson 場均3.2抄截聯盟第1，16抄截領先，但球隊1-4 W1；1-4掙扎。
• Kings: Domantas Sabonis 81板16.2板領先聯盟，但球隊0-5全敗L5。

傷病潮統計: 截至10/28，聯盟傷病名單108人，84人因傷病缺陣，Week 1 傷病潮嚴重。
"""

if __name__ == "__main__":
    now = datetime.now().strftime('%Y-%m-%d %H:%M HKT')
    # 額外每日報告 (由 Meta AI 生成的 md)
    extra = ""
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            extra = "\n\n---\n" + f.read()
    except:
        pass

    # Push 1: 戰績榜 (分開第一次推送)
    push1_text = f"🏀 *NBA Push 1/2 - 完整30隊詳細戰績榜 (7-15詳細)* - {now}\n{STANDINGS_PUSH}"
    send_split(push1_text, "完整戰績榜")

    time.sleep(2)  # 兩次推送之間隔2秒

    # Push 2: 詳細新聞+戰果 (分開第二次推送)
    push2_text = f"📰 *NBA Push 2/2 - 30隊詳細新聞報道+戰果 - 雷霆重點* - {now}\n{NEWS_PUSH}{extra}\n\n✅ 每日 09:30 + 每小時 自動分兩次推送"
    send_split(push2_text, "詳細新聞")

    print("Done 2 pushes")
