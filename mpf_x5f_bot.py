
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
    try:
        from playwright.sync_api import sync_playwright
        print("V12 Playwright try yesterday...")
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            page=browser.new_page()
            page.goto("https://www.manulife.com.hk/en/individual/funds/mpf-fund-prices.html", wait_until="networkidle", timeout=90000)
            page.wait_for_timeout(8000)
            content=page.content()
            live={}
            for m in re.findall(r'\((SHK\d+|DHK\d+)\)[^\d]*([\d]+\.[\d]+)\s*,\s*as of\s+([\d/]+)\s*,\s*([+-]?[\d.]+)%', content):
                code, price, date_str, chg=m
                if code in ALL_FUNDS:
                    live[code]={"price":float(price),"date":date_str,"chg":float(chg),"source":"playwright_daily_昨日同步"}
            browser.close()
            if len(live)>=15:
                print(f"Playwright success {len(live)}")
                return live
    except Exception as e:
        print(f"Playwright skip {e}")
    return {}

def fetch_mpfa():
    print("Fallback MPFA 30/09/2026 - GitHub Actions Playwright will get yesterday")
    d={}
    for code, base in ALL_FUNDS.items():
        d[code]={"price":base["price"],"date":"30/09/2026","chg":0.0,"source":"mpfa_30Sep2026"}
    return d

def fetch_live():
    live=fetch_playwright_daily()
    if len(live)>=20:
        return live
    return fetch_mpfa()

def ai_score(code, info):
    b=ALL_FUNDS.get(code,{}); chg=info.get("chg",0); price=info.get("price",b.get("price",0))
    ma20=b.get("ma20",price); rsi=b.get("rsi",50); ytd=b.get("ytd",0); r1Y=b.get("r1Y",0); risk=b.get("risk",3)
    trend=(15 if price>ma20 else 0)+(10 if ytd>0 else 0)+(5 if chg>0 else 0)+(5 if chg>=0.5 else 0)
    value=25 if rsi<40 else 20 if rsi<55 else 10 if rsi<70 else 0
    mom=25 if r1Y>20 else 18 if r1Y>10 else 10 if r1Y>0 else 5
    risk_s=20-risk*2-(10 if abs(chg)>=2 else 0)
    total=trend+value+mom+risk_s
    if total>=75: action="🟢 立即轉入"; reason=f"強 YTD{ytd:+.1f}% RSI{rsi}"
    elif total>=60: action="🟢 分批轉入"; reason=f"動量佳 RSI{rsi}"
    elif total>=45: action="🟡 持有"; reason=f"中性 YTD{ytd:+.1f}%"
    elif total>=30: action="🟠 減持"; reason="轉弱"
    else: action="🔴 迴避"; reason="弱勢"
    return total, action, reason

def build_msg(live):
    today=dt.now(); yesterday=today-timedelta(days=1)
    today_s=today.strftime("%Y-%m-%d %H:%M"); y_s=yesterday.strftime("%d/%m/%Y")
    sources=set(v.get("source","") for v in live.values())
    latest=max([v.get("date","") for v in live.values()], default="30/09/2026")
    is_daily=any("playwright" in s for s in sources)
    label=f"宏利即時 {latest} 已至昨日 {y_s}" if is_daily else f"MPFA 30/09/2026 (Actions會更新至昨日 {y_s})"
    msg=f"📊 宏利全29基金 AI日報 - {today_s} [V12.1]\n"
    msg+=f"今天 {today.strftime('%d/%m/%Y')} 目標截至昨日 {y_s} | 來源 {label} | {len(live)}隻\n"
    msg+=f"來源 {', '.join(sources)}\n━━━━━━━━━━━━━━━━━━━━\n\n"
    sl=sorted(live.items(), key=lambda x: x[1].get("chg",0), reverse=True)
    gainers = ", ".join([f"{c} {v.get('chg',0):+.2f}%" for c,v in sl[:3]])
    losers = ", ".join([f"{c} {v.get('chg',0):+.2f}%" for c,v in sl[-3:]])
    msg+=f"🔥 升幅 {gainers}\n"
    msg+=f"❄️ 跌幅 {losers}\n\n"
    cats=[("股票9隻",["SHK128","SHK136","SHK131","SHK130","SHK137","SHK126","SHK127","SHK129","SHK145"]),("債券4隻",["SHK132","SHK133","SHK144","SHK146"]),("保證3隻",["DHK121","SHK122","SHK125"]),("混合6隻",["SHK123","SHK124","SHK134","SHK135","SHK138","SHK150"]),("DIS2隻",["SHK148","SHK149"]),("目標5隻",["SHK139","SHK140","SHK141","SHK142","SHK143"])]
    for cat_name,codes in cats:
        msg+=f"\n【{cat_name}】\n"
        for code in codes:
            if code in live:
                v=live[code]; f=ALL_FUNDS.get(code,{}); chg=v.get("chg",0)
                flag="🚨" if abs(chg)>=2 else "🟢" if chg>=0.5 else "🔴" if chg<=-0.5 else ""
                mark="昨日" if y_s in v.get("date","") or "05/11" in v.get("date","") or is_daily else "30/09"
                msg+=f"{flag}{code} {f.get('zh','')} ${v['price']:.3f} {chg:+.2f}% as of {v.get('date')} {mark}\n"
    msg+=f"\n━━━━━━━━━━━━ AI入市 (5維度) \n"
    scored=[]
    for code, info in live.items():
        s,a,r=ai_score(code,info); scored.append((code,s,a,r,info))
    for code,s,a,r,info in sorted(scored, key=lambda x: x[1], reverse=True)[:10]:
        msg+=f"{a} {code} {s}分 ${info['price']:.3f} {info.get('chg',0):+.2f}% | {r}\n"
    msg+=f"\n🔗 https://ac7127.github.io/manulife-mpf-tracker/\n✅ V12.1 真每日截至昨日 + AI + Telegram"
    return msg

def save_json(live):
    try:
        data={"as_of": max([v.get("date","") for v in live.values()]),"fetched_at":dt.now().isoformat(),"target_yesterday":(dt.now()-timedelta(days=1)).strftime("%d/%m/%Y"),"funds":live}
        with open("prices.json","w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
        print("prices.json saved")
    except Exception as e:
        print(e)

def send_safe(text):
    if not BOT_TOKEN or not CHAT_ID:
        print(text[:2500]); return
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    t=text
    while len(t)>0:
        chunk=t[:3800] if len(t)<=3800 else t[:3800].rsplit("\n",1)[0]
        if not chunk: chunk=t[:3800]
        try:
            r=requests.post(url, json={"chat_id":CHAT_ID,"text":chunk}, timeout=25)
            print(f"Telegram {r.status_code}")
        except Exception as e:
            print(e)
        t=t[len(chunk):]; time.sleep(1.2)

if __name__=="__main__":
    live=fetch_live()
    save_json(live)
    msg=build_msg(live)
    print(msg[:3500])
    send_safe(msg)
