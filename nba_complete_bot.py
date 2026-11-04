import os, requests, time
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

def send_split(text, title=""):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing token")
        return
    parts = [text[i:i+MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    for idx, part in enumerate(parts):
        msg = part if idx==0 else f"{title} (續 {idx+1}/{len(parts)})\n\n"+part
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": True}
        try:
            r = requests.post(url, json=payload, timeout=15)
            print(f"{title} {idx+1}/{len(parts)} {r.status_code}")
        except Exception as e:
            print(f"Telegram err {e}")
        time.sleep(0.9)

HKT = timezone(timedelta(hours=8))
EST = timezone(timedelta(hours=-5))
now_hkt = datetime.now(HKT)
now_est = datetime.now(EST)
now_str = now_hkt.strftime('%Y-%m-%d %H:%M HKT')

def fetch(url, headers=None, timeout=12):
    if headers is None:
        headers={"User-Agent":"Mozilla/5.0"}
    for _ in range(2):
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            if r.status_code==200 and len(r.text)>50:
                return r
        except Exception as e:
            print(f"fetch fail {url} {e}")
            time.sleep(0.5)
    return None

STATIC_TEAMS = {
    "ATL": {"team":"Atlanta Hawks","conference":"East"},
    "BOS": {"team":"Boston Celtics","conference":"East"},
    "BKN": {"team":"Brooklyn Nets","conference":"East"},
    "CHA": {"team":"Charlotte Hornets","conference":"East"},
    "CHI": {"team":"Chicago Bulls","conference":"East"},
    "CLE": {"team":"Cleveland Cavaliers","conference":"East"},
    "DET": {"team":"Detroit Pistons","conference":"East"},
    "IND": {"team":"Indiana Pacers","conference":"East"},
    "MIA": {"team":"Miami Heat","conference":"East"},
    "MIL": {"team":"Milwaukee Bucks","conference":"East"},
    "NYK": {"team":"New York Knicks","conference":"East","aliases":["NY","New York Knicks"]},
    "ORL": {"team":"Orlando Magic","conference":"East"},
    "PHI": {"team":"Philadelphia 76ers","conference":"East","aliases":["PHL"]},
    "TOR": {"team":"Toronto Raptors","conference":"East"},
    "WAS": {"team":"Washington Wizards","conference":"East","aliases":["WSH"]},
    "DAL": {"team":"Dallas Mavericks","conference":"West"},
    "DEN": {"team":"Denver Nuggets","conference":"West"},
    "GSW": {"team":"Golden State Warriors","conference":"West","aliases":["GS"]},
    "HOU": {"team":"Houston Rockets","conference":"West"},
    "LAC": {"team":"LA Clippers","conference":"West","aliases":["Los Angeles Clippers"]},
    "LAL": {"team":"Los Angeles Lakers","conference":"West"},
    "MEM": {"team":"Memphis Grizzlies","conference":"West"},
    "MIN": {"team":"Minnesota Timberwolves","conference":"West"},
    "NOP": {"team":"New Orleans Pelicans","conference":"West","aliases":["NO","NOH"]},
    "OKC": {"team":"Oklahoma City Thunder","conference":"West"},
    "PHX": {"team":"Phoenix Suns","conference":"West"},
    "POR": {"team":"Portland Trail Blazers","conference":"West"},
    "SAC": {"team":"Sacramento Kings","conference":"West"},
    "SAS": {"team":"San Antonio Spurs","conference":"West","aliases":["SA"]},
    "UTA": {"team":"Utah Jazz","conference":"West","aliases":["UTAH"]},
}

# 建立 displayName -> abbr 對應，包含別名
NAME_TO_ABBR = {}
for abbr, info in STATIC_TEAMS.items():
    NAME_TO_ABBR[info["team"]] = abbr
    # 小寫版本
    NAME_TO_ABBR[info["team"].lower()] = abbr
    for alias in info.get("aliases",[]):
        NAME_TO_ABBR[alias] = abbr
        NAME_TO_ABBR[alias.lower()] = abbr
# 額外 ESPN 常見 displayName
NAME_TO_ABBR.update({
    "LA Clippers": "LAC",
    "Los Angeles Clippers": "LAC",
    "New York Knicks": "NYK",
    "San Antonio Spurs": "SAS",
    "Utah Jazz": "UTA",
    "Golden State Warriors": "GSW",
    "New Orleans Pelicans": "NOP",
    "Philadelphia 76ers": "PHI",
    "Washington Wizards": "WAS",
})

def get_games_from_espn(date_obj):
    ymd = date_obj.strftime("%Y%m%d")
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}"
    r = fetch(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://www.espn.com/"}, timeout=10)
    games=[]
    if not r:
        return games
    try:
        data = r.json()
        for ev in data.get("events",[]):
            comp = ev.get("competitions",[{}])[0]
            stype = comp.get("status",{}).get("type",{}).get("name","")
            desc = comp.get("status",{}).get("type",{}).get("description","")
            if "STATUS_FINAL" not in stype and "Final" not in desc:
                continue
            comps = comp.get("competitors",[])
            if len(comps)<2:
                continue
            # 用分數判斷勝負最準
            c1, c2 = comps[0], comps[1]
            try:
                s1 = int(float(c1.get("score",0) or 0))
                s2 = int(float(c2.get("score",0) or 0))
            except:
                continue
            if s1==s2:
                continue
            winner = c1 if s1>s2 else c2
            loser = c2 if s1>s2 else c1
            w_name = winner.get("team",{}).get("displayName","") or winner.get("team",{}).get("name","")
            l_name = loser.get("team",{}).get("displayName","") or loser.get("team",{}).get("name","")
            # 也試 abbr
            w_abbr = winner.get("team",{}).get("abbreviation","")
            l_abbr = loser.get("team",{}).get("abbreviation","")
            games.append((w_name, l_name, w_abbr, l_abbr))
    except Exception as e:
        print(f"ESPN parse {ymd} err {e}")
    return games

def get_games_from_cdn(date_obj):
    y = date_obj.strftime("%Y")
    m = date_obj.strftime("%m")
    d = date_obj.strftime("%d")
    url = f"https://cdn.nba.com/static/json/liveData/scoreboard/{y}/{m}/{d}/scoreboard.json"
    r = fetch(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://www.nba.com/"}, timeout=10)
    games=[]
    if not r:
        return games
    try:
        data = r.json()
        g_list = data.get("scoreboard",{}).get("games",[]) or data.get("games",[])
        for g in g_list:
            status = g.get("gameStatus",0)  # 3=Final
            if status!=3:
                # 也看 gameStatusText
                if "Final" not in g.get("gameStatusText",""):
                    continue
            home = g.get("homeTeam",{})
            away = g.get("awayTeam",{})
            hs = int(home.get("score",0) or 0)
            aws = int(away.get("score",0) or 0)
            if hs==aws:
                continue
            if hs>aws:
                w_code = home.get("teamTricode","")
                l_code = away.get("teamTricode","")
                w_name = home.get("teamCity","")+" "+home.get("teamName","")
                l_name = away.get("teamCity","")+" "+away.get("teamName","")
            else:
                w_code = away.get("teamTricode","")
                l_code = home.get("teamTricode","")
                w_name = away.get("teamCity","")+" "+away.get("teamName","")
                l_name = home.get("teamCity","")+" "+home.get("teamName","")
            games.append((w_name, l_name, w_code, l_code))
    except Exception as e:
        print(f"CDN parse {y}-{m}-{d} err {e}")
    return games

def build_standings():
    print("=== V6 開始自計 30隊 ===")
    tally = {}
    for abbr, info in STATIC_TEAMS.items():
        tally[abbr] = {"team": info["team"], "abbr": abbr, "conference": info["conference"], "wins":0, "losses":0, "pct":0.0, "gb":0, "streak":"", "home":"", "road":""}

    start = datetime(2026,10,15, tzinfo=EST).date()
    end = now_est.date()
    cur = start
    total_final = 0
    while cur <= end:
        # 先試 ESPN
        games = get_games_from_espn(cur)
        if not games:
            games = get_games_from_cdn(cur)
        for w_name, l_name, w_abbr, l_abbr in games:
            # 優先用 displayName 映射
            w_key = NAME_TO_ABBR.get(w_name) or NAME_TO_ABBR.get(w_name.lower()) or NAME_TO_ABBR.get(w_abbr) or NAME_TO_ABBR.get(w_abbr.lower())
            l_key = NAME_TO_ABBR.get(l_name) or NAME_TO_ABBR.get(l_name.lower()) or NAME_TO_ABBR.get(l_abbr) or NAME_TO_ABBR.get(l_abbr.lower())
            # 如果都對唔上，試用 Tricode 直接
            if not w_key and w_abbr in tally:
                w_key = w_abbr
            if not l_key and l_abbr in tally:
                l_key = l_abbr
            if w_key in tally and l_key in tally:
                tally[w_key]["wins"]+=1
                tally[l_key]["losses"]+=1
                total_final+=1
            else:
                print(f"Unmapped game {cur} {w_name}({w_abbr})->{w_key} beat {l_name}({l_abbr})->{l_key}")
        time.sleep(0.35)
        cur += timedelta(days=1)
        if (cur - start).days > 30:  # 最多30日，足夠覆蓋開季到今日
            break

    print(f"Total Final counted: {total_final}")
    teams = list(tally.values())
    for t in teams:
        w=t["wins"]; l=t["losses"]
        t["pct"]= w/(w+l) if (w+l)>0 else 0.0
    # 檢查是否太少
    if total_final < 20:
        print("自計太少，視為失敗")
        return None
    return teams

def format_standings(teams):
    if not teams or len(teams)<10:
        return f"⚠️ 暫時無法自計戰績，請稍後重試 - {now_str}\n"

    east = [t for t in teams if t["conference"]=="East"]
    west = [t for t in teams if t["conference"]=="West"]
    east_sorted = sorted(east, key=lambda x: (x["pct"], x["wins"]), reverse=True)
    west_sorted = sorted(west, key=lambda x: (x["pct"], x["wins"]), reverse=True)

    def calc_gb(lst):
        if not lst:
            return lst
        leader = lst[0]
        lw = leader["wins"]; ll = leader["losses"]
        for t in lst:
            gb = ((lw - t["wins"]) + (t["losses"] - ll))/2
            if gb < 0:
                gb = 0
            t["gb"]=gb
        return lst

    east_sorted = calc_gb(east_sorted)
    west_sorted = calc_gb(west_sorted)

    out = f"🏀 *2026-27 NBA 完整30隊即時戰績榜 (ESPN逐日自計 V6)* - {now_str}\n"
    out += f"_來源: ESPN+CDN逐日Final自計，火箭已更新_\n\n"

    out += "*東岸 1-15 詳細:*\n"
    for i,t in enumerate(east_sorted,1):
        pct_str = f"{t['pct']:.3f}".lstrip('0') if t['pct']<1 else f"{t['pct']:.3f}"
        if t['pct']==0:
            pct_str=" .000"
        out += f"{i}. {t['team']} {t['wins']}-{t['losses']} {pct_str} GB{t['gb']:.1f}"
        if t['abbr']=="OKC":
            out+=" ← 雷霆"
        out+="\n"

    out += "\n*西岸 1-15 詳細:*\n"
    for i,t in enumerate(west_sorted,1):
        pct_str = f"{t['pct']:.3f}".lstrip('0') if t['pct']<1 else f"{t['pct']:.3f}"
        if t['pct']==0:
            pct_str=" .000"
        out += f"{i}. {t['team']} {t['wins']}-{t['losses']} {pct_str} GB{t['gb']:.1f}"
        if t['abbr']=="HOU":
            out+=" ← 火箭最新"
        if t['abbr']=="OKC":
            out+=" ← 雷霆"
        out+="\n"
    return out

def get_recent_scores():
    results=[]
    for delta in [2,1,0]:
        d = (now_est - timedelta(days=delta)).date()
        games = get_games_from_espn(d)
        if not games:
            games = get_games_from_cdn(d)
        # 為顯示，我們重新抓一次詳細比分
        ymd = d.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}"
        r = fetch(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        if r:
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
                pass
        time.sleep(0.3)
    # 去重
    uniq=[]
    seen=set()
    for r in results:
        if r not in seen:
            uniq.append(r); seen.add(r)
    return uniq[-15:]

def send_daily():
    teams = build_standings()
    standings_text = format_standings(teams)
    scores = get_recent_scores()
    scores_text = "📊 *即時戰果 (ESPN同步)*:\n" + ("\n".join(scores) if scores else "暫無") + "\n"

    push1 = f"🏀 *NBA 每日 09:30 - Push 1/2 - 完整30隊即時戰績榜 (ESPN逐日自計 V6)* - {now_str}\n\n{standings_text}"
    push2 = f"📰 *NBA 每日 09:30 - Push 2/2 - 即時戰果* - {now_str}\n\n{scores_text}\n\n"

    thunder = next((t for t in (teams or []) if t["abbr"]=="OKC"), None)
    if thunder:
        push2 += f"⚡ *雷霆重點 即時同步*: {thunder['team']} {thunder['wins']}-{thunder['losses']} 勝率 {thunder['pct']:.3f}\n\n"

    push2 += "_資料來源: ESPN scoreboard + cdn.nba.com 逐日 Final 自計，每日09:30 HKT 自動更新_\n"

    send_split(push1, "完整戰績榜")
    time.sleep(2)
    send_split(push2, "詳細新聞")

if __name__ == "__main__":
    print(f"Start V6 at {now_str}")
    send_daily()





