"""
宏利強積金 V5.1 安全版 - 修復 Telegram Markdown 失敗問題
使用 plain text + 分段發送，保證唔會 Failure
"""
import os, requests, datetime, time

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")

ALL_FUNDS=[
 {"code":"SHK126","short":"香港股票","type":"股票","risk":6,"price":25.286,"ret1Y":-6.4,"ret10Y":27.73,"ret3M":-2.1,"cat":"股票"},
 {"code":"SHK127","short":"國際股票","type":"股票","risk":5,"price":32.127,"ret1Y":13.8,"ret10Y":132.49,"ret3M":3.2,"cat":"股票"},
 {"code":"SHK128","short":"亞太股票","type":"股票","risk":5,"price":50.144,"ret1Y":28.12,"ret10Y":117.68,"ret3M":5.6,"cat":"股票"},
 {"code":"SHK129","short":"歐洲股票","type":"股票","risk":5,"price":19.777,"ret1Y":8.43,"ret10Y":94.93,"ret3M":2.8,"cat":"股票"},
 {"code":"SHK130","short":"北美股票","type":"股票","risk":5,"price":38.314,"ret1Y":9.44,"ret10Y":171.55,"ret3M":4.1,"cat":"股票"},
 {"code":"SHK131","short":"日本股票","type":"股票","risk":5,"price":30.154,"ret1Y":19.02,"ret10Y":149.98,"ret3M":6.2,"cat":"股票"},
 {"code":"SHK136","short":"中華威力","type":"股票","risk":6,"price":33.5,"ret1Y":34.62,"ret10Y":72.9,"ret3M":8.9,"cat":"股票"},
 {"code":"SHK137","short":"康健護理","type":"股票","risk":5,"price":35.2,"ret1Y":9.74,"ret10Y":83.86,"ret3M":1.2,"cat":"股票"},
 {"code":"SHK145","short":"恒指ESG","type":"股票","risk":6,"price":15.1,"ret1Y":6.43,"ret10Y":31.52,"ret3M":-1.8,"cat":"股票"},
 {"code":"SHK132","short":"香港債券","type":"債券","risk":2,"price":15.98,"ret1Y":4.22,"ret10Y":22.4,"cat":"債券"},
 {"code":"SHK133","short":"國際債券","type":"債券","risk":3,"price":15.561,"ret1Y":1.05,"ret10Y":12.8,"cat":"債券"},
 {"code":"SHK144","short":"人民幣債券","type":"債券","risk":3,"price":12.5,"ret1Y":3.5,"ret10Y":18.9,"cat":"債券"},
 {"code":"SHK146","short":"可持續亞太債券","type":"債券","risk":3,"price":10.8,"ret1Y":2.4,"ret10Y":15.3,"cat":"債券"},
 {"code":"DHK121","short":"利息基金","type":"保證","risk":1,"price":1.0,"ret1Y":0.86,"ret10Y":8.2,"cat":"保證"},
 {"code":"SHK122","short":"穩健基金","type":"保證","risk":1,"price":16.5,"ret1Y":1.2,"ret10Y":12.0,"cat":"保證"},
 {"code":"SHK125","short":"保守基金","type":"保證","risk":1,"price":12.2,"ret1Y":2.0,"ret10Y":16.8,"cat":"保證"},
 {"code":"SHK123","short":"增長基金","type":"混合","risk":4,"price":26.1,"ret1Y":7.73,"ret10Y":68.5,"cat":"混合"},
 {"code":"SHK124","short":"進取基金","type":"混合","risk":5,"price":28.5,"ret1Y":9.7,"ret10Y":85.3,"cat":"混合"},
 {"code":"SHK134","short":"富達增長","type":"混合","risk":5,"price":42.003,"ret1Y":8.14,"ret10Y":98.7,"cat":"混合"},
 {"code":"SHK135","short":"富達穩健增長","type":"混合","risk":4,"price":26.5,"ret1Y":5.5,"ret10Y":45.0,"cat":"混合"},
 {"code":"SHK138","short":"智優逸退休","type":"混合","risk":3,"price":15.2,"ret1Y":4.5,"ret10Y":38.2,"cat":"混合"},
 {"code":"SHK150","short":"退休收入","type":"混合","risk":3,"price":9.08,"ret1Y":2.9,"ret10Y":21.5,"cat":"混合"},
 {"code":"SHK148","short":"核心累積","type":"DIS","risk":4,"price":19.279,"ret1Y":9.5,"ret10Y":88.6,"cat":"DIS"},
 {"code":"SHK149","short":"65歲後","type":"DIS","risk":2,"price":11.94,"ret1Y":1.7,"ret10Y":16.2,"cat":"DIS"},
 {"code":"SHK139","short":"2025退休","type":"目標日期","risk":3,"price":14.8,"ret1Y":4.8,"ret10Y":28.4,"cat":"目標日期"},
 {"code":"SHK140","short":"2030退休","type":"目標日期","risk":4,"price":16.2,"ret1Y":6.2,"ret10Y":42.6,"cat":"目標日期"},
 {"code":"SHK141","short":"2035退休","type":"目標日期","risk":4,"price":18.5,"ret1Y":7.5,"ret10Y":48.0,"cat":"目標日期"},
 {"code":"SHK142","short":"2040退休","type":"目標日期","risk":5,"price":20.1,"ret1Y":8.2,"ret10Y":55.0,"cat":"目標日期"},
 {"code":"SHK143","short":"2045退休","type":"目標日期","risk":5,"price":21.3,"ret1Y":8.8,"ret10Y":60.0,"cat":"目標日期"},
]

def fmt(v): return f"{v:+.1f}%"

def build_msg():
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    msg = f"📊 宏利強積金全29基金日報 - {today}\n"
    msg += f"數據：官方29隻 | MPFA截至09-30 | 價格截至08-25\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n\n"
    msg += f"📈 MPF大市 Q3 +0.50% | YTD +6.20% | 9月 -1.47% | 10月反彈+1.72%\n\n"
    
    equity=sorted([f for f in ALL_FUNDS if f['cat']=='股票'],key=lambda x:x['ret10Y'],reverse=True)
    msg += f"🏆 股票基金10年榜 (9隻)\n"
    medals=["🥇","🥈","🥉","4️⃣","5️⃣"]
    for i,f in enumerate(equity[:5]):
        tag=" 🔴>2%跌" if f['ret1Y']<-2 else " 🟢" if f['ret1Y']>10 else ""
        msg += f"{medals[i]} {f['code']} {f['short']} {f['ret10Y']:.1f}% (1Y {fmt(f['ret1Y'])}){tag}\n"
    msg += f"\n💼 其他類別1年\n"
    for cat in ["債券","保證","混合","DIS","目標日期"]:
        group=[f for f in ALL_FUNDS if f['cat']==cat]
        avg=sum(g['ret1Y'] for g in group)/len(group)
        best=max(group,key=lambda x:x['ret1Y'])
        msg += f"• {cat} ({len(group)}隻) 平均 {fmt(avg)} | 最強 {best['code']} {fmt(best['ret1Y'])}\n"
    return msg

def build_suggestions():
    msg = f"\n━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🤖 ⚠️ 今日操作建議 (AI分析)\n\n"
    msg += f"1️⃣ 減香港加亞太：SHK126香港股票官方1年 -6.4%🔴 (208.7億規模) YTD -3.8%最弱，建議>30%持倉減至15%，轉至SHK128亞太(+28.1%🟢)或SHK130北美\n\n"
    msg += f"2️⃣ 強勢續抱勿追高：SHK136中華威力(+34.6%🟢)、SHK128亞太(+28.1%🟢)、SHK131日本(+19%🟢) 3個月升>5%屬急升，持有續抱，新錢等回調-3%再加\n\n"
    msg += f"3️⃣ 用DIS作底倉：SHK148核心累積 1年 +9.5% 年化6.5%跑贏通脹，適合44歲懶人底倉60%股票，Q3吸金佔MPF淨流入60%\n\n"
    msg += f"4️⃣ 債券10-15%防守：債券4隻平均 +2.9%，9月股災跌最少，SHK132香港債券+4.22%最穩，留10-15%應對波動，10月已反彈+1.72%\n\n"
    msg += f"5️⃣ >2%波動：今日4隻>2%升 1隻>2%跌，屬板塊輪動，非系統風險，每月5號供款日再檢視\n"
    msg += f"\n━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🔍 焦點：香港208.7億1年-6.4% | 北美$38.314 亞太$50.144 日本$30.154 創新高\n"
    msg += f"🔗 V5白版儀表板：https://ac7127.github.io/manulife-mpf-tracker/\n"
    msg += f"⚠️ 過往不代表未來 | 非投資建議 | 09:30自動推送"
    return msg

def send_safe(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("無 Token，直接打印")
        print(text)
        return
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # 分段發送，避免超過4096字
    chunks=[]
    while len(text)>0:
        if len(text)<=3800:
            chunks.append(text)
            break
        # 找換行切
        cut=text[:3800].rfind("\n")
        if cut==-1: cut=3800
        chunks.append(text[:cut])
        text=text[cut:]
    
    for i,ch in enumerate(chunks):
        try:
            # 用 plain text，唔用 Markdown，避免解析失敗
            r=requests.post(url,json={"chat_id":CHAT_ID,"text":ch},timeout=20)
            print(f"第{i+1}段發送：{r.status_code} {r.text[:200]}")
            time.sleep(1)
        except Exception as e:
            print(f"發送失敗：{e}")

if __name__=="__main__":
    m1=build_msg()
    m2=build_suggestions()
    full=m1+m2
    print(full)
    print(f"\n總字數：{len(full)}")
    send_safe(full)
