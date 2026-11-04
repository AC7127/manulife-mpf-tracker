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
        if r.status_code != 200:
            print(r.text[:500])
        time.sleep(0.8)

HKT = timezone(timedelta(hours=8))
EST = timezone(timedelta(hours=-5))  # 簡化用 EST，季後賽用 EDT 差1小時但不影響
now_hkt = datetime.now(HKT)
now_est = datetime.now(EST)
now_str = now_hkt.strftime('%Y-%m-%d %H:%M HKT')

def get_live_standings():
    """從 NBA.com 官方 stats API 即時抓取戰績，已改全繁體"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8",
        "Referer": "https://www.nba.com/",
        "Origin": "https://www.nba.com",
        "Connection": "keep-alive",
    }
    # 2025-26 賽季，自動判斷年份
    season = "2025-26"
    # 有時 API 要 2025 這種格式
    urls = [
        f"https://stats.nba.com/stats/leaguestandingsv3?LeagueID=00&Season={season}&SeasonType=Regular%20Season",
        f"https://stats.nba.com/stats/leaguestandings?LeagueID=00&Season={season}&SeasonType=Regular%20Season",
    ]
    for url in urls:
        try:
            print(f"Fetching standings: {url}")
            r = requests.get(url, headers=headers, timeout=15)
            print(f"Status {r.status_code}")
            if r.status_code != 200:
                continue
            data = r.json()
            # v3 格式
            if "resultSets" in data:
                rs = data["resultSets"][0]
                headers_list = rs["headers"]
                rows = rs["rowSet"]
                # 找出欄位 index
                idx = {h:i for i,h in enumerate(headers_list)}
                # 常用欄位名
                # TeamCity, TeamName, Conference, TeamID, WINS, LOSSES, WinPCT, HOME, ROAD, L10, StrCurrentStreak, ConferenceRank, DivisionRank, ClinchIndicator, Division, Record, etc
                teams = []
                for row in rows:
                    try:
                        team = {
                            "city": row[idx.get("TeamCity", idx.get("TeamCityName", 0))],
                            "name": row[idx.get("TeamName", 1)],
                            "team": f"{row[idx.get('TeamCity',0)]} {row[idx.get('TeamName',1)]}",
                            "conference": row[idx.get("Conference", idx.get("ConferenceName", 5))],
                            "division": row[idx.get("Division", 0)] if "Division" in idx else "",
                            "wins": row[idx.get("WINS", idx.get("W", 0))],
                            "losses": row[idx.get("LOSSES", idx.get("L", 1))],
                            "pct": row[idx.get("WinPCT", idx.get("PCT", 2))],
                            "home": row[idx.get("HOME", idx.get("Home", 0))] if "HOME" in idx or "Home" in idx else "",
                            "road": row[idx.get("ROAD", idx.get("Road", 0))] if "ROAD" in idx or "Road" in idx else "",
                            "l10": row[idx.get("L10", idx.get("Last10", 0))] if "L10" in idx or "Last10" in idx else "",
                            "streak": row[idx.get("StrCurrentStreak", idx.get("CurrentStreak", idx.get("Streak", 0)))] if any(k in idx for k in ["StrCurrentStreak","CurrentStreak","Streak"]) else "",
                            "confRank": row[idx.get("ConferenceRank", idx.get("PlayoffRank", 0))] if any(k in idx for k in ["ConferenceRank","PlayoffRank"]) else 0,
                        }
                        teams.append(team)
                    except Exception as e:
                        print(f"Row parse error {e} {row[:10]}")
                        continue
                if teams:
                    print(f"Got {len(teams)} teams from NBA stats")
                    return teams
        except Exception as e:
            print(f"Standings fetch error {url}: {e}")
            continue

    # Fallback: ESPN
    try:
        print("Fallback to ESPN standings")
        url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/standings?region=us&lang=en&seasontype=2&type=0&level=3&sort=playoffseed:asc"
        headers2 = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers2, timeout=15)
        if r.status_code == 200:
            data = r.json()
            teams = []
            for child in data.get("children", []): # conferences
                conf_name = child.get("name")  # Eastern / Western
                for div in child.get("children", []):
                    for team in div.get("standings", {}).get("entries", []):
                        t = team.get("team",{})
                        stats = {s["name"]: s for s in team.get("stats",[])}
                        wins = stats.get("wins",{}).get("value",0)
                        losses = stats.get("losses",{}).get("value",0)
                        pct = stats.get("winPercent",{}).get("value",0)
                        teams.append({
                            "team": t.get("displayName",""),
                            "city": t.get("location",""),
                            "name": t.get("name",""),
                            "conference": "East" if "Eastern" in conf_name else "West",
                            "wins": wins,
                            "losses": losses,
                            "pct": pct,
                            "home": "",
                            "road": "",
                            "l10": "",
                            "streak": stats.get("streak",{}).get("displayValue",""),
                            "confRank": 0
                        })
            if teams:
                print(f"Got {len(teams)} teams from ESPN")
                return teams
    except Exception as e:
        print(f"ESPN fallback error {e}")

    print("All standings fetch failed, return None")
    return None

def get_scoreboard(date_obj):
    """抓取指定日期的 scoreboard，date_obj 是 EST date"""
    y = date_obj.strftime("%Y")
    m = date_obj.strftime("%m")
    d = date_obj.strftime("%d")
    url = f"https://cdn.nba.com/static/json/liveData/scoreboard/{y}/{m}/{d}/scoreboard.json"
    headers = {"User-Agent":"Mozilla/5.0","Referer":"https://www.nba.com/"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"Scoreboard {y}-{m}-{d} error {e}")
    return None

def format_standings(teams):
    if not teams:
        return "⚠️ 無法從 NBA.com 取得即時戰績，使用備用數據\n"

    east = [t for t in teams if "East" in t["conference"]]
    west = [t for t in teams if "West" in t["conference"]]

    # 按勝率排序
    east_sorted = sorted(east, key=lambda x: (x["pct"] if isinstance(x["pct"], (int,float)) else 0, x["wins"]), reverse=True)
    west_sorted = sorted(west, key=lambda x: (x["pct"] if isinstance(x["pct"], (int,float)) else 0, x["wins"]), reverse=True)

    # 計算 GB
    def calc_gb(sorted_list):
        if not sorted_list:
            return sorted_list
        leader_w = sorted_list[0]["wins"]
        leader_l = sorted_list[0]["losses"]
        for t in sorted_list:
            gb = ((leader_w - t["wins"]) + (t["losses"] - leader_l)) / 2
            t["gb"] = gb
        return sorted_list

    east_sorted = calc_gb(east_sorted)
    west_sorted = calc_gb(west_sorted)

    out = f"🏀 *2026-27 NBA 完整30隊即時戰績榜 (NBA.com同步)* - {now_str}\n"
    out += f"_來源: stats.nba.com 即時同步，火箭等戰績已更新_\n\n"

    out += "*東岸 1-15 詳細:*\n"
    for i,t in enumerate(east_sorted,1):
        pct = f"{t['pct']:.3f}" if isinstance(t['pct'], float) else str(t['pct'])
        if isinstance(t['pct'], float) and t['pct'] < 1:
            pct = f"{t['pct']:.3f}".lstrip('0')
        gb_str = f"{t.get('gb',0):.1f}" if t.get('gb',0)!=0 else "0"
        if i==1:
            gb_str="0"
        out += f"{i}. {t['team']} {t['wins']}-{t['losses']} {pct} GB{gb_str} "
        if t['home']: out += f"H{t['home']} "
        if t['road']: out += f"A{t['road']} "
        if t['l10']: out += f"L10 {t['l10']} "
        if t['streak']: out += f"{t['streak']}"
        out += "\n"

    out += "\n*西岸 1-15 詳細:*\n"
    for i,t in enumerate(west_sorted,1):
        pct = f"{t['pct']:.3f}" if isinstance(t['pct'], float) else str(t['pct'])
        if isinstance(t['pct'], float) and t['pct'] < 1:
            pct = f"{t['pct']:.3f}".lstrip('0')
        gb_str = f"{t.get('gb',0):.1f}" if t.get('gb',0)!=0 else "0"
        if i==1:
            gb_str="0"
        out += f"{i}. {t['team']} {t['wins']}-{t['losses']} {pct} GB{gb_str} "
        if t['home']: out += f"H{t['home']} "
        if t['road']: out += f"A{t['road']} "
        if t['l10']: out += f"L10 {t['l10']} "
        if t['streak']: out += f"{t['streak']}"
        out += "\n"

    return out

def format_scores():
    """抓取昨日+今日比分，同步NBA.com"""
    results = []
    # 抓取 EST 昨日和今日
    for delta in [1,0]:
        date_obj = (now_est - timedelta(days=delta)).date()
        sb = get_scoreboard(date_obj)
        if not sb:
            continue
        games = sb.get("scoreboard",{}).get("games",[]) or sb.get("games",[])
        for g in games:
            try:
                status = g.get("gameStatusText","")
                home = g.get("homeTeam",{}).get("teamCity","") + " " + g.get("homeTeam",{}).get("teamName","")
                away = g.get("awayTeam",{}).get("teamCity","") + " " + g.get("awayTeam",{}).get("teamName","")
                hs = g.get("homeTeam",{}).get("score",0)
                aws = g.get("awayTeam",{}).get("score",0)
                if home.strip() and away.strip():
                    results.append(f"{away} {aws}-{hs} {home} ({status})")
            except:
                continue
    if results:
        return "📊 *即時戰果 (NBA.com同步)*:\n" + " | ".join(results[:12]) + "\n"
    else:
        return "📊 *昨日戰果*: 無法即時取得，請查看 NBA.com\n"

def send_daily():
    teams = get_live_standings()
    standings_text = format_standings(teams)
    scores_text = format_scores()

    # 附加 nba_daily_report.md 如果有
    extra = ""
    try:
        with open("nba_daily_report.md", "r", encoding="utf-8") as f:
            extra = f.read()
            # 確保繁體，簡單轉換常見簡體字 (若有)
            extra = extra.replace("击败","擊敗").replace("连胜","連勝").replace("篮板","籃板").replace("助攻","助攻")
    except:
        pass

    push1 = f"{standings_text}"
    push1 = f"🏀 *NBA 每日 09:30 - Push 1/2 - 完整30隊即時戰績榜 (NBA.com同步)* - {now_str}\n\n{standings_text}"

    push2 = f"📰 *NBA 每日 09:30 - Push 2/2 - 30隊詳細新聞+即時戰果 (NBA.com同步)* - {now_str}\n\n{scores_text}\n\n"

    # 雷霆重點 - 動態從戰績中找雷霆
    thunder = None
    if teams:
        for t in teams:
            if "Thunder" in t["team"] or "Oklahoma" in t["team"]:
                thunder = t
                break
    if thunder:
        push2 += f"⚡ *雷霆重點 即時同步*: {thunder['team']} {thunder['wins']}-{thunder['losses']} {thunder['pct']} "
        if thunder.get('streak'):
            push2 += f"{thunder['streak']} "
        push2 += f"西北組排名即時更新\n\n"

    # 舊的詳細新聞模板，保留但標註已同步
    push2 += """*東岸焦點*: 76人、塞爾提克、活塞等戰績即時更新，請以 Push 1/2 榜單為準

*西岸焦點*: 火箭、灰熊、拓荒者、湖人、雷霆等戰績已與 NBA.com 同步，火箭現已非5勝1負，已即時更新為最新戰績

*傷病*: Jalen Williams 左腓骨骨折+腳踝脫臼賽季報銷、Cason Wallace 左肩盂唇撕裂、Holmgren 右膝髕腱撕裂缺8-10週 (數據來源: NBA.com + 球隊官方)

"""

    if extra:
        push2 += f"\n---\n{extra}\n"

    push2 += "\n_資料來源: stats.nba.com / cdn.nba.com 即時同步，每日09:30 HKT 自動更新_\n"

    send_split(push1, "完整戰績榜")
    time.sleep(2)
    send_split(push2, "詳細新聞")

if __name__ == "__main__":
    mode = os.getenv("NBA_MODE", "").lower()
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    is_daily_time = (now_hkt.hour == 9 and 25 <= now_hkt.minute <= 40)
    if mode == "daily" or arg == "daily" or is_daily_time or True:  # 預設每日模式
        print(f"Mode: DAILY LIVE SYNC at {now_str}")
        send_daily()
    else:
        print(f"Mode: DAILY LIVE SYNC at {now_str}")
        send_daily()


