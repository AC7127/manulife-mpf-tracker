"""
宏利強積金監控代理 - GitHub Actions 自動化版 v2 (排版優化)
每日 09:00 HKT 自動推送到 Telegram
數據來源：Manulife Global Select MPF Scheme (截至 2026-03-31)
優化：手機友好排版 + 互動儀表板連結
"""
import os
import requests
import datetime

# 從環境變數讀取 (GitHub Secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("請設定 BOT_TOKEN 和 CHAT_ID 環境變數")
    BOT_TOKEN = BOT_TOKEN or "YOUR_BOT_TOKEN"
    CHAT_ID = CHAT_ID or "YOUR_CHAT_ID"

MPF_FUNDS = [
    {"name": "宏利MPF康健護理基金", "short": "康健護理", "code": "SHK137", "risk": 5, "price": 32.875, "type": "股票", "ret": {"3M": -3.17, "YTD": -3.17, "1Y": 9.74, "3Y": 20.04, "5Y": 29.23, "10Y": 83.86, "3Y_ann": 6.28, "5Y_ann": 5.26, "10Y_ann": 6.28}},
    {"name": "宏利MPF亞太股票基金", "short": "亞太股票", "code": "SHK128", "risk": 5, "price": 40.081, "type": "股票", "ret": {"3M": 2.27, "YTD": 2.27, "1Y": 28.12, "3Y": 44.06, "5Y": 20.45, "10Y": 117.68, "3Y_ann": 12.94, "5Y_ann": 3.79, "10Y_ann": 8.09}},
    {"name": "宏利MPF中華威力基金", "short": "中華威力", "code": "SHK136", "risk": 6, "price": 32.451, "type": "股票", "ret": {"3M": 1.93, "YTD": 1.93, "1Y": 34.62, "3Y": 37.48, "5Y": -7.64, "10Y": 72.90, "3Y_ann": 11.19, "5Y_ann": -1.58, "10Y_ann": 5.63}},
    {"name": "宏利MPF香港股票基金", "short": "香港股票", "code": "SHK126", "risk": 6, "price": 23.946, "type": "股票", "ret": {"3M": -2.58, "YTD": -2.58, "1Y": 12.85, "3Y": 21.07, "5Y": -19.32, "10Y": 42.72, "3Y_ann": 6.58, "5Y_ann": -4.20, "10Y_ann": 3.62}},
    {"name": "宏利MPF恒指ESG基金", "short": "恒指ESG", "code": "SHK145", "risk": 6, "price": 14.504, "type": "股票", "ret": {"3M": -6.43, "YTD": -6.43, "1Y": 6.43, "3Y": 14.76, "5Y": -14.23, "10Y": 31.52, "3Y_ann": 4.69, "5Y_ann": -3.02, "10Y_ann": 2.78}},
    {"name": "宏利MPF日本股票基金", "short": "日本股票", "code": "SHK131", "risk": 5, "price": 24.848, "type": "股票", "ret": {"3M": -1.70, "YTD": -1.70, "1Y": 19.02, "3Y": 68.02, "5Y": 61.45, "10Y": 149.98, "3Y_ann": 18.88, "5Y_ann": 10.05, "10Y_ann": 9.59}},
    {"name": "宏利MPF歐洲股票基金", "short": "歐洲股票", "code": "SHK129", "risk": 6, "price": 17.308, "type": "股票", "ret": {"3M": -4.05, "YTD": -4.05, "1Y": 8.43, "3Y": 11.84, "5Y": 9.22, "10Y": 94.93, "3Y_ann": 3.80, "5Y_ann": 1.78, "10Y_ann": 6.90}},
    {"name": "宏利MPF北美股票基金", "short": "北美股票", "code": "SHK130", "risk": 5, "price": 33.422, "type": "股票", "ret": {"3M": -8.34, "YTD": -8.34, "1Y": 9.44, "3Y": 51.17, "5Y": 38.70, "10Y": 171.55, "3Y_ann": 14.77, "5Y_ann": 6.76, "10Y_ann": 10.51}},
    {"name": "宏利MPF國際股票基金", "short": "國際股票", "code": "SHK127", "risk": 5, "price": 27.613, "type": "股票", "ret": {"3M": -4.66, "YTD": -4.66, "1Y": 13.80, "3Y": 43.61, "5Y": 28.46, "10Y": 132.49, "3Y_ann": 12.82, "5Y_ann": 5.14, "10Y_ann": 8.80}},
    {"name": "宏利MPF進取基金", "short": "進取基金", "code": "SHK124", "risk": 5, "price": 27.374, "type": "混合", "ret": {"3M": -2.11, "YTD": -2.11, "1Y": 15.79, "3Y": 32.03, "5Y": 9.35, "10Y": 81.90, "3Y_ann": 9.70, "5Y_ann": 1.80, "10Y_ann": 6.17}},
    {"name": "宏利MPF增長基金", "short": "增長基金", "code": "SHK123", "risk": 4, "price": 25.066, "type": "混合", "ret": {"3M": -1.83, "YTD": -1.83, "1Y": 12.73, "3Y": 25.04, "5Y": 4.80, "10Y": 57.74, "3Y_ann": 7.73, "5Y_ann": 0.94, "10Y_ann": 4.66}},
    {"name": "宏利MPF富達增長基金", "short": "富達增長", "code": "SHK134", "risk": 5, "price": 37.379, "type": "混合", "ret": {"3M": -2.54, "YTD": -2.54, "1Y": 13.66, "3Y": 26.45, "5Y": 4.43, "10Y": 68.34, "3Y_ann": 8.14, "5Y_ann": 0.87, "10Y_ann": 5.35}},
]

def fmt(v):
    return f"{v:+.1f}%"

def format_detailed_message():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    msg = f"📊 *宏利強積金監控日報* - {today}\n"
    msg += f"數據：宏利官方 Q1 2026 | 自動推送 09:00 HKT\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n\n"
    
    msg += f"🏆 *10年回報排行榜*\n"
    sorted_10y = sorted(MPF_FUNDS, key=lambda x: x['ret']['10Y'], reverse=True)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    for i, f in enumerate(sorted_10y[:5], 0):
        r = f['ret']
        msg += f"{medals[i]} {f['code']} {f['short']} {r['10Y']:.1f}% (年化{r['10Y_ann']:.1f}%)\n"
    
    msg += f"\n━━━━━━━━━━━━━━━━━━━━\n\n"
    msg += f"📈 *詳細回報 - 手機優化版*\n\n"
    
    for f in sorted_10y:
        r = f['ret']
        msg += f"🔹 *{f['code']} {f['short']}*\n"
        msg += f"   {f['type']} | 風險{f['risk']} | ${f['price']}\n"
        msg += f"   3M {fmt(r['3M'])} | 1Y {fmt(r['1Y'])} | 3Y {fmt(r['3Y'])}\n"
        msg += f"   5Y {fmt(r['5Y'])} | 10Y {r['10Y']:.1f}% (年{r['10Y_ann']:.1f}%)\n\n"
    
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"💡 *今日洞察*\n"
    best_1y = max(MPF_FUNDS, key=lambda x: x['ret']['1Y'])
    worst_1y = min(MPF_FUNDS, key=lambda x: x['ret']['1Y'])
    best_10y = max(MPF_FUNDS, key=lambda x: x['ret']['10Y'])
    worst_3m = min(MPF_FUNDS, key=lambda x: x['ret']['3M'])
    
    msg += f"• 1年最強: {best_1y['short']} {fmt(best_1y['ret']['1Y'])}\n"
    msg += f"• 1年最弱: {worst_1y['short']} {fmt(worst_1y['ret']['1Y'])}\n"
    msg += f"• 長線王: {best_10y['code']} 10年 +{best_10y['ret']['10Y']:.1f}%\n"
    msg += f"• 短期最弱: {worst_3m['short']} 3M {fmt(worst_3m['ret']['3M'])}\n"
    
    msg += f"\n━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"🔗 *互動儀表板*\n"
    msg += f"👉 https://ac7127.github.io/manulife-mpf-tracker/\n"
    msg += f"   (入去睇圖表 + 完整數據)\n\n"
    msg += f"📊 MPF整體2025平均 +6.2~7.55%，連續第4年正回報\n"
    msg += f"⚠️ 過往不代表未來 | 非投資建議"
    
    return msg

def send_telegram(message):
    if not BOT_TOKEN or "YOUR" in BOT_TOKEN:
        print("❌ 未設定 BOT_TOKEN")
        print(message)
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=20)
        result = resp.json()
        if result.get("ok"):
            print(f"✅ Telegram 推送成功! Message ID: {result['result']['message_id']}")
            return True
        else:
            print(f"❌ 推送失敗: {result}")
            payload["parse_mode"] = None
            resp2 = requests.post(url, json=payload, timeout=20)
            print(f"重試純文本: {resp2.json()}")
            return False
    except Exception as e:
        print(f"❌ 網絡錯誤: {e}")
        return False

if __name__ == "__main__":
    message = format_detailed_message()
    print(message)
    print("\n" + "="*50 + "\n")
    send_telegram(message)

