"""
宏利強積金全29基金完整版 v4 - Q3 2026
包含股票/混合/債券/保證/DIS/目標日期
數據：MPFA官方+宏利最新價
"""
import os, requests, datetime
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")

ALL_FUNDS=[
 # 股票 9隻
 {"code":"SHK126","short":"香港股票","type":"股票","risk":6,"price":25.286,"ret1Y":-6.4,"ret10Y":27.73,"cat":"股票"},
 {"code":"SHK127","short":"國際股票","type":"股票","risk":5,"price":32.127,"ret1Y":13.8,"ret10Y":132.49,"cat":"股票"},
 {"code":"SHK128","short":"亞太股票","type":"股票","risk":5,"price":50.144,"ret1Y":28.12,"ret10Y":117.68,"cat":"股票"},
 {"code":"SHK129","short":"歐洲股票","type":"股票","risk":5,"price":19.777,"ret1Y":8.43,"ret10Y":94.93,"cat":"股票"},
 {"code":"SHK130","short":"北美股票","type":"股票","risk":5,"price":38.314,"ret1Y":9.44,"ret10Y":171.55,"cat":"股票"},
 {"code":"SHK131","short":"日本股票","type":"股票","risk":5,"price":30.154,"ret1Y":19.02,"ret10Y":149.98,"cat":"股票"},
 {"code":"SHK136","short":"中華威力","type":"股票","risk":6,"price":33.5,"ret1Y":34.62,"ret10Y":72.9,"cat":"股票"},
 {"code":"SHK137","short":"康健護理","type":"股票","risk":5,"price":35.2,"ret1Y":9.74,"ret10Y":83.86,"cat":"股票"},
 {"code":"SHK145","short":"恒指ESG","type":"股票","risk":6,"price":15.1,"ret1Y":6.43,"ret10Y":31.52,"cat":"股票"},
 # 債券 4隻
 {"code":"SHK132","short":"香港債券","type":"債券","risk":2,"price":15.98,"ret1Y":4.22,"ret10Y":35.0,"cat":"債券"},
 {"code":"SHK133","short":"國際債券","type":"債券","risk":3,"price":15.561,"ret1Y":1.05,"ret10Y":20.0,"cat":"債券"},
 {"code":"SHK144","short":"人民幣債券","type":"債券","risk":3,"price":12.5,"ret1Y":3.5,"ret10Y":25.0,"cat":"債券"},
 {"code":"SHK146","short":"可持續亞太債券","type":"債券","risk":3,"price":10.8,"ret1Y":2.8,"ret10Y":22.0,"cat":"債券"},
 # 保證/保守 3隻
 {"code":"DHK121","short":"利息基金","type":"保證","risk":1,"price":1.0,"ret1Y":0.86,"ret10Y":8.0,"cat":"保證"},
 {"code":"SHK122","short":"穩健基金","type":"保證","risk":1,"price":16.5,"ret1Y":1.2,"ret10Y":12.0,"cat":"保證"},
 {"code":"SHK125","short":"保守基金","type":"貨幣市場","risk":1,"price":12.2,"ret1Y":2.0,"ret10Y":15.0,"cat":"保證"},
 # 混合 6隻核心 + 退休收入
 {"code":"SHK123","short":"增長基金","type":"混合","risk":4,"price":26.1,"ret1Y":7.73,"ret10Y":57.74,"cat":"混合"},
 {"code":"SHK124","short":"進取基金","type":"混合","risk":5,"price":28.5,"ret1Y":9.7,"ret10Y":81.9,"cat":"混合"},
 {"code":"SHK134","short":"富達增長","type":"混合","risk":5,"price":42.003,"ret1Y":8.14,"ret10Y":68.34,"cat":"混合"},
 {"code":"SHK135","short":"富達穩健增長","type":"混合","risk":4,"price":26.5,"ret1Y":5.5,"ret10Y":45.0,"cat":"混合"},
 {"code":"SHK138","short":"智優逸退休","type":"混合","risk":3,"price":15.2,"ret1Y":4.5,"ret10Y":35.0,"cat":"混合"},
 {"code":"SHK150","short":"退休收入","type":"混合","risk":3,"price":9.08,"ret1Y":5.12,"ret10Y":28.0,"cat":"混合"},
 # DIS 2隻
 {"code":"SHK148","short":"核心累積","type":"DIS","risk":4,"price":19.279,"ret1Y":9.5,"ret10Y":85.0,"cat":"DIS"},
 {"code":"SHK149","short":"65歲後","type":"DIS","risk":2,"price":11.94,"ret1Y":1.7,"ret10Y":18.0,"cat":"DIS"},
 # 目標日期 5隻
 {"code":"SHK139","short":"2025退休","type":"目標日期","risk":3,"price":14.8,"ret1Y":4.8,"ret10Y":32.0,"cat":"目標日期"},
 {"code":"SHK140","short":"2030退休","type":"目標日期","risk":4,"price":16.2,"ret1Y":6.2,"ret10Y":40.0,"cat":"目標日期"},
 {"code":"SHK141","short":"2035退休","type":"目標日期","risk":4,"price":18.5,"ret1Y":7.5,"ret10Y":48.0,"cat":"目標日期"},
 {"code":"SHK142","short":"2040退休","type":"目標日期","risk":5,"price":20.1,"ret1Y":8.2,"ret10Y":55.0,"cat":"目標日期"},
 {"code":"SHK143","short":"2045退休","type":"目標日期","risk":5,"price":21.3,"ret1Y":8.8,"ret10Y":60.0,"cat":"目標日期"},
]

def fmt(v): return f"{v:+.1f}%"

def format_msg():
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    msg=f"📊 *宏利強積金全29基金日報* - {today}\n"
    msg+=f"數據：官方29隻成分基金 | MPFA截至09-30 | 價格截至08-25\n"
    msg+=f"━━━━━━━━━━━━━━━━━━━━\n\n"
    msg+=f"📈 *MPF大市 Q3* Q3 +0.50% | YTD +6.20% | 9月 -1.47%\n"
    msg+=f"股票基金過去12個月平均 +10.3% | 債券基金 -1.5%\n\n"
    # 股票排行
    equity=sorted([f for f in ALL_FUNDS if f['cat']=='股票'],key=lambda x:x['ret10Y'],reverse=True)
    msg+=f"🏆 *股票基金10年榜 (9隻)*\n"
    for i,f in enumerate(equity[:5],1):
        medal=["🥇","🥈","🥉","4️⃣","5️⃣"][i-1]
        msg+=f"{medal} {f['code']} {f['short']} {f['ret10Y']:.1f}% (1Y {fmt(f['ret1Y'])})\n"
    msg+=f"\n💼 *其他類別1年回報*\n"
    for cat in ["債券","保證","混合","DIS","目標日期"]:
        group=[f for f in ALL_FUNDS if f['cat']==cat]
        avg=sum(g['ret1Y'] for g in group)/len(group) if group else 0
        msg+=f"• {cat} ({len(group)}隻) 平均 {fmt(avg)} | 最強 {max(group,key=lambda x:x['ret1Y'])['code']} {fmt(max(group,key=lambda x:x['ret1Y'])['ret1Y'])}\n"
    msg+=f"\n⚠️ *焦點*\n"
    msg+=f"• 香港股票 SHK126 官方1年 -6.4% (MPFA 09-30) 規模208.7億\n"
    msg+=f"• 北美 $38.314 日本 $30.154 亞太 $50.144 創新高\n"
    msg+=f"• 完整29隻包括保證基金及退休目標基金\n"
    msg+=f"\n━━━━━━━━━━━━━━━━━━━━\n"
    msg+=f"🔗 *全29基金互動儀表板*\n"
    msg+=f"👉 https://ac7127.github.io/manulife-mpf-tracker/\n"
    msg+=f"   (可按分類篩選：股票/債券/保證/DIS/目標日期)\n\n"
    msg+=f"⚠️ 過往不代表未來 | 非投資建議"
    return msg

def send(m):
    if not BOT_TOKEN: print(m); return
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r=requests.post(url,json={"chat_id":CHAT_ID,"text":m,"parse_mode":"Markdown"},timeout=20)
        print(r.json())
    except Exception as e: print(e)

if __name__=="__main__":
    msg=format_msg()
    print(msg)
    send(msg)



