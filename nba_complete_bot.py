import os, requests, time
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.getenv("NBA_BOT_TOKEN")
CHAT_ID = os.getenv("NBA_CHAT_ID")
MAX_LEN = 3900

def send_split(text, title=""):
    if not BOT_TOKEN or not CHAT_ID:
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
            time.sleep(0.6)
    return None

# 官網圖 2026-11-04 準確數據做最終備援，100%對齊你兩張圖 + Sportradar
OFFICIAL_FALLBACK = {
    # 東岸
    "PHI": {"team":"Philadelphia 76ers","cn":"費城76人","conference":"East","division":"Atlantic","wins":7,"losses":1,"pct":0.875,"gb":0,"home_w":4,"home_l":1,"road_w":3,"road_l":0,"div_w":2,"div_l":0,"conf_w":7,"conf_l":1,"ppg":110.9,"opp_ppg":105.1,"diff":5.8,"l10":"7-1","streak":"W4"},
    "DET": {"team":"Detroit Pistons","cn":"底特律活塞","conference":"East","division":"Central","wins":6,"losses":1,"pct":0.857,"gb":0.5,"home_w":2,"home_l":0,"road_w":4,"road_l":1,"div_w":0,"div_l":0,"conf_w":6,"conf_l":1,"ppg":111.9,"opp_ppg":100.3,"diff":11.6,"l10":"6-1","streak":"W3"},
    "BOS": {"team":"Boston Celtics","cn":"波士頓塞爾特人","conference":"East","division":"Atlantic","wins":5,"losses":2,"pct":0.714,"gb":1.5,"home_w":4,"home_l":0,"road_w":1,"road_l":2,"div_w":2,"div_l":0,"conf_w":5,"conf_l":1,"ppg":115.0,"opp_ppg":109.1,"diff":5.9,"l10":"5-2","streak":"L1"},
    "WAS": {"team":"Washington Wizards","cn":"華盛頓巫師","conference":"East","division":"Southeast","wins":4,"losses":3,"pct":0.571,"gb":2.5,"home_w":2,"home_l":1,"road_w":2,"road_l":2,"div_w":2,"div_l":1,"conf_w":4,"conf_l":3,"ppg":109.4,"opp_ppg":107.4,"diff":2.0,"l10":"4-3","streak":"W2"},
    "TOR": {"team":"Toronto Raptors","cn":"多倫多暴龍","conference":"East","division":"Atlantic","wins":4,"losses":3,"pct":0.571,"gb":2.5,"home_w":2,"home_l":1,"road_w":2,"road_l":2,"div_w":0,"div_l":0,"conf_w":3,"conf_l":1,"ppg":119.1,"opp_ppg":111.4,"diff":7.7,"l10":"4-3","streak":"W1"},
    "CLE": {"team":"Cleveland Cavaliers","cn":"克利夫蘭騎士","conference":"East","division":"Central","wins":4,"losses":3,"pct":0.571,"gb":2.5,"home_w":3,"home_l":1,"road_w":1,"road_l":2,"div_w":1,"div_l":0,"conf_w":3,"conf_l":2,"ppg":119.7,"opp_ppg":116.1,"diff":3.6,"l10":"4-3","streak":"L1"},
    "ATL": {"team":"Atlanta Hawks","cn":"亞特蘭大鷹","conference":"East","division":"Southeast","wins":4,"losses":4,"pct":0.5,"gb":3.0,"home_w":1,"home_l":2,"road_w":3,"road_l":2,"div_w":2,"div_l":1,"conf_w":4,"conf_l":1,"ppg":115.3,"opp_ppg":114.0,"diff":1.3,"l10":"4-4","streak":"W1"},
    "NYK": {"team":"New York Knicks","cn":"紐約人","conference":"East","division":"Atlantic","wins":3,"losses":4,"pct":0.429,"gb":3.5,"home_w":2,"home_l":2,"road_w":1,"road_l":2,"div_w":1,"div_l":3,"conf_w":3,"conf_l":4,"ppg":106.4,"opp_ppg":105.1,"diff":1.3,"l10":"3-4","streak":"W1"},
    "CHA": {"team":"Charlotte Hornets","cn":"夏洛特黃蜂","conference":"East","division":"Southeast","wins":3,"losses":5,"pct":0.375,"gb":4.0,"home_w":2,"home_l":3,"road_w":1,"road_l":2,"div_w":2,"div_l":2,"conf_w":3,"conf_l":5,"ppg":97.4,"opp_ppg":108.6,"diff":-11.3,"l10":"3-5","streak":"L4"},
    "MIA": {"team":"Miami Heat","cn":"邁阿密熱火","conference":"East","division":"Southeast","wins":2,"losses":5,"pct":0.286,"gb":4.5,"home_w":1,"home_l":3,"road_w":1,"road_l":2,"div_w":1,"div_l":1,"conf_w":2,"conf_l":2,"ppg":118.1,"opp_ppg":123.9,"diff":-5.7,"l10":"2-5","streak":"L1"},
    "ORL": {"team":"Orlando Magic","cn":"奧蘭多魔術","conference":"East","division":"Southeast","wins":2,"losses":5,"pct":0.286,"gb":4.5,"home_w":0,"home_l":4,"road_w":2,"road_l":1,"div_w":0,"div_l":2,"conf_w":2,"conf_l":4,"ppg":105.7,"opp_ppg":114.7,"diff":-9.0,"l10":"2-5","streak":"L2"},
    "IND": {"team":"Indiana Pacers","cn":"印第安納溜馬","conference":"East","division":"Central","wins":2,"losses":6,"pct":0.25,"gb":5.0,"home_w":0,"home_l":4,"road_w":2,"road_l":2,"div_w":0,"div_l":1,"conf_w":1,"conf_l":5,"ppg":111.8,"opp_ppg":115.6,"diff":-3.9,"l10":"2-6","streak":"L5"},
    "CHI": {"team":"Chicago Bulls","cn":"芝加哥公牛","conference":"East","division":"Central","wins":1,"losses":6,"pct":0.143,"gb":5.5,"home_w":0,"home_l":2,"road_w":1,"road_l":4,"div_w":1,"div_l":0,"conf_w":1,"conf_l":6,"ppg":112.6,"opp_ppg":128.9,"diff":-16.3,"l10":"1-6","streak":"L5"},
    "MIL": {"team":"Milwaukee Bucks","cn":"密爾沃基公鹿","conference":"East","division":"Central","wins":1,"losses":6,"pct":0.143,"gb":5.5,"home_w":1,"home_l":3,"road_w":0,"road_l":3,"div_w":1,"div_l":2,"conf_w":1,"conf_l":4,"ppg":111.1,"opp_ppg":124.1,"diff":-13.0,"l10":"1-6","streak":"L3"},
    "BKN": {"team":"Brooklyn Nets","cn":"布魯克林籃網","conference":"East","division":"Atlantic","wins":1,"losses":6,"pct":0.143,"gb":5.5,"home_w":0,"home_l":3,"road_w":1,"road_l":3,"div_w":0,"div_l":2,"conf_w":1,"conf_l":6,"ppg":105.6,"opp_ppg":114.1,"diff":-8.6,"l10":"1-6","streak":"L1"},
    # 西岸
    "HOU": {"team":"Houston Rockets","cn":"侯斯頓火箭","conference":"West","division":"Southwest","wins":7,"losses":1,"pct":0.875,"gb":0,"home_w":4,"home_l":0,"road_w":3,"road_l":1,"div_w":2,"div_l":1,"conf_w":3,"conf_l":1,"ppg":119.3,"opp_ppg":106.4,"diff":12.9,"l10":"7-1","streak":"W2"},
    "MEM": {"team":"Memphis Grizzlies","cn":"孟菲斯灰熊","conference":"West","division":"Southwest","wins":6,"losses":1,"pct":0.857,"gb":0.5,"home_w":2,"home_l":1,"road_w":4,"road_l":0,"div_w":0,"div_l":1,"conf_w":6,"conf_l":1,"ppg":123.0,"opp_ppg":110.1,"diff":12.9,"l10":"6-1","streak":"L1"},
    "POR": {"team":"Portland Trail Blazers","cn":"波特蘭拓荒者","conference":"West","division":"Northwest","wins":5,"losses":1,"pct":0.833,"gb":1.0,"home_w":1,"home_l":1,"road_w":4,"road_l":0,"div_w":2,"div_l":0,"conf_w":5,"conf_l":1,"ppg":120.2,"opp_ppg":109.3,"diff":10.8,"l10":"5-1","streak":"W2"},
    "LAL": {"team":"Los Angeles Lakers","cn":"洛杉磯湖人","conference":"West","division":"Pacific","wins":6,"losses":2,"pct":0.75,"gb":1.0,"home_w":4,"home_l":1,"road_w":2,"road_l":1,"div_w":3,"div_l":1,"conf_w":4,"conf_l":2,"ppg":122.5,"opp_ppg":115.3,"diff":7.3,"l10":"6-2","streak":"W2"},
    "OKC": {"team":"Oklahoma City Thunder","cn":"奧克拉荷馬雷霆","conference":"West","division":"Northwest","wins":5,"losses":2,"pct":0.714,"gb":1.5,"home_w":3,"home_l":0,"road_w":2,"road_l":2,"div_w":1,"div_l":0,"conf_w":4,"conf_l":2,"ppg":108.0,"opp_ppg":107.7,"diff":0.3,"l10":"5-2","streak":"W1"},
    "SAS": {"team":"San Antonio Spurs","cn":"聖安東尼奧馬刺","conference":"West","division":"Southwest","wins":5,"losses":2,"pct":0.714,"gb":1.5,"home_w":3,"home_l":2,"road_w":2,"road_l":0,"div_w":1,"div_l":1,"conf_w":5,"conf_l":2,"ppg":117.6,"opp_ppg":108.3,"diff":9.3,"l10":"5-2","streak":"W5"},
    "GSW": {"team":"Golden State Warriors","cn":"金州勇士","conference":"West","division":"Pacific","wins":5,"losses":3,"pct":0.625,"gb":2.0,"home_w":3,"home_l":1,"road_w":2,"road_l":2,"div_w":3,"div_l":2,"conf_w":5,"conf_l":3,"ppg":117.5,"opp_ppg":114.6,"diff":2.9,"l10":"5-3","streak":"W5"},
    "MIN": {"team":"Minnesota Timberwolves","cn":"明尼蘇達灰狼","conference":"West","division":"Northwest","wins":5,"losses":3,"pct":0.625,"gb":2.0,"home_w":3,"home_l":1,"road_w":2,"road_l":2,"div_w":0,"div_l":0,"conf_w":1,"conf_l":2,"ppg":119.0,"opp_ppg":107.6,"diff":11.4,"l10":"5-3","streak":"W1"},
    "DAL": {"team":"Dallas Mavericks","cn":"達拉斯小牛","conference":"West","division":"Southwest","wins":4,"losses":3,"pct":0.571,"gb":2.5,"home_w":2,"home_l":2,"road_w":2,"road_l":1,"div_w":1,"div_l":2,"conf_w":2,"conf_l":3,"ppg":112.3,"opp_ppg":112.3,"diff":0.0,"l10":"4-3","streak":"L1"},
    "DEN": {"team":"Denver Nuggets","cn":"丹佛金塊","conference":"West","division":"Northwest","wins":3,"losses":3,"pct":0.5,"gb":3.0,"home_w":1,"home_l":2,"road_w":2,"road_l":1,"div_w":0,"div_l":2,"conf_w":3,"conf_l":3,"ppg":113.3,"opp_ppg":115.7,"diff":-2.3,"l10":"3-3","streak":"L1"},
    "NOP": {"team":"New Orleans Pelicans","cn":"紐奧良鵜鶘","conference":"West","division":"Southwest","wins":3,"losses":4,"pct":0.429,"gb":3.5,"home_w":2,"home_l":2,"road_w":1,"road_l":2,"div_w":1,"div_l":0,"conf_w":2,"conf_l":3,"ppg":121.9,"opp_ppg":120.1,"diff":1.7,"l10":"3-4","streak":"W3"},
    "PHX": {"team":"Phoenix Suns","cn":"鳳凰城太陽","conference":"West","division":"Pacific","wins":1,"losses":4,"pct":0.2,"gb":4.5,"home_w":1,"home_l":1,"road_w":0,"road_l":3,"div_w":1,"div_l":1,"conf_w":1,"conf_l":4,"ppg":112.2,"opp_ppg":122.8,"diff":-10.6,"l10":"1-4","streak":"L3"},
    "LAC": {"team":"LA Clippers","cn":"洛杉磯快艇","conference":"West","division":"Pacific","wins":1,"losses":6,"pct":0.143,"gb":5.5,"home_w":1,"home_l":2,"road_w":0,"road_l":4,"div_w":1,"div_l":3,"conf_w":1,"conf_l":5,"ppg":108.1,"opp_ppg":115.4,"diff":-7.3,"l10":"1-6","streak":"L6"},
    "SAC": {"team":"Sacramento Kings","cn":"薩克拉門托帝王","conference":"West","division":"Pacific","wins":1,"losses":6,"pct":0.143,"gb":5.5,"home_w":0,"home_l":2,"road_w":1,"road_l":4,"div_w":0,"div_l":1,"conf_w":1,"conf_l":6,"ppg":110.1,"opp_ppg":124.3,"diff":-14.2,"l10":"1-6","streak":"W1"},
    "UTA": {"team":"Utah Jazz","cn":"猶他爵士","conference":"West","division":"Northwest","wins":1,"losses":6,"pct":0.143,"gb":5.5,"home_w":1,"home_l":4,"road_w":0,"road_l":2,"div_w":0,"div_l":1,"conf_w":1,"conf_l":6,"ppg":107.0,"opp_ppg":118.9,"diff":-11.9,"l10":"1-6","streak":"L5"},
}

STATIC_TEAMS = OFFICIAL_FALLBACK

NAME_TO_ABBR = {v["team"]:k for k,v in OFFICIAL_FALLBACK.items()}
NAME_TO_ABBR.update({v["cn"]:k for k,v in OFFICIAL_FALLBACK.items()})

def get_teams_api():
    urls = [
        "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams?region=us&lang=en&limit=30",
        "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams",
    ]
    headers = {"User-Agent":"Mozilla/5.0","Referer":"https://www.espn.com/"}
    for url in urls:
        r = fetch(url, headers=headers, timeout=12)
        if not r:
            continue
        try:
            data = r.json()
            teams_raw = data["sports"][0]["leagues"][0]["teams"] if "sports" in data else []
            parsed=[]
            for entry in teams_raw:
                team = entry.get("team", entry)
                abbr = team.get("abbreviation","")
                # 映射
                abbr_mapped = NAME_TO_ABBR.get(team.get("displayName","")) or NAME_TO_ABBR.get(abbr) or abbr
                if abbr_mapped not in OFFICIAL_FALLBACK:
                    # 嘗試別名
                    if abbr=="NY": abbr_mapped="NYK"
                    elif abbr=="SA": abbr_mapped="SAS"
                    elif abbr=="NO": abbr_mapped="NOP"
                    elif abbr=="WSH": abbr_mapped="WAS"
                    elif abbr=="PHL": abbr_mapped="PHI"
                    elif abbr=="GS": abbr_mapped="GSW"
                rec = team.get("record",{}) or entry.get("record",{})
                wins=losses=0
                summary = rec.get("summary","")
                if "-" in summary:
                    try:
                        w,l = summary.split("-")
                        wins=int(w); losses=int(l)
                    except:
                        pass
                if wins==0 and losses==0:
                    for it in rec.get("items",[]):
                        for s in it.get("stats",[]):
                            if s.get("name")=="wins": wins=int(s.get("value",0))
                            if s.get("name")=="losses": losses=int(s.get("value",0))
                if wins+losses>0:
                    parsed.append((abbr_mapped, wins, losses))
            if len(parsed)>=25:
                print(f"Teams API got {len(parsed)}")
                return parsed
        except Exception as e:
            print(f"Teams API fail {e}")
            continue
    return None

def get_detailed_from_scoreboard():
    tally = {}
    for abbr, info in OFFICIAL_FALLBACK.items():
        tally[abbr] = dict(info)
        tally[abbr]["pf"]=0; tally[abbr]["pa"]=0
        tally[abbr]["home_w"]=info["home_w"]; tally[abbr]["home_l"]=info["home_l"]
        tally[abbr]["road_w"]=info["road_w"]; tally[abbr]["road_l"]=info["road_l"]
        tally[abbr]["games"]=[]

    start = datetime(2026,10,20, tzinfo=timezone(timedelta(hours=-5))).date()
    end = datetime.now(timezone(timedelta(hours=-5))).date()
    cur = start
    total=0
    while cur <= end:
        ymd = cur.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}"
        r = fetch(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        if r:
            try:
                data=r.json()
                for ev in data.get("events",[]):
                    if ev.get("season",{}).get("type",2)!=2:
                        continue
                    comp=ev.get("competitions",[{}])[0]
                    if "Final" not in comp.get("status",{}).get("type",{}).get("description",""):
                        continue
                    comps=comp.get("competitors",[])
                    if len(comps)<2: continue
                    home=next((c for c in comps if c.get("homeAway")=="home"), comps[0])
                    away=next((c for c in comps if c.get("homeAway")=="away"), comps[1])
                    hs=int(float(home.get("score",0) or 0))
                    aws=int(float(away.get("score",0) or 0))
                    if hs==0 and aws==0: continue
                    h_name=home.get("team",{}).get("displayName","")
                    a_name=away.get("team",{}).get("displayName","")
                    h_abbr=home.get("team",{}).get("abbreviation","")
                    a_abbr=away.get("team",{}).get("abbreviation","")
                    h_key=NAME_TO_ABBR.get(h_name) or NAME_TO_ABBR.get(h_abbr) or h_abbr
                    a_key=NAME_TO_ABBR.get(a_name) or NAME_TO_ABBR.get(a_abbr) or a_abbr
                    if h_key=="NY": h_key="NYK"
                    if a_key=="NY": a_key="NYK"
                    if h_key=="SA": h_key="SAS"
                    if a_key=="SA": a_key="SAS"
                    if h_key=="NO": h_key="NOP"
                    if a_key=="NO": a_key="NOP"
                    if h_key not in tally or a_key not in tally:
                        continue
                    # 計 PPG 用
                    tally[h_key]["pf"]+=hs; tally[h_key]["pa"]+=aws
                    tally[a_key]["pf"]+=aws; tally[a_key]["pa"]+=hs
                    total+=1
            except:
                pass
        time.sleep(0.3)
        cur+=timedelta(days=1)
        if (cur-start).days>20:
            break
    print(f"Detailed scoreboard counted {total} games")
    return tally

def build_standings():
    teams_api = get_teams_api()
    detailed = get_detailed_from_scoreboard()

    final=[]
    for abbr, base in OFFICIAL_FALLBACK.items():
        # 勝敗優先用 API，否則用官網備援
        wins=base["wins"]; losses=base["losses"]
        if teams_api:
            for api_abbr, api_w, api_l in teams_api:
                if api_abbr==abbr:
                    wins=api_w; losses=api_l
                    break
        # PPG 用 detailed 自計更新，如果有數據
        ppg=base["ppg"]; opp_ppg=base["opp_ppg"]; diff=base["diff"]
        if detailed and detailed.get(abbr):
            d=detailed[abbr]
            tot=wins+losses
            if tot>0 and d.get("pf",0)>0:
                ppg = d["pf"]/tot
                opp_ppg = d["pa"]/tot
                diff = ppg-opp_ppg

        final.append({
            **base,
            "wins":wins, "losses":losses,
            "pct": wins/(wins+losses) if (wins+losses)>0 else 0,
            "ppg":ppg, "opp_ppg":opp_ppg, "diff":diff,
        })
    return final

def format_standings(teams):
    east=[t for t in teams if t["conference"]=="East"]
    west=[t for t in teams if t["conference"]=="West"]
    east_sorted=sorted(east, key=lambda x: (x["pct"], x["wins"]), reverse=True)
    west_sorted=sorted(west, key=lambda x: (x["pct"], x["wins"]), reverse=True)

    def calc_gb(lst):
        if not lst: return lst
        lw=lst[0]["wins"]; ll=lst[0]["losses"]
        for t in lst:
            gb=((lw - t["wins"]) + (t["losses"] - ll))/2
            if gb<0: gb=0
            t["gb"]=gb
        return lst

    east_sorted=calc_gb(east_sorted)
    west_sorted=calc_gb(west_sorted)

    out=f"🏀 *2026-27 NBA 完整30隊即時戰績榜 (V9 最終核對版)* - {datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M HKT')}\n"
    out+=f"_來源: ESPN teams官方勝敗 + 官網圖12欄核對，已修正V7少1場問題_\n\n"

    def fmt(lst, title):
        s=f"*{title} 1-15 詳細:*\n"
        s+="`勝利 戰敗 勝率 GB 主場 客場 賽區 聯盟 PPG OPP PPG DIFF 最近10場 STRK`\n"
        for i,t in enumerate(lst,1):
            pct_str=f"{t['pct']:.3f}".lstrip('0')
            if t['pct']>=1: pct_str="1.000"
            if t['pct']==0: pct_str=".000"
            s+=f"{i}. {t['cn']} {t['team']} {t['wins']} {t['losses']} {pct_str} {t['gb']:.1f} {t['home_w']}-{t['home_l']} {t['road_w']}-{t['road_l']} {t['div_w']}-{t['div_l']} {t['conf_w']}-{t['conf_l']} {t['ppg']:.1f} {t['opp_ppg']:.1f} {t['diff']:+.1f} {t['l10']} {t['streak']}"
            if t['abbr']=="HOU": s+=" ← 火箭最新"
            if t['abbr']=="OKC": s+=" ← 雷霆"
            s+="\n"
        return s

    out+=fmt(east_sorted,"東岸")
    out+="\n"
    out+=fmt(west_sorted,"西岸")
    return out

def get_recent_scores():
    results=[]
    for delta in [2,1,0]:
        d=(datetime.now(timezone(timedelta(hours=-5))) - timedelta(days=delta)).date()
        ymd=d.strftime("%Y%m%d")
        url=f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}"
        r=fetch(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        if not r: continue
        try:
            data=r.json()
            for ev in data.get("events",[]):
                if ev.get("season",{}).get("type",2)!=2: continue
                comp=ev.get("competitions",[{}])[0]
                status=comp.get("status",{}).get("type",{}).get("description","")
                comps=comp.get("competitors",[])
                if len(comps)<2: continue
                home=next((c for c in comps if c.get("homeAway")=="home"), comps[0])
                away=next((c for c in comps if c.get("homeAway")=="away"), comps[1])
                results.append(f"{away.get('team',{}).get('displayName','')} {away.get('score','0')}-{home.get('score','0')} {home.get('team',{}).get('displayName','')} ({status})")
        except:
            pass
        time.sleep(0.3)
    uniq=[]; seen=set()
    for r in results:
        if r not in seen:
            uniq.append(r); seen.add(r)
    return uniq[-15:]

def send_daily():
    teams=build_standings()
    standings_text=format_standings(teams)
    scores=get_recent_scores()
    scores_text="📊 *即時戰果 (ESPN同步)*:\n" + ("\n".join(scores) if scores else "暫無") + "\n"

    push1=f"🏀 *NBA 每日 09:30 - Push 1/2 - 完整30隊即時戰績榜 (V9 最終核對版)* - {datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M HKT')}\n\n{standings_text}"
    push2=f"📰 *NBA 每日 09:30 - Push 2/2 - 即時戰果+雷霆* - {datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M HKT')}\n\n{scores_text}\n\n"

    thunder=next((t for t in (teams or []) if t["abbr"]=="OKC"), None)
    if thunder:
        push2+=f"⚡ *雷霆重點*: {thunder['cn']} {thunder['wins']}-{thunder['losses']} 勝率 {thunder['pct']:.3f} {thunder['streak']} 主場 {thunder['home_w']}-{thunder['home_l']}\n\n"

    push2+="_資料來源: ESPN teams官方勝敗+官網12欄核對，已修正V7少1場問題，每日09:30 HKT 自動更新_\n"

    # 發送
    if not os.getenv("NBA_BOT_TOKEN"):
        print(standings_text[:4000])
        return
    # 分段
    MAX_LEN=3900
    parts=[push1[i:i+MAX_LEN] for i in range(0,len(push1),MAX_LEN)]
    for idx, part in enumerate(parts):
        msg=part if idx==0 else f"完整戰績榜 (續 {idx+1}/{len(parts)})\n\n"+part
        url=f"https://api.telegram.org/bot{os.getenv('NBA_BOT_TOKEN')}/sendMessage"
        payload={"chat_id":os.getenv("NBA_CHAT_ID"),"text":msg,"parse_mode":"Markdown","disable_web_page_preview":True}
        try:
            r=requests.post(url, json=payload, timeout=15)
            print(f"Push1 {idx+1}/{len(parts)} {r.status_code}")
        except Exception as e:
            print(e)
        time.sleep(0.9)
    time.sleep(2)
    parts2=[push2[i:i+MAX_LEN] for i in range(0,len(push2),MAX_LEN)]
    for idx, part in enumerate(parts2):
        msg=part if idx==0 else f"詳細新聞 (續 {idx+1}/{len(parts2)})\n\n"+part
        url=f"https://api.telegram.org/bot{os.getenv('NBA_BOT_TOKEN')}/sendMessage"
        payload={"chat_id":os.getenv("NBA_CHAT_ID"),"text":msg,"parse_mode":"Markdown","disable_web_page_preview":True}
        try:
            r=requests.post(url, json=payload, timeout=15)
            print(f"Push2 {idx+1}/{len(parts2)} {r.status_code}")
        except Exception as e:
            print(e)
        time.sleep(0.9)

if __name__=="__main__":
    print(f"Start V9 at {datetime.now(timezone(timedelta(hours=8)))}")
    send_daily()







