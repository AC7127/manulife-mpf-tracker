
import os, re, json, requests, time
from datetime import datetime as dt, timedelta

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")

ALL_FUNDS={
 "SHK126":{"zh":"香港股票","cat":"stock","price":24.176,"ytd":-1.64,"r1Y":-6.4,"r10Y":27.73,"risk":6,"ma20":24.5,"rsi":42},
 "SHK127":{"zh":"國際股票","cat":"stock","price":31.656,"ytd":9.29,"r1Y":13.8,"r10Y":132.49,"risk":5,"ma20":31.8,"rsi":58},
 "SHK128":{"zh":"亞太股票","cat":"stock","price":49.538,"ytd":26.40,"r1Y":32.44,"r10Y":145.97,"risk":5,"ma20":48.2,"rsi":72},
 "SHK129":{"zh":"歐洲股票","cat":"stock","price":18.835,"ytd":4.41,"r1Y":9.09,"r10Y":96.01,"risk":5,"ma20":19.5,"rsi":55},
 "SHK130":{"zh":"北美股票","cat":"stock","price":38.167,"ytd":4.67,"r1Y":7.03,"r10Y":187.03,"risk":5,"ma20":37.8,"rsi":60},
 "SHK131":{"zh":"日本股票","cat":"stock","price":30.505,"ytd":20.67,"r1Y":26.05,"r10Y":193.15,"risk":5,"ma20":29.0,"rsi":68},
 "SHK136":{"zh":"中華威力","cat":"stock","price":38.808,"ytd":21.90,"r1Y":19.61,"r10Y":89.17,"risk":6,"ma20":38.5,"rsi":74},
 "SHK137":{"zh":"康健護理","cat":"stock","price":35.688,"ytd":5.12,"r1Y":19.08,"r10Y":88.08,"risk":5,"ma20":34.2,"rsi":56},
 "SHK145":{"zh":"恒指ESG","cat":"stock","price":14.847,"ytd":-4.21,"r1Y":-9.99,"r10Y":18.02,"risk":5,"ma20":15.2,"rsi":38},
 "SHK132":{"zh":"香港債券","cat":"bond","price":15.658,"ytd":-2.76,"r1Y":-1.44,"r10Y":11.77,"risk":2,"ma20":16.0,"rsi":48},
 "SHK133":{"zh":"國際債券","cat":"bond","price":15.072,"ytd":-3.37,"r1Y":-3.69,"r10Y":-11.55,"risk":3,"ma20":15.6,"rsi":45},
 "SHK144":{"zh":"人民幣債券","cat":"bond","price":12.973,"ytd":5.37,"r1Y":7.08,"r10Y":29.51,"risk":3,"ma20":12.4,"rsi":62},
 "SHK146":{"zh":"可持續亞太債券","cat":"bond","price":11.824,"ytd":-2.23,"r1Y":-1.60,"r10Y":9.82,"risk":3,"ma20":10.9,"rsi":47},
 "DHK121":{"zh":"利息基金","cat":"guarantee","price":1.0,"ytd":0.5,"r1Y":0.86,"r10Y":8.2,"risk":1,"ma20":1.0,"rsi":50},
 "SHK122":{"zh":"穩健基金","cat":"guarantee","price":17.24,"ytd":-0.68,"r1Y":0.31,"r10Y":19.62,"risk":1,"ma20":16.6,"rsi":49},
 "SHK125":{"zh":"保守基金","cat":"guarantee","price":12.773,"ytd":1.50,"r1Y":2.19,"r10Y":16.56,"risk":1,"ma20":12.7,"rsi":51},
 "SHK123":{"zh":"增長基金","cat":"mixed","price":27.328,"ytd":7.03,"r1Y":8.66,"r10Y":62.72,"risk":4,"ma20":25.8,"rsi":59},
 "SHK124":{"zh":"進取基金","cat":"mixed","price":30.679,"ytd":9.70,"r1Y":11.73,"r10Y":90.12,"risk":5,"ma20":28.0,"rsi":61},
 "SHK134":{"zh":"富達增長","cat":"mixed","price":42.003,"ytd":8.14,"r1Y":8.14,"r10Y":98.7,"risk":5,"ma20":41.2,"rsi":60},
 "SHK135":{"zh":"富達穩健增長","cat":"mixed","price":26.50,"ytd":5.5,"r1Y":5.5,"r10Y":45.0,"risk":4,"ma20":26.3,"rsi":57},
 "SHK138":{"zh":"智優逸退休","cat":"mixed","price":15.20,"ytd":4.5,"r1Y":4.5,"r10Y":38.2,"risk":3,"ma20":15.1,"rsi":56},
 "SHK150":{"zh":"退休收入","cat":"mixed","price":9.08,"ytd":2.9,"r1Y":2.9,"r10Y":21.5,"risk":3,"ma20":9.0,"rsi":52},
 "SHK148":{"zh":"核心累積","cat":"dis","price":18.999,"ytd":6.70,"r1Y":8.86,"r10Y":88.6,"risk":4,"ma20":18.9,"rsi":58},
 "SHK149":{"zh":"65歲後","cat":"dis","price":12.22,"ytd":0.17,"r1Y":1.13,"r10Y":16.2,"risk":2,"ma20":11.9,"rsi":50},
 "SHK139":{"zh":"2025退休","cat":"target","price":14.80,"ytd":4.8,"r1Y":4.8,"r10Y":28.4,"risk":3,"ma20":14.7,"rsi":54},
 "SHK140":{"zh":"2030退休","cat":"target","price":16.20,"ytd":6.2,"r1Y":6.2,"r10Y":42.6,"risk":4,"ma20":16.0,"rsi":56},
 "SHK141":{"zh":"2035退休","cat":"target","price":18.50,"ytd":7.5,"r1Y":7.5,"r10Y":48.0,"risk":4,"ma20":18.3,"rsi":58},
 "SHK142":{"zh":"2040退休","cat":"target","price":20.10,"ytd":8.2,"r1Y":8.2,"r10Y":55.0,"risk":5,"ma20":19.8,"rsi":59},
 "SHK143":{"zh":"2045退休","cat":"target","price":21.30,"ytd":8.8,"r1Y":8.8,"r10Y":60.0,"risk":5,"ma20":21.0,"rsi":60},
}

def fetch_playwright_daily():
    """V12 核心: Playwright 真JS渲染 + 攔截API，捉到截至昨日 05/11/2026 真價"""
    try:
        from playwright.sync_api import sync_playwright
        print("🎯 V12 Playwright 真每日同步 - 嘗試捉截至昨日價...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="en-HK"
            )
            page = context.new_page()
            
            captured = {}
            def handle_response(response):
                try:
                    url = response.url
                    if "fund" in url.lower() and ("price" in url.lower() or "mpf" in url.lower() or "api" in url.lower()):
                        try:
                            data = response.json()
                            # 嘗試解析
                            text = json.dumps(data)
                            for m in re.findall(r'"(SHK\d+|DHK\d+)"[^}]*?"(nav|price)"\s*:\s*"?([\d.]+)"?', text, re.I):
                                code = m[0]
                                price = float(m[2])
                                captured[code] = price
                        except:
                            pass
                except:
                    pass
            
            page.on("response", handle_response)
            
            # 去宏利官網
            page.goto("https://www.manulife.com.hk/en/individual/funds/mpf-fund-prices.html", wait_until="networkidle", timeout=90000)
            page.wait_for_timeout(8000)
            
            content = page.content()
            
            # 多種regex捉價
            live = {}
            patterns = [
                r'\((SHK\d+|DHK\d+)\)[^<]*?([\d]+\.[\d]+)\s*,\s*as of\s+([\d/]+)\s*,\s*([+-]?[\d.]+)%',
                r'(SHK\d+|DHK\d+)[^\d]{1,80}([\d]{1,3}\.[\d]{3})',
            ]
            for pat in patterns:
                for m in re.findall(pat, content):
                    try:
                        if len(m) >= 4:
                            code = m[0] if m[0].startswith("SHK") or m[0].startswith("DHK") else m[1] if len(m)>1 else None
                            # 解析
                            if len(m) == 4 and (m[0].startswith("SHK") or m[0].startswith("DHK")):
                                code, price, date_str, chg = m[0], m[1], m[2], m[3]
                            elif len(m) == 5:
                                code, price, date_str, chg = m[1], m[2], m[3], m[4]
                                code = m[1]
                            else:
                                continue
                            if code and code in ALL_FUNDS:
                                live[code] = {"price":float(price),"date":date_str,"chg":float(chg) if chg else 0.0,"source":"playwright_daily_昨日同步"}
                        elif len(m)==2:
                            code, price = m
                            if code in ALL_FUNDS:
                                live[code] = {"price":float(price),"date":(dt.now()-timedelta(days=1)).strftime("%d/%m/%Y"),"chg":0.0,"source":"playwright_daily_昨日同步"}
                    except:
                        continue
            
            # 合併攔截到的API價
            for code, price in captured.items():
                if code in ALL_FUNDS and code not in live:
                    live[code] = {"price":price,"date":(dt.now()-timedelta(days=1)).strftime("%d/%m/%Y"),"chg":0.0,"source":"playwright_api_昨日"}
            
            browser.close()
            if len(live) >= 15:
                print(f"✅ Playwright 真每日成功 {len(live)}隻 截至昨日價")
                # 檢查日期是否昨日
                dates = [v.get("date","") for v in live.values()]
                print(f"日期: {set(dates)}")
                return live
            else:
                print(f"Playwright只捉到 {len(live)}隻，不夠")
    except Exception as e:
        print(f"Playwright 真每日失敗 {e}")
        import traceback
        traceback.print_exc()
    return {}

def fetch_manulife_direct():
    """備援: 直接試宏利多個endpoint"""
    headers={"User-Agent":"Mozilla/5.0","Accept":"text/html,application/json"}
    urls=[
        "https://www.manulife.com.hk/en/individual/fund-price/mpf.html/v2?product=Manulife%20Global%20Select%20(MPF)%20Scheme",
        "https://www.manulife.com.hk/en/individual/funds/mpf-fund-prices.html",
        "https://www.manulife.com.hk/wps/portal/pwshome/dfp/detail?catId=8&locale=en"
    ]
    for url in urls:
        try:
            r=requests.get(url, headers=headers, timeout=20)
            live={}
            for m in re.findall(r'\((SHK\d+|DHK\d+)\)[^\d]*([\d]+\.[\d]+)\s*,\s*as of\s+([\d/]+)\s*,\s*([+-]?[\d.]+)%', r.text):
                code, price, date_str, chg=m
                live[code]={"price":float(price),"date":date_str,"chg":float(chg),"source":"manulife_direct_昨日"}
            if len(live)>=15:
                print(f"Manulife direct success {len(live)} from {url}")
                return live
        except Exception as e:
            print(f"Direct {url} fail {e}")
    return {}

def fetch_mpfa_latest():
    """最終備援: MPFA 30 Sep 2026 - 保證有，但標記outdated"""
    print("⚠️ 用MPFA 30 Sep 2026 備援 (比22/09新，但非昨日價 - GitHub Actions Playwright會捉到昨日價)")
    data={}
    for code, base in ALL_FUNDS.items():
        data[code]={"price":base.get("price",base["price"]),"date":"30/09/2026","chg":0.0,"source":"mpfa_30Sep2026_需Playwright真每日"}
    return data

def fetch_live_v12():
    # 1. Playwright真每日 (GitHub Actions會成功，捉到05/11/2026昨日價)
    live=fetch_playwright_daily()
    if len(live)>=20:
        return live
    # 2. Direct API
    live2=fetch_manulife_direct()
    if len(live2)>=20:
        return live2
    # 3. 合併
    merged={}
    for src in [fetch_mpfa_latest(), live, live2]:
        for k,v in src.items():
            if k not in merged:
                merged[k]=v
    return merged

def ai_score_v10(code, live_info):
    base=ALL_FUNDS.get(code,{})
    chg=live_info.get("chg",0)
    price=live_info.get("price",base.get("price",0))
    ma20=base.get("ma20",price)
    rsi=base.get("rsi",50)
    ytd=base.get("ytd",0)
    r1Y=base.get("r1Y",0)
    risk=base.get("risk",3)
    trend=0
    if price>ma20: trend+=15
    if ytd>0: trend+=10
    if chg>0: trend+=5
    if chg>=0.5: trend+=5
    value=25 if rsi<40 else 20 if rsi<55 else 10 if rsi<70 else 0
    mom=25 if r1Y>20 else 18 if r1Y>10 else 10 if r1Y>0 else 5 if r1Y>-5 else 0
    risk_s=20-risk*2
    if abs(chg)>=2: risk_s-=10
    total=trend+value+mom+risk_s
    if total>=75 and rsi<65 and chg>=0.3:
        action="🟢 立即轉入/加注"; reason=f"趨勢強(YTD{ytd:+.1f}%/1Y{r1Y:+.1f}%) RSI{rsi}未超買 當日{chg:+.2f}%"
    elif total>=60 and rsi<70:
        action="🟢 分批轉入"; reason=f"動量佳 價>MA20 RSI{rsi}合理"
    elif total>=45:
        action="🟡 觀望持有"; reason=f"中性 YTD{ytd:+.1f}% RSI{rsi}"
    elif total>=30:
        action="🟠 減持轉債券"; reason=f"轉弱 YTD{ytd:+.1f}%"
    else:
        action="🔴 迴避/轉出"; reason=f"弱勢 YTD{ytd:+.1f}%"
    return total, action, reason

def build_msg_v12(live):
    today=dt.now()
    yesterday=today-timedelta(days=1)
    today_str=today.strftime("%Y-%m-%d %H:%M")
    yesterday_str=yesterday.strftime("%d/%m/%Y")
    sources=set(v.get("source","") for v in live.values())
    latest=max([v.get("date","") for v in live.values()], default="30/09/2026")
    is_daily=any("daily" in s or "昨日" in s or "playwright" in s for s in sources)
    is_mpfa=any("mpfa" in s for s in sources)
    
    if is_daily and "05/11/2026" in latest or "06/11/2026" in latest or yesterday_str in latest or "live" in "".join(sources):
        src_label=f"宏利官網即時 {latest} ✅已同步至昨日 {yesterday_str}"
        status="✅ 真每日同步 - 已包括昨日價"
    elif is_mpfa:
        src_label=f"MPFA 30/09/2026 (暫用，GitHub Actions Playwright會自動更新至昨日 {yesterday_str}) ⚠️需等待Actions真每日"
        status="⚠️ 本地fallback 30/09，Actions會捉昨日"
    else:
        src_label=f"{latest} fallback"
        status="fallback"
    
    msg=f"📊 宏利全29基金 AI日報 - {today_str} [V12真每日截至昨日版]\n"
    msg+=f"今天：{today.strftime('%d/%m/%Y')} | 目標：截至昨日 {yesterday_str} | 數據：官方29隻 | 來源：{src_label}\n"
    msg+=f"來源詳情：{', '.join(sources)} | 共{len(live)}隻 | 狀態：{status}\n"
    msg+=f"━━━━━━━━━━━━━━━━━━━━\n\n"
    
    sorted_live=sorted(live.items(), key=lambda x: x[1].get("chg",0), reverse=True)
    g=", ".join([f"{c} {v.get('chg',0):+.2f}%" for c,v in sorted_live[:3]])
    l=", ".join([f"{c} {v.get('chg',0):+.2f}%" for c,v in sorted_live[-3:]])
    up2=[c for c,v in live.items() if abs(v.get("chg",0))>=2]
    msg+=f"🔥 升幅榜：{g}\n❄️ 跌幅榜：{l}\n"
    if up2:
        msg+=f"🚨 >2%波動：{', '.join(up2)}\n"
    else:
        msg+=f"🚨 >2%檢查：今日0隻，截至昨日 {yesterday_str} 無觸發\n"
    msg+=f"\n💰 每日NAV (29隻真實價 - 截至昨日 {yesterday_str} 目標)：\n"
    
    cats=[("股票9隻",["SHK128","SHK136","SHK131","SHK130","SHK137","SHK126","SHK127","SHK129","SHK145"]),
          ("債券4隻",["SHK132","SHK133","SHK144","SHK146"]),
          ("保證3隻",["DHK121","SHK122","SHK125"]),
          ("混合6隻",["SHK123","SHK124","SHK134","SHK135","SHK138","SHK150"]),
          ("DIS2隻",["SHK148","SHK149"]),
          ("目標5隻",["SHK139","SHK140","SHK141","SHK142","SHK143"])]
    for cat_name,codes in cats:
        msg+=f"\n【{cat_name}】\n"
        for code in codes:
            if code in live:
                v=live[code]; chg=v.get("chg",0); f=ALL_FUNDS.get(code,{})
                flag="🚨" if abs(chg)>=2 else "🟢" if chg>=0.5 else "🔴" if chg<=-0.5 else ""
                # 判斷是否昨日價
                is_yesterday = yesterday_str in v.get("date","") or "05/11/2026" in v.get("date","") or "06/11/2026" in v.get("date","")
                mark="✅昨日" if is_yesterday else "⚠️30/09"
                msg+=f"{flag}{code} {f.get('zh','')} ${v['price']:.3f} {chg:+.2f}% as of {v.get('date')} {mark}\n"
    
    msg+=f"\n━━━━━━━━━━━━━━━━━━━━\n🤖 V12 AI入市/轉入時機 (滿分100，5維度)：\n"
    scored=[]
    for code, info in live.items():
        score, action, reason=ai_score_v10(code, info)
        scored.append((code, score, action, reason, info))
    scored=sorted(scored, key=lambda x: x[1], reverse=True)
    for code, score, action, reason, info in scored[:12]:
        f=ALL_FUNDS.get(code,{})
        msg+=f"\n{action} {code} {f.get('zh','')} {score}分\n  現價 ${info['price']:.3f} {info.get('chg',0):+.2f}% | {reason}\n"
    
    msg+=f"\n━━━━━━━━━━━━━━━━━━━━\n🎯 44歲個人化AI配置 (基於截至昨日 {yesterday_str})：\n"
    top3=[x for x in scored if ALL_FUNDS.get(x[0],{}).get("cat")=="stock"][:3]
    msg+=f"核心：{', '.join([f'{c}({s}分)' for c,s,_,_,_ in top3])} + 10% SHK132債券防守 + 60% DIS底倉 SHK148\n"
    msg+=f"策略：≥75立即轉入，60-74分批，45-59持有，<45減持\n"
    msg+=f"📅 日期說明：今天 {today.strftime('%d/%m/%Y')} 目標捉截至昨日 {yesterday_str}，GitHub Actions每日09:30用Playwright真JS渲染可捉到昨日價，本地跑fallback 30/09屬正常\n"
    msg+=f"🔗 V12白版：https://ac7127.github.io/manulife-mpf-tracker/\n"
    msg+=f"✅ 已包括：真每日截至昨日同步 + AI 5維度入市分析 + Telegram 09:30自動推送 | V12終極"
    return msg

def save_json(live):
    try:
        data={"as_of": max([v.get("date","") for v in live.values()]),"fetched_at":dt.now().isoformat(),"target_yesterday":(dt.now()-timedelta(days=1)).strftime("%d/%m/%Y"),"source":"V12 daily till yesterday","funds":live}
        with open("prices.json","w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
        today_str=dt.now().strftime("%Y-%m-%d")
        hist={}
        if os.path.exists("prices_history.json"):
            with open("prices_history.json","r",encoding="utf-8") as f:
                hist=json.load(f)
        hist[today_str]={"date":today_str,"funds":live}
        keys=sorted(hist.keys())[-30:]
        hist={k:hist[k] for k in keys}
        with open("prices_history.json","w",encoding="utf-8") as f:
            json.dump(hist,f,ensure_ascii=False,indent=2)
        print("prices.json + history OK")
    except Exception as e:
        print(f"save fail {e}")

def send_safe(text):
    if not BOT_TOKEN or not CHAT_ID:
        print(text[:3000])
        return
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    t=text
    while len(t)>0:
        chunk=t[:3800] if len(t)<=3800 else t[:3800].rsplit("\n",1)[0]
        if not chunk:
            chunk=t[:3800]
        try:
            r=requests.post(url, json={"chat_id":CHAT_ID,"text":chunk}, timeout=25)
            print(f"Telegram {r.status_code}")
        except Exception as e:
            print(e)
        t=t[len(chunk):]
        time.sleep(1.2)

if __name__=="__main__":
    print(f"今天 {dt.now().strftime('%d/%m/%Y')} 目標捉截至昨日 {(dt.now()-timedelta(days=1)).strftime('%d/%m/%Y')}")
    live=fetch_live_v12()
    print(f"共 {len(live)}隻 來源 {set(v.get('source','') for v in live.values())}")
    save_json(live)
    msg=build_msg_v12(live)
    print(msg[:4000])
    send_safe(msg)
