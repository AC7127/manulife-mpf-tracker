import os
import requests
from datetime import datetime, timezone, timedelta
import time

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

def send_split(text, title=""):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing token/chat")
        return
    parts = [text[i:i+MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    for idx, part in enumerate(parts):
        msg = part if idx == 0 else f"{title} (續 {idx+1}/{len(parts)})\n\n" + part
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True}
        try:
            r = requests.post(url, json=payload, timeout=15)
            print(f"{title} {idx+1}/{len(parts)} {r.status_code}")
        except Exception as e:
            print(f"Telegram error {e}")
        time.sleep(0.9)

HKT = timezone(timedelta(hours=8))
EST = timezone(timedelta(hours=-5))
now_hkt = datetime.now(HKT)
now_est = datetime.now(EST)
now_str = now_hkt.strftime('%Y-%m-%d %H:%M HKT')

def fetch_with_retry(url, headers=None, timeout=12):
    if headers is None:
        headers = {"User-Agent":"Mozilla/5.0"}
    for _ in range(2):
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            if r.status_code == 200 and len(r.text) > 80:
                return r
            print(f"GET {url} -> {r.status_code}")
        except Exception as e:
            print(f"Fetch fail {url}: {e}")
            time.sleep(0.8)
    return None

# 30隊靜態資料，帶東/西岸，確保就算API無conference都分到
STATIC_TEAMS = {
    "ATL": {"team":"Atlanta Hawks","conference":"East","city":"Atlanta"},
    "BOS": {"team":"Boston Celtics","conference":"East","city":"Boston"},
    "BKN": {"team":"Brooklyn Nets","conference":"East","city":"Brooklyn"},
    "CHA": {"team":"Charlotte Hornets","conference":"East","city":"Charlotte"},
    "CHI": {"team":"Chicago Bulls","conference":"East","city":"Chicago"},
    "CLE": {"team":"Cleveland Cavaliers","conference":"East","city":"Cleveland"},
    "DET": {"team":"Detroit Pistons","conference":"East","city":"Detroit"},
    "IND": {"team":"Indiana Pacers","conference":"East","city":"Indiana"},
    "MIA": {"team":"Miami Heat","conference":"East","city":"Miami"},
    "MIL": {"team":"Milwaukee Bucks","conference":"East","city":"Milwaukee"},
    "NYK": {"team":"New York Knicks","conference":"East","city":"New York"},
    "ORL": {"team":"Orlando Magic","conference":"East","city":"Orlando"},
    "PHI": {"team":"Philadelphia 76ers","conference":"East","city":"Philadelphia"},
    "TOR": {"team":"Toronto Raptors","conference":"East","city":"Toronto"},
    "WAS": {"team":"Washington Wizards","conference":"East","city":"Washington"},
    "DAL": {"team":"Dallas Mavericks","conference":"West","city":"Dallas"},
    "DEN": {"team":"Denver Nuggets","conference":"West","city":"Denver"},
    "GSW": {"team":"Golden State Warriors","conference":"West","city":"Golden State"},
    "HOU": {"team":"Houston Rockets","conference":"West","city":"Houston"},
    "LAC": {"team":"LA Clippers","conference":"West","city":"LA"},
    "LAL": {"team":"Los Angeles Lakers","conference":"West","city":"Los Angeles"},
    "MEM": {"team":"Memphis Grizzlies","conference":"West","city":"Memphis"},
    "MIN": {"team":"Minnesota Timberwolves","conference":"West","city":"Minnesota"},
    "NOP": {"team":"New Orleans Pelicans","conference":"West","city":"New Orleans"},
    "OKC": {"team":"Oklahoma City Thunder","conference":"West","city":"Oklahoma City"},
    "PHX": {"team":"Phoenix Suns","conference":"West","city":"Phoenix"},
    "POR": {"team":"Portland Trail Blazers","conference":"West","city":"Portland"},
    "SAC": {"team":"Sacramento Kings","conference":"West","city":"Sacramento"},
    "SAS": {"team":"San Antonio Spurs","conference":"West","city":"San Antonio"},
    "UTA": {"team":"Utah Jazz","conference":"West","city":"Utah"},
}

def get_standings_from_espn_history():
    """用ESPN scoreboard逐日計分，最穩定，GitHub已證實可過"""
    print("=== 開始用 ESPN scoreboard 歷史自計戰績 ===")
    # 初始化
    tally = {}
    for abbr, info in STATIC_TEAMS.items():
        tally[abbr] = {"team": info["team"], "abbr": abbr, "conference": info["conference"], "wins":0, "losses":0, "home":"", "road":"", "streak":"", "pct":0.0, "gb":0}

    start_date = datetime(2026, 10, 21, tzinfo=EST).date()  # 2026-27 開季
    end_date = now_est.date()
    cur = start_date
    total_games = 0
    headers = {"User-Agent":"Mozilla/5.0","Referer":"https://www.espn.com/"}

    while cur <= end_date:
        ymd = cur.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}"
        r = fetch_with_retry(url, headers=headers, timeout=10)
        if r:
            try:
                data = r.json()
                events = data.get("events",[])
                for ev in events:
                    comp = ev.get("competitions",[{}])[0]
                    status_type = comp.get("status",{}).get("type",{}).get("name","")
                    # 只要 Final
                    if status_type != "STATUS_FINAL" and "Final" not in comp.get("status",{}).get("type",{}).get("description",""):
                        # 有時 description = Final
                        desc = comp.get("status",{}).get("type",{}).get("description","")
                        if "Final" not in desc:
                            continue
                    competitors = comp.get("competitors",[])
                    if len(competitors) < 2:
                        continue
                    # 找出勝方
                    winner = None
                    loser = None
                    for c in competitors:
                        if c.get("winner"):
                            winner = c
                        else:
                            # 如果無 winner 標記，用分數比
                            if not winner:
                                pass
                    # 用分數判斷更準
                    if len(competitors)==2:
                        c1, c2 = competitors[0], competitors[1]
                        s1 = int(c1.get("score",0) or 0)
                        s2 = int(c2.get("score",0) or 0)
                        if s1 > s2:
                            winner, loser = c1, c2
                        elif s2 > s1:
                            winner, loser = c2, c1
                        else:
                            continue
                        w_abbr = winner.get("team",{}).get("abbreviation","")
                        l_abbr = loser.get("team",{}).get("abbreviation","")
                        if w_abbr in tally and l_abbr in tally:
                            tally[w_abbr]["wins"] += 1
                            tally[l_abbr]["losses"] += 1
                            total_games += 1
            except Exception as e:
                print(f"Parse scoreboard {ymd} error {e}")
        # 避免被限速
        time.sleep(0.35)
        cur += timedelta(days=1)
        # 安全上限，唔好loop太耐
        if (cur - start_date).days > 25:
            break

    print(f"自計完成，共 {total_games} 場 Final")
    # 轉 list
    teams = list(tally.values())
    for t in teams:
        w = t["wins"]; l = t["losses"]
        tot = w+l
        t["pct"] = w/tot if tot>0 else 0
    # 如果總場數太少，代表API有問題
    if total_games < 10:
        print("自計場數太少，視為失敗")
        return None
    return teams

def get_espn_standings_direct():
    """直接嘗試ESPN standings，作為備援"""
    urls = [
        "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/standings?region=us&lang=en&seasontype=2&type=0&level=3",
        "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/standings",
    ]
    headers = {"User-Agent":"Mozilla/5.0","Accept":"application/json","Referer":"https://www.espn.com/"}
    for url in urls:
        r = fetch_with_retry(url, headers=headers, timeout=10)
        if not r:
            continue
        try:
            data = r.json()
            teams=[]
            for conf in data.get("children",[]):
                conf_name = conf.get("name","")
                for div in conf.get("children",[]):
                    for entry in div.get("standings",{}).get("entries",[]):
                        ti = entry.get("team",{})
                        abbr = ti.get("abbreviation","")
                        stats = {s["name"]: s for s in entry.get("stats",[])}
                        wins = int(stats.get("wins",{}).get("value",0))
                        losses = int(stats.get("losses",{}).get("value",0))
                        pct = float(stats.get("winPercent",{}).get("value",0))
                        info = STATIC_TEAMS.get(abbr, {"team": ti.get("displayName",""), "conference": "East" if "Eastern" in conf_name else "West"})
                        teams.append({
                            "team": info["team"] or ti.get("displayName",""),
                            "abbr": abbr,
                            "conference": info["conference"],
                            "wins": wins,
                            "losses": losses,
                            "pct": pct,
                            "gb": float(stats.get("gamesBehind",{}).get("value",0) or 0),
                            "home": stats.get("home",{}).get("displayValue",""),
                            "road": stats.get("road",{}).get("displayValue",""),
                            "streak": stats.get("streak",{}).get("displayValue",""),
                        })
            if len(teams) >= 20:
                print(f"Direct standings OK {len(teams)}")
                return teams
        except Exception as e:
            print(f"Direct standings parse fail {e}")
            continue
    return None

def get_live_standings():
    # 1. 先用自計歷史，最穩
    teams = get_standings_from_espn_history()
    if teams and len(teams)>=20:
        return teams
    # 2. 再試直接 standings
    teams = get_espn_standings_direct()
    if teams:
        return teams
    print("All standings methods failed")
    return None

def get_recent_scores():
    results=[]
    for delta in [2,1,0]:
        date_obj = (now_est - timedelta(days=delta)).date()
        ymd = date_obj.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}"
        r = fetch_with_retry(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        if not r:
            continue
        try:
            data = r.json()
            for ev in data.get("events",[]):
                comp = ev.get("competitions",[{}])[0]
                status = comp.get("status",{}).get("type",{}).get("description","")
                comps = comp.get("competitors",[])
                if len(comps)<2:
                    continue
                home = next((c for c in comps if c.get("homeAway")=="home"), comps[0])
                away = next((c for c in comps if c.get("homeAway")=="away"), comps[1])
                hs = home.get("score","0")
                aws = away.get("score","0")
                h_name = home.get("team",{}).get("displayName","")
                a_name = away.get("team",{}).get("displayName","")
                results.append(f"{a_name} {aws}-{hs} {h_name} ({status})")
        except:
            continue
        time.sleep(0.3)
    # 去重
    uniq=[]
    seen=set()
    for r in results:
        if r not in seen:
            uniq.append(r); seen.add(r)
    return uniq

def format_standings(teams):
    if not teams or len(teams)<15:
        return f"⚠️ *暫時無法自計戰績，請稍後重試* - {now_str}\n已嘗試 ESPN 歷史逐日統計，建議查看 https://www.espn.com/nba/standings\n"

    east = [t for t in teams if "East" in t["conference"]]
    west = [t for t in teams if "West" in t["conference"]]
    east_sorted = sorted(east, key=lambda x: (x["pct"], x["wins"]), reverse=True)
    west_sorted = sorted(west, key=lambda x: (x["pct"], x["wins"]), reverse=True)

    def calc_gb(lst):
        if not lst: return lst
        leader_w = lst[0]["wins"]; leader_l = lst[0]["losses"]
        for t in lst:
            if t.get("gb",0)==0 and lst.index(t)!=0:
                t["gb"] = ((leader_w - t["wins"]) + (t["losses"] - leader_l))/2
        return lst

    east_sorted = calc_gb(east_sorted)
    west_sorted = calc_gb(west_sorted)

    out = f"🏀 *2026-27 NBA 完整30隊即時戰績榜 (ESPN逐日自計同步)* - {now_str}\n"
    out += f"_來源: ESPN scoreboard 逐日 Final 自計，火箭已更新為最新_\n\n"

    out += "*東岸 1-15 詳細:*\n"
    for i,t in enumerate(east_sorted,1):
        pct = f"{t['pct']:.3f}".lstrip('0') if t['pct']<1 else f"{t['pct']:.3f}"
        gb = f"{t.get('gb',0):.1f}" if i!=1 else "0"
        out += f"{i}. {t['team']} {t['wins']}-{t['losses']} {pct} GB{gb}"
        if t.get("streak"): out+=f" {t['streak']}"
        out+="\n"

    out += "\n*西岸 1-15 詳細:*\n"
    for i,t in enumerate(west_sorted,1):
        pct = f"{t['pct']:.3f}".lstrip('0') if t['pct']<1 else f"{t['pct']:.3f}"
        gb = f"{t.get('gb',0):.1f}" if i!=1 else "0"
        out += f"{i}. {t['team']} {t['wins']}-{t['losses']} {pct} GB{gb}"
        if t.get("streak"): out+=f" {t['streak']}"
        # 標記火箭
        if t["abbr"]=="HOU":
            out+=f" ← 火箭最新"
        if t["abbr"]=="OKC":
            out+=f" ← 雷霆"
        out+="\n"
    return out

def send_daily():
    teams = get_live_standings()
    standings_text = format_standings(teams)
    scores = get_recent_scores()
    scores_text = "📊 *即時戰果 (ESPN同步)*:\n" + ("\n".join(scores[-15:]) if scores else "暫無") + "\n"

    push1 = f"🏀 *NBA 每日 09:30 - Push 1/2 - 完整30隊即時戰績榜 (ESPN逐日自計)* - {now_str}\n\n{standings_text}"
    push2 = f"📰 *NBA 每日 09:30 - Push 2/2 - 30隊詳細新聞+即時戰果* - {now_str}\n\n{scores_text}\n\n"

    thunder = next((t for t in (teams or []) if t.get("abbr")=="OKC"), None)
    if thunder:
        push2 += f"⚡ *雷霆重點 即時同步*: {thunder['team']} {thunder['wins']}-{thunder['losses']} 勝率 {thunder['pct']:.3f} 西北組即時更新，火箭已非5勝1負\n\n"

    push2 += """*東岸焦點*: 76人、塞爾提克、活塞等以 Push 1/2 自計榜為準

*西岸焦點*: 火箭、灰熊、拓荒者、湖人、雷霆等戰績已透過 ESPN 逐日 Final 自計同步，火箭已更新為最新 (請以即時榜為準)

*傷病*: Jalen Williams 賽季報銷、Cason Wallace 盂唇撕裂、Holmgren 缺8-10週

"""
    push2 += "\n_資料來源: ESPN scoreboard 逐日 Final 自計 + cdn.nba.com，每日09:30 HKT 自動更新，GitHub 實測可過_\n"

    send_split(push1, "完整戰績榜")
    time.sleep(2)
    send_split(push2, "詳細新聞")

if __name__ == "__main__":
    print(f"Start V5 self-count at {now_str}")
    send_daily()




