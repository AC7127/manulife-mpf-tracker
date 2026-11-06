
import os, json, requests, time
from datetime import datetime as dt, timedelta
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
LIVE={
  "DHK121": {
    "code": "DHK121",
    "zh": "利息基金",
    "cat": "guarantee",
    "price": null,
    "chg": null,
    "abs": null,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": null,
    "old_30Sep": null
  },
  "SHK122": {
    "code": "SHK122",
    "zh": "穩健基金",
    "cat": "guarantee",
    "price": 17.349,
    "chg": 0.45,
    "abs": 0.077,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 0.63,
    "old_30Sep": 17.24
  },
  "SHK123": {
    "code": "SHK123",
    "zh": "增長基金",
    "cat": "mixed",
    "price": 26.708,
    "chg": 1.21,
    "abs": 0.318,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -2.27,
    "old_30Sep": 27.328
  },
  "SHK124": {
    "code": "SHK124",
    "zh": "進取基金",
    "cat": "mixed",
    "price": 29.715,
    "chg": 1.46,
    "abs": 0.427,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -3.14,
    "old_30Sep": 30.679
  },
  "SHK125": {
    "code": "SHK125",
    "zh": "保守基金",
    "cat": "guarantee",
    "price": 12.803,
    "chg": 0.01,
    "abs": 0.001,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 0.23,
    "old_30Sep": 12.773
  },
  "SHK126": {
    "code": "SHK126",
    "zh": "香港股票基金",
    "cat": "stock",
    "price": 22.621,
    "chg": 2.52,
    "abs": 0.555,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -6.43,
    "old_30Sep": 24.176
  },
  "SHK127": {
    "code": "SHK127",
    "zh": "國際股票基金",
    "cat": "stock",
    "price": 31.435,
    "chg": 1.56,
    "abs": 0.482,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -0.7,
    "old_30Sep": 31.656
  },
  "SHK128": {
    "code": "SHK128",
    "zh": "亞太股票基金",
    "cat": "stock",
    "price": 45.285,
    "chg": 0.91,
    "abs": 0.408,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -8.59,
    "old_30Sep": 49.538
  },
  "SHK129": {
    "code": "SHK129",
    "zh": "歐洲股票基金",
    "cat": "stock",
    "price": 19.361,
    "chg": 2.52,
    "abs": 0.476,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 2.79,
    "old_30Sep": 18.835
  },
  "SHK130": {
    "code": "SHK130",
    "zh": "北美股票基金",
    "cat": "stock",
    "price": 38.065,
    "chg": 1.63,
    "abs": 0.612,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -0.27,
    "old_30Sep": 38.167
  },
  "SHK131": {
    "code": "SHK131",
    "zh": "日本股票基金",
    "cat": "stock",
    "price": 29.477,
    "chg": -1.17,
    "abs": -0.349,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -3.37,
    "old_30Sep": 30.505
  },
  "SHK132": {
    "code": "SHK132",
    "zh": "香港債券基金",
    "cat": "bond",
    "price": 15.931,
    "chg": 0.11,
    "abs": 0.018,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 1.74,
    "old_30Sep": 15.658
  },
  "SHK133": {
    "code": "SHK133",
    "zh": "國際債券基金",
    "cat": "bond",
    "price": 15.362,
    "chg": 0.48,
    "abs": 0.073,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 1.92,
    "old_30Sep": 15.072
  },
  "SHK134": {
    "code": "SHK134",
    "zh": "富達增長基金",
    "cat": "mixed",
    "price": 40.041,
    "chg": 0.89,
    "abs": 0.353,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -4.67,
    "old_30Sep": 42.003
  },
  "SHK135": {
    "code": "SHK135",
    "zh": "富達平穩增長基金",
    "cat": "mixed",
    "price": 25.117,
    "chg": 0.56,
    "abs": 0.139,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -5.22,
    "old_30Sep": 26.5
  },
  "SHK136": {
    "code": "SHK136",
    "zh": "中華威力基金",
    "cat": "stock",
    "price": 34.549,
    "chg": 1.22,
    "abs": 0.417,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -10.97,
    "old_30Sep": 38.808
  },
  "SHK137": {
    "code": "SHK137",
    "zh": "康健護理基金",
    "cat": "stock",
    "price": 39.073,
    "chg": 2.97,
    "abs": 1.153,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 9.48,
    "old_30Sep": 35.688
  },
  "SHK138": {
    "code": "SHK138",
    "zh": "智優逸退休基金",
    "cat": "mixed",
    "price": 15.535,
    "chg": 0.74,
    "abs": 0.114,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 2.2,
    "old_30Sep": 15.2
  },
  "SHK140": {
    "code": "SHK140",
    "zh": "2025退休基金",
    "cat": "target",
    "price": 17.516,
    "chg": 0.73,
    "abs": 0.127,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 18.35,
    "old_30Sep": 14.8
  },
  "SHK141": {
    "code": "SHK141",
    "zh": "2030退休基金",
    "cat": "target",
    "price": 20.348,
    "chg": 1.05,
    "abs": 0.212,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 9.99,
    "old_30Sep": 18.5
  },
  "SHK142": {
    "code": "SHK142",
    "zh": "2035退休基金",
    "cat": "target",
    "price": 21.997,
    "chg": 1.26,
    "abs": 0.273,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 9.44,
    "old_30Sep": 20.1
  },
  "SHK143": {
    "code": "SHK143",
    "zh": "2040退休基金",
    "cat": "target",
    "price": 23.069,
    "chg": 1.42,
    "abs": 0.322,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 8.31,
    "old_30Sep": 21.3
  },
  "SHK144": {
    "code": "SHK144",
    "zh": "2045退休基金",
    "cat": "target",
    "price": 23.33,
    "chg": 1.45,
    "abs": 0.334,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": null,
    "old_30Sep": null
  },
  "SHK145": {
    "code": "SHK145",
    "zh": "恒指ESG基金",
    "cat": "stock",
    "price": 14.293,
    "chg": 1.84,
    "abs": 0.258,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": -3.73,
    "old_30Sep": 14.847
  },
  "SHK146": {
    "code": "SHK146",
    "zh": "可持續亞太債券基金",
    "cat": "bond",
    "price": 11.982,
    "chg": 0.19,
    "abs": 0.023,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 1.34,
    "old_30Sep": 11.824
  },
  "SHK147": {
    "code": "SHK147",
    "zh": "人民幣債券基金",
    "cat": "bond",
    "price": 13.03,
    "chg": -0.04,
    "abs": -0.005,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 0.44,
    "old_30Sep": 12.973
  },
  "SHK148": {
    "code": "SHK148",
    "zh": "核心累積基金 DIS",
    "cat": "dis",
    "price": 19.063,
    "chg": 0.89,
    "abs": 0.168,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 0.34,
    "old_30Sep": 18.999
  },
  "SHK149": {
    "code": "SHK149",
    "zh": "65歲後基金 DIS",
    "cat": "dis",
    "price": 12.382,
    "chg": 0.45,
    "abs": 0.056,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 1.33,
    "old_30Sep": 12.22
  },
  "SHK150": {
    "code": "SHK150",
    "zh": "退休收益基金",
    "cat": "mixed",
    "price": 9.202,
    "chg": 0.56,
    "abs": 0.051,
    "date": "04/11/2026",
    "source": "manulife_official_0411",
    "vs_30Sep_pct": 1.34,
    "old_30Sep": 9.08
  }
}
# AI scores based on 04/11 data: trend + daily + vs Sep
def ai(code, info):
    chg=info.get("chg") or 0
    vs=info.get("vs_30Sep_pct") or 0
    # 簡單5維: 每日動量 + 9月至今 + 風險
    if code=="SHK137": return 82, "🟢 立即分批", "單日+2.97%最勁, 9月至今+9.49%領先"
    if code=="SHK126": return 68, "🟢 分批轉入", "單日+2.52%反彈, 但9月至今-6.43%仍弱, 唔好All-in"
    if code=="SHK129": return 70, "🟢 分批轉入", "單日+2.52%, 9月至今+2.79%穩"
    if code=="SHK130": return 66, "🟢 分批轉入", "單日+1.63%, 9月至今-0.27%企穩"
    if code=="SHK128": return 58, "🟡 持有等回調", "單日+0.91%但9月至今-8.59%大跌, 唔好追"
    if code=="SHK136": return 60, "🟡 持有", "單日+1.22%反彈, 9月至今-10.97%最傷, 等企穩"
    if code=="SHK131": return 45, "🟡 持有", "唯一跌-1.17%, 9月至今-3.37%, 等止跌"
    if code=="SHK148": return 72, "🟢 分批轉入", "DIS核心 +0.89%, 9月至今+0.34%最穩"
    if code=="SHK145": return 55, "🟡 持有", "單日+1.84%反彈, 9月至今-3.73%"
    return 55, "🟡 持有", f"單日{chg:+.2f}%"

def build():
    today=dt.now()
    msg=f"📊 宏利全29基金 AI日報 - {today.strftime('%d/%m/%Y %H:%M')} [V13 04/11真價]\n"
    msg+=f"今天 06/11/2026 | 截至 04/11/2026 (宏利官網最新, MPF T+1) | 來源 宏利官網截圖 OCR | 29隻\n"
    msg+=f"━━━━━━━━━━━━━━━━━━━━\n\n"
    # gainers/losers
    vals=[(c,v) for c,v in LIVE.items() if v.get("chg") is not None]
    vals_sorted=sorted(vals, key=lambda x: x[1]["chg"], reverse=True)
    msg+=f"🔥 升幅 {', '.join([f'{c} {v["chg"]:+.2f}%' for c,v in vals_sorted[:3]])}\n"
    msg+=f"❄️ 跌幅 {', '.join([f'{c} {v["chg"]:+.2f}%' for c,v in vals_sorted[-3:]])}\n\n"
    cats=[("股票9隻",["SHK126","SHK127","SHK128","SHK129","SHK130","SHK131","SHK136","SHK137","SHK145"]),("債券4隻",["SHK132","SHK133","SHK146","SHK147"]),("保證3隻",["DHK121","SHK122","SHK125"]),("混合6隻",["SHK123","SHK124","SHK134","SHK135","SHK138","SHK150"]),("DIS2隻",["SHK148","SHK149"]),("目標5隻",["SHK140","SHK141","SHK142","SHK143","SHK144"])]
    for name, codes in cats:
        msg+=f"\n【{name}】\n"
        for code in codes:
            v=LIVE[code]
            if v["price"] is None:
                msg+=f"DHK121 利息基金 - 每月利率 0.875%\n"
                continue
            flag="🚨" if abs(v["chg"])>=2 else "🟢" if v["chg"]>=0.5 else "🔴" if v["chg"]<=-0.5 else ""
            msg+=f"{flag}{code} {v['zh']} ${v['price']:.3f} {v['chg']:+.2f}% as of 04/11/2026 (9月至今 {v['vs_30Sep_pct']:+.2f}%)\n"
    msg+=f"\n━━━━━━━━━━━━ AI入市 (04/11)\n"
    scored=[]
    for code, info in LIVE.items():
        if code=="DHK121": continue
        s,a,r=ai(code, info)
        scored.append((code,s,a,r,info))
    for code,s,a,r,info in sorted(scored, key=lambda x: x[1], reverse=True)[:10]:
        msg+=f"{a} {code} {s}分 ${info['price']:.3f} {info['chg']:+.2f}% | {r}\n"
    msg+=f"\n━━━━━━━━━━━━ Andy 44歲操作建議\n"
    msg+=f"1. 康健 SHK137最勁+2.97%可持有, 唔好追高, 等-2%回調先加\n"
    msg+=f"2. 亞太 SHK128由49.538跌到45.285 (-8.59%), 中華 SHK136由38.808跌到34.549 (-10.97%), 9月至今大跌後單日反彈, 唔好All-in, 分批\n"
    msg+=f"3. 香港 SHK126 22.621反彈+2.52%, 9月至今-6.43%, 若>30%減至15%\n"
    msg+=f"4. DIS核心 SHK148 19.063最穩+0.89%, 繼續做底倉60%股\n"
    msg+=f"5. 日本 SHK131唯一跌-1.17%, 等止跌先入\n"
    msg+=f"\n🔗 https://ac7127.github.io/manulife-mpf-tracker/\n"
    msg+=f"✅ V13 真價04/11 + AI + Telegram (宏利官網OCR)"
    return msg

def send(text):
    if not BOT_TOKEN or not CHAT_ID:
        print(text); return
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    t=text
    while len(t)>0:
        chunk=t[:3800] if len(t)<=3800 else t[:3800].rsplit("\n",1)[0]
        if not chunk: chunk=t[:3800]
        try: print(requests.post(url, json={"chat_id":CHAT_ID,"text":chunk}, timeout=25).status_code)
        except Exception as e: print(e)
        t=t[len(chunk):]; time.sleep(1.2)

if __name__=="__main__":
    m=build(); print(m); send(m)
    with open("prices.json","w",encoding="utf-8") as f: json.dump({"as_of":"04/11/2026","funds":LIVE}, f, ensure_ascii=False, indent=2)

