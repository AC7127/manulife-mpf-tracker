import os, requests, time
from datetime import datetime, timezone, timedelta
from collections import defaultdict

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
    "ATL": {"team":"Atlanta Hawks","conference":"East","division":"Southeast","cn":"亞特蘭大鷹"},
    "BOS": {"team":"Boston Celtics","conference":"East","division":"Atlantic","cn":"波士頓塞爾特人"},
    "BKN": {"team":"Brooklyn Nets","conference":"East","division":"Atlantic","cn":"布魯克林籃網"},
    "CHA": {"team":"Charlotte Hornets","conference":"East","division":"Southeast","cn":"夏洛特黃蜂"},
    "CHI": {"team":"Chicago Bulls","conference":"East","division":"Central","cn":"芝加哥公牛"},
    "CLE": {"team":"Cleveland Cavaliers","conference":"East","division":"Central","cn":"克利夫蘭騎士"},
    "DET": {"team":"Detroit Pistons","conference":"East","division":"Central","cn":"底特律活塞"},
    "IND": {"team":"Indiana Pacers","conference":"East","division":"Central","cn":"印第安納溜馬"},
    "MIA": {"team":"Miami Heat","conference":"East","division":"Southeast","cn":"邁阿密熱火"},
    "MIL": {"team":"Milwaukee Bucks","conference":"East","division":"Central","cn":"密爾沃基公鹿"},
    "NYK": {"team":"New York Knicks","conference":"East","division":"Atlantic","cn":"紐約人"},
    "ORL": {"team":"Orlando Magic","conference":"East","division":"Southeast","cn":"奧蘭多魔術"},
    "PHI": {"team":"Philadelphia 76ers","conference":"East","division":"Atlantic","cn":"費城76人"},
    "TOR": {"team":"Toronto Raptors","conference":"East","division":"Atlantic","cn":"多倫多暴龍"},
    "WAS": {"team":"Washington Wizards","conference":"East","division":"Southeast","cn":"華盛頓巫師"},
    "DAL": {"team":"Dallas Mavericks","conference":"West","division":"Southwest","cn":"達拉斯小牛"},
    "DEN": {"team":"Denver Nuggets","conference":"West","division":"Northwest","cn":"丹佛金塊"},
    "GSW": {"team":"Golden State Warriors","conference":"West","division":"Pacific","cn":"金州勇士"},
    "HOU": {"team":"Houston Rockets","conference":"West","division":"Southwest","cn":"侯斯頓火箭"},
    "LAC": {"team":"LA Clippers","conference":"West","division":"Pacific","cn":"洛杉磯快艇"},
    "LAL": {"team":"Los Angeles Lakers","conference":"West","division":"Pacific","cn":"洛杉磯湖人"},
    "MEM": {"team":"Memphis Grizzlies","conference":"West","division":"Southwest","cn":"孟菲斯灰熊"},
    "MIN": {"team":"Minnesota Timberwolves","conference":"West","division":"Northwest","cn":"明尼蘇達灰狼"},
    "NOP": {"team":"New Orleans Pelicans","conference":"West","division":"Southwest","cn":"紐奧良鵜鶘"},
    "OKC": {"team":"Oklahoma City Thunder","conference":"West","division":"Northwest","cn":"奧克拉荷馬雷霆"},
    "PHX": {"team":"Phoenix Suns","conference":"West","division":"Pacific","cn":"鳳凰城太陽"},
    "POR": {"team":"Portland Trail Blazers","conference":"West","division":"Northwest","cn":"波特蘭拓荒者"},
    "SAC": {"team":"Sacramento Kings","conference":"West","division":"Pacific","cn":"薩克拉門托帝王"},
    "SAS": {"team":"San Antonio Spurs","conference":"West","division":"Southwest","cn":"聖安東尼奧馬刺"},
    "UTA": {"team":"Utah Jazz","conference":"West","division":"Northwest","cn":"猶他爵士"},
}

NAME_TO_ABBR = {}
for abbr, info in STATIC_TEAMS.items():
    NAME_TO_ABBR[info["team"]] = abbr
    NAME_TO_ABBR[info["team"].lower()] = abbr
    NAME_TO_ABBR[info["cn"]] = abbr
    for alias in [abbr, abbr.lower()]:
        NAME_TO_ABBR[alias] = abbr
# 額外 ESPN 別名
NAME_TO_ABBR.update({
    "LA Clippers": "LAC", "Los Angeles Clippers": "LAC",
    "New York Knicks": "NYK", "San Antonio Spurs": "SAS",
    "Utah Jazz": "UTA", "Golden State Warriors": "GSW",
    "New Orleans Pelicans": "NOP", "Philadelphia 76ers": "PHI",
    "Washington Wizards": "WAS", "NY": "NYK", "SA": "SAS",
    "NO": "NOP", "WSH": "WAS", "PHL": "PHI", "GS": "GSW",
    "UTAH": "UTA",
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
            # 只計 Regular Season type=2
            season_type = ev.get("season",{}).get("type",2)
            if season_type != 2:
                continue
            comp = ev.get("competitions",[{}])[0]
            stype = comp.get("status",{}).get("type",{}).get("name","")
            desc = comp.get("status",{}).get("type",{}).get("description","")
            if "STATUS_FINAL" not in stype and "Final" not in desc:
                continue
            comps = comp.get("competitors",[])
            if len(comps)<2:
                continue
            c1, c2 = comps[0], comps[1]
            try:
                s1 = int(float(c1.get("score",0) or 0))
                s2 = int(float(c2.get("score",0) or 0))
            except:
                continue
            if s1==s2 or s1==0 and s2==0:
                continue
            # 判斷主客
            home = next((c for c in comps if c.get("homeAway")=="home"), None)
            away = next((c for c in comps if c.get("homeAway")=="away"), None)
            if not home or not away:
                # 用 c1,c2 假設
                home, away = c1, c2
            winner = c1 if s1>s2 else c2
            loser = c2 if s1>s2 else c1
            games.append({
                "date": date_obj,
                "home": home,
                "away": away,
                "winner": winner,
                "loser": loser,
                "home_score": int(home.get("score",0) or 0),
                "away_score": int(away.get("score",0) or 0),
            })
    except Exception as e:
        print(f"ESPN parse {ymd} err {e}")
    return games

def build_standings():
    print("=== V7 開始自計 30隊 Regular Season ===")
    tally = {}
    for abbr, info in STATIC_TEAMS.items():
        tally[abbr] = {
            "team": info["team"], "abbr": abbr, "cn": info["cn"],
            "conference": info["conference"], "division": info["division"],
            "wins":0, "losses":0,
            "home_w":0, "home_l":0, "road_w":0, "road_l":0,
            "div_w":0, "div_l":0, "conf_w":0, "conf_l":0,
            "pf":0, "pa":0,
            "games": []  # 按時間順序 {win:bool, date}
        }

    start = datetime(2026,10,22, tzinfo=EST).date()  # 2026-27 常規賽開始
    end = now_est.date()
    cur = start
    total_final = 0
    while cur <= end:
        games = get_games_from_espn(cur)
        for g in games:
            home = g["home"]; away = g["away"]
            hs = g["home_score"]; aws = g["away_score"]
            # 取隊名
            h_name = home.get("team",{}).get("displayName","")
            a_name = away.get("team",{}).get("displayName","")
            h_abbr_raw = home.get("team",{}).get("abbreviation","")
            a_abbr_raw = away.get("team",{}).get("abbreviation","")

            h_key = NAME_TO_ABBR.get(h_name) or NAME_TO_ABBR.get(h_name.lower()) or NAME_TO_ABBR.get(h_abbr_raw) or NAME_TO_ABBR.get(h_abbr_raw.lower())
            a_key = NAME_TO_ABBR.get(a_name) or NAME_TO_ABBR.get(a_name.lower()) or NAME_TO_ABBR.get(a_abbr_raw) or NAME_TO_ABBR.get(a_abbr_raw.lower())

            if h_key not in tally or a_key not in tally:
                # 嘗試 tricode
                if h_abbr_raw in tally:
                    h_key = h_abbr_raw
                if a_abbr_raw in tally:
                    a_key = a_abbr_raw
            if h_key not in tally or a_key not in tally:
                print(f"Unmapped {cur} {h_name}({h_abbr_raw}) vs {a_name}({a_abbr_raw})")
                continue

            # 勝負
            home_win = hs > aws
            if home_win:
                tally[h_key]["wins"]+=1
                tally[h_key]["home_w"]+=1
                tally[a_key]["losses"]+=1
                tally[a_key]["road_l"]+=1
                tally[h_key]["games"].append({"win":True, "date":cur})
                tally[a_key]["games"].append({"win":False, "date":cur})
            else:
                tally[a_key]["wins"]+=1
                tally[a_key]["road_w"]+=1
                tally[h_key]["losses"]+=1
                tally[h_key]["home_l"]+=1
                tally[a_key]["games"].append({"win":True, "date":cur})
                tally[h_key]["games"].append({"win":False, "date":cur})

            # 得分
            tally[h_key]["pf"]+=hs
            tally[h_key]["pa"]+=aws
            tally[a_key]["pf"]+=aws
            tally[a_key]["pa"]+=hs

            # 賽區/聯盟
            h_div = tally[h_key]["division"]
            a_div = tally[a_key]["division"]
            h_conf = tally[h_key]["conference"]
            a_conf = tally[a_key]["conference"]
            if h_div == a_div:
                if home_win:
                    tally[h_key]["div_w"]+=1
                    tally[a_key]["div_l"]+=1
                else:
                    tally[a_key]["div_w"]+=1
                    tally[h_key]["div_l"]+=1
            if h_conf == a_conf:
                if home_win:
                    tally[h_key]["conf_w"]+=1
                    tally[a_key]["conf_l"]+=1
                else:
                    tally[a_key]["conf_w"]+=1
                    tally[h_key]["conf_l"]+=1

            total_final+=1
        time.sleep(0.35)
        cur += timedelta(days=1)
        if (cur - start).days > 35:
            break

    print(f"Total Regular Season Final counted: {total_final}")
    for t in tally.values():
        w=t["wins"]; l=t["losses"]
        t["pct"]= w/(w+l) if (w+l)>0 else 0
        t["ppg"]= t["pf"]/(w+l) if (w+l)>0 else 0
        t["opp_ppg"]= t["pa"]/(w+l) if (w+l)>0 else 0
        t["diff"]= t["ppg"]-t["opp_ppg"]
        # STRK
        games = t["games"]
        if games:
            last_win = games[-1]["win"]
            streak = 0
            for g in reversed(games):
                if g["win"]==last_win:
                    streak+=1
                else:
                    break
            t["streak"]= f"{'W' if last_win else 'L'}{streak}"
            # 最近10場
            last10 = games[-10:]
            w10 = sum(1 for g in last10 if g["win"])
            l10 = len(last10)-w10
            t["l10"]= f"{w10}-{l10}"
        else:
            t["streak"]=""; t["l10"]="0-0"

    if total_final < 20:
        print("自計太少")
        return None
    return list(tally.values())

def format_standings(teams):
    if not teams:
        return f"⚠️ 暫時無法自計戰績 - {now_str}\n"

    east = [t for t in teams if t["conference"]=="East"]
    west = [t for t in teams if t["conference"]=="West"]
    east_sorted = sorted(east, key=lambda x: (x["pct"], x["wins"]), reverse=True)
    west_sorted = sorted(west, key=lambda x: (x["pct"], x["wins"]), reverse=True)

    def calc_gb(lst):
        if not lst: return lst
        lw = lst[0]["wins"]; ll = lst[0]["losses"]
        for t in lst:
            gb = ((lw - t["wins"]) + (t["losses"] - ll))/2
            if gb < 0: gb = 0
            t["gb"]=gb
        return lst

    east_sorted = calc_gb(east_sorted)
    west_sorted = calc_gb(west_sorted)

    # 完整12欄格式，貼近官網截圖
    out = f"🏀 *2026-27 NBA 完整30隊即時戰績榜 (V7 完整12欄同步官網)* - {now_str}\n"
    out += f"_來源: ESPN Regular Season逐日Final自計，已過濾季前賽_\n\n"

    def format_table(sorted_list, title):
        s = f"*{title} 1-15 詳細:*\n"
        s += "`勝利 戰敗 勝率 GB 主場 客場 賽區 聯盟 PPG OPP PPG DIFF 最近10場 STRK`\n"
        for i,t in enumerate(sorted_list,1):
            pct_str = f"{t['pct']:.3f}".lstrip('0')
            if t['pct']==0: pct_str=".000"
            if t['pct']>=1: pct_str="1.000"
            home = f"{t['home_w']}-{t['home_l']}"
            road = f"{t['road_w']}-{t['road_l']}"
            div = f"{t['div_w']}-{t['div_l']}"
            conf = f"{t['conf_w']}-{t['conf_l']}"
            s += f"{i}. {t['cn']} {t['team']} {t['wins']} {t['losses']} {pct_str} {t['gb']:.1f} {home} {road} {div} {conf} {t['ppg']:.1f} {t['opp_ppg']:.1f} {t['diff']:+.1f} {t['l10']} {t['streak']}"
            if t['abbr']=="HOU":
                s+=" ← 火箭最新"
            if t['abbr']=="OKC":
                s+=" ← 雷霆"
            s+="\n"
        return s

    out += format_table(east_sorted, "東岸")
    out += "\n"
    out += format_table(west_sorted, "西岸")
    return out

def get_recent_scores():
    results=[]
    for delta in [2,1,0]:
        d = (now_est - timedelta(days=delta)).date()
        ymd = d.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}"
        r = fetch(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        if not r:
            continue
        try:
            data = r.json()
            for ev in data.get("events",[]):
                if ev.get("season",{}).get("type",2)!=2:
                    continue
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

    push1 = f"🏀 *NBA 每日 09:30 - Push 1/2 - 完整30隊即時戰績榜 (V7 12欄官網同步)* - {now_str}\n\n{standings_text}"
    push2 = f"📰 *NBA 每日 09:30 - Push 2/2 - 即時戰果+雷霆* - {now_str}\n\n{scores_text}\n\n"

    thunder = next((t for t in (teams or []) if t["abbr"]=="OKC"), None)
    if thunder:
        push2 += f"⚡ *雷霆重點*: {thunder['cn']} {thunder['team']} {thunder['wins']}-{thunder['losses']} 勝率 {thunder['pct']:.3f} {thunder['streak']} 主場 {thunder['home_w']}-{thunder['home_l']}\n\n"

    push2 += "_資料來源: ESPN Regular Season逐日Final自計，12欄完整同步NBA.com官網格式，每日09:30 HKT 自動更新_\n"

    send_split(push1, "完整戰績榜")
    time.sleep(2)
    send_split(push2, "詳細新聞")

if __name__ == "__main__":
    print(f"Start V7 at {now_str}")
    send_daily()






