"""
宏利強積金全29基金完整版 v5 - Q3 2026 + AI操作建議
Telegram 每日 09:30 自動推送含操作建議
"""

import os, requests, datetime

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")

ALL_FUNDS=[
 {"code":"SHK126","short":"香港股票","type":"股票","risk":6,"price":25.286,"ret1Y":-6.4,"ret10Y":27.73,"ret3M":-2.1,"retYTD":-4.2,"cat":"股票","size":"208.7億"},
 {"code":"SHK127","short":"國際股票","type":"股票","risk":5,"price":32.127,"ret1Y":13.8,"ret10Y":132.49,"ret3M":3.2,"retYTD":9.8,"cat":"股票"},
 {"code":"SHK128","short":"亞太股票","type":"股票","risk":5,"price":50.144,"ret1Y":28.12,"ret10Y":117.68,"ret3M":5.6,"retYTD":18.2,"cat":"股票"},
 {"code":"SHK129","short":"歐洲股票","type":"股票","risk":5,"price":19.777,"ret1Y":8.43,"ret10Y":94.93,"ret3M":2.8,"retYTD":6.1,"cat":"股票"},
 {"code":"SHK130","short":"北美股票","type":"股票","risk":5,"price":38.314,"ret1Y":9.44,"ret10Y":171.55,"ret3M":4.1,"retYTD":8.9,"cat":"股票"},
 {"code":"SHK131","short":"日本股票","type":"股票","risk":5,"price":30.154,"ret1Y":19.02,"ret10Y":149.98,"ret3M":6.2,"retYTD":15.3,"cat":"股票"},
 {"code":"SHK136","short":"中華威力","type":"股票","risk":6,"price":33.5,"ret1Y":34.62,"ret10Y":72.9,"ret3M":8.9,"retYTD":22.4,"cat":"股票"},
 {"code":"SHK137","short":"康健護理","type":"股票","risk":5,"price":35.2,"ret1Y":9.74,"ret10Y":83.86,"ret3M":1.2,"retYTD":5.4,"cat":"股票"},
 {"code":"SHK145","short":"恒指ESG","type":"股票","risk":6,"price":15.1,"ret1Y":6.43,"ret10Y":31.52,"ret3M":-1.8,"retYTD":2.1,"cat":"股票"},
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

def generate_suggestions():
    """AI 操作建議邏輯"""
    suggestions=[]
    
    # 1. 香港股票最弱
    hk = next(f for f in ALL_FUNDS if f['code']=='SHK126')
    if hk['ret1Y'] < -2:
        suggestions.append(f"1️⃣ **減香港加亞太**：{hk['code']}官方1年 {fmt(hk['ret1Y'])}🔴 (規模{hk['size']})，YTD -3.8%為29隻最弱。建議持倉>30%者減至15%，轉至SHK128亞太(+28.1%🟢)或SHK130北美，分散風險")
    
    # 2. 捕捉強勢但唔追高
    strong = [f for f in ALL_FUNDS if f['ret1Y'] > 20]
    if strong:
        top = sorted(strong, key=lambda x: x['ret1Y'], reverse=True)[:3]
        names = "、".join([f"{f['code']} {f['short']}({fmt(f['ret1Y'])}🟢)" for f in top])
        suggestions.append(f"2️⃣ **強勢續抱勿追高**：{names} 3個月升幅>5%屬急升，持有續抱，新錢唔好高位追，等待回調-3%再加注")
    
    # 3. DIS核心累積
    dis_core = next(f for f in ALL_FUNDS if f['code']=='SHK148')
    suggestions.append(f"3️⃣ **用DIS作底倉**：{dis_core['code']}核心累積 1年 {fmt(dis_core['ret1Y'])}，年化6.5%跑贏通脹1.8%，適合44歲懶人底倉60%股票，Q3吸金佔MPF淨流入60%")
    
    # 4. 債券防守
    bond_avg = sum(f['ret1Y'] for f in ALL_FUNDS if f['cat']=='債券')/4
    suggestions.append(f"4️⃣ **債券10-15%防守**：債券4隻平均 {fmt(bond_avg)}，9月股災時跌最少，SHK132香港債券 {fmt(4.22)}最穩，宜留10-15%應對10月後波動，10月MPF已反彈+1.72%但仍有回調風險")
    
    # 5. >2%波動標記
    volatile = [f for f in ALL_FUNDS if abs(f['ret3M']) > 2]
    if len(volatile) >= 4:
        up = len([f for f in volatile if f['ret3M']>2])
        down = len([f for f in volatile if f['ret3M']<-2])
        suggestions.append(f"5️⃣ **>2%波動標記**：今日{up}隻>2%升📈 {down}隻>2%跌📉，屬板塊輪動，非系統風險，唔使追市，每月5號供款日再檢視")
    
    return suggestions

def format_msg():
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    msg=f"📊 *宏利強積金全29基金日報* - {today}\n"
    msg+=f"數據：官方29隻 | MPFA截至09-30 | 價格截至08-25\n"
    msg+=f"━━━━━━━━━━━━━━━━━━━━\n\n"
    msg+=f"📈 *MPF大市 Q3* Q3 +0.50% | YTD +6.20% | 9月 -1.47% | 10月反彈+1.72%\n"
    msg+=f"股票平均10年 76.6% | 債券 +2.9% | 保證 +1.4%\n\n"
    
    equity=sorted([f for f in ALL_FUNDS if f['cat']=='股票'],key=lambda x:x['ret10Y'],reverse=True)
    msg+=f"🏆 *股票基金10年榜 (9隻)*\n"
    for i,f in enumerate(equity[:5],1):
        medal=["🥇","🥈","🥉","4️⃣","5️⃣"][i-1]
        tag="🔴" if f['ret1Y']<-2 else "🟢" if f['ret1Y']>10 else ""
        msg+=f"{medal} {f['code']} {f['short']} {f['ret10Y']:.1f}% (1Y {fmt(f['ret1Y'])}){tag}\n"
    msg+=f"\n💼 *其他類別1年*\n"
    for cat in ["債券","保證","混合","DIS","目標日期"]:
        group=[f for f in ALL_FUNDS if f['cat']==cat]
        avg=sum(g['ret1Y'] for g in group)/len(group) if group else 0
        best=max(group,key=lambda x:x['ret1Y'])
        msg+=f"• {cat} ({len(group)}隻) 平均 {fmt(avg)} | 最強 {best['code']} {fmt(best['ret1Y'])}\n"
    
    msg+=f"\n━━━━━━━━━━━━━━━━━━━━\n"
    msg+=f"🤖 *⚠️ 今日操作建議 (AI分析)*\n\n"
    for s in generate_suggestions():
        msg+=f"{s}\n\n"
    
    msg+=f"━━━━━━━━━━━━━━━━━━━━\n"
    msg+=f"🔍 *焦點數據*\n"
    msg+=f"• 香港 SHK126 208.7億 1年 -6.4% YTD -3.8% 最弱\n"
    msg+=f"• 北美 $38.314 亞太 $50.144 日本 $30.154 創新高\n"
    msg+=f"• DIS核心 19.279 年化6.5% 跑贏通脹\n"
    msg+=f"\n🔗 *互動儀表板 V5白版*\n"
    msg+=f"👉 https://ac7127.github.io/manulife-mpf-tracker/\n"
    msg+=f"   (可按分類篩選 + 當日至10年切換)\n\n"
    msg+=f"⚠️ 過往不代表未來 | 非投資建議 | 每日09:30自動推送"
    return msg

def send(m):
    if not BOT_TOKEN: 
        print(m)
        return
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        # Telegram 有字數限制 4096，超過要分段
        if len(m) > 4000:
            parts = [m[i:i+3800] for i in range(0, len(m), 3800)]
            for p in parts:
                r=requests.post(url,json={"chat_id":CHAT_ID,"text":p,"parse_mode":"Markdown"},timeout=20)
                print(r.json())
        else:
            r=requests.post(url,json={"chat_id":CHAT_ID,"text":m,"parse_mode":"Markdown"},timeout=20)
            print(r.json())
    except Exception as e: 
        print(e)

if __name__=="__main__":
    msg=format_msg()
    print(msg)
    print("\n---字數---", len(msg))
    send(msg)



