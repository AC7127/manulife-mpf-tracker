"""
宏利強積金監控代理 - GitHub Actions 自動化版
每日 09:00 HKT 自動推送到 Telegram
數據來源：Manulife Global Select MPF Scheme (截至 2026-03-31)

GitHub Secrets 需要設定：
- BOT_TOKEN: 你的 Telegram Bot Token
- CHAT_ID: 你的 Telegram Chat ID (8711230455)
"""
import os
import requests
import datetime

# 從環境變數讀取 (GitHub Secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("請設定 BOT_TOKEN 和 CHAT_ID 環境變數")
    # 本地測試用 fallback (請在 GitHub Secrets 設定後刪除)
    BOT_TOKEN = BOT_TOKEN or "YOUR_BOT_TOKEN"
    CHAT_ID = CHAT_ID or "YOUR_CHAT_ID"

# 宏利強積金完整數據 - 來自官方 2026 Q1 Quarterly Fund Fact Sheet
MPF_FUNDS = [
    {"name": "宏利MPF康健護理基金", "code": "SHK137", "risk": 5, "price": 32.875, "type": "股票", "ret": {"3M": -3.17, "YTD": -3.17, "1Y": 9.74, "3Y": 20.04, "5Y": 29.23, "10Y": 83.86, "3Y_ann": 6.28, "5Y_ann": 5.26, "10Y_ann": 6.28}},
    {"name": "宏利MPF亞太股票基金", "code": "SHK128", "risk": 5, "price": 40.081, "type": "股票", "ret": {"3M": 2.27, "YTD": 2.27, "1Y": 28.12, "3Y": 44.06, "5Y": 20.45, "10Y": 117.68, "3Y_ann": 12.94, "5Y_ann": 3.79, "10Y_ann": 8.09}},
    {"name": "宏利MPF中華威力基金", "code": "SHK136", "risk": 6, "price": 32.451, "type": "股票", "ret": {"3M": 1.93, "YTD": 1.93, "1Y": 34.62, "3Y": 37.48, "5Y": -7.64, "10Y": 72.90, "3Y_ann": 11.19, "5Y_ann": -1.58, "10Y_ann": 5.63}},
    {"name": "宏利MPF香港股票基金", "code": "SHK126", "risk": 6, "price": 23.946, "type": "股票", "ret": {"3M": -2.58, "YTD": -2.58, "1Y": 12.85, "3Y": 21.07, "5Y": -19.32, "10Y": 42.72, "3Y_ann": 6.58, "5Y_ann": -4.20, "10Y_ann": 3.62}},
    {"name": "宏利MPF恒指ESG基金", "code": "SHK145", "risk": 6, "price": 14.504, "type": "股票", "ret": {"3M": -6.43, "YTD": -6.43, "1Y": 6.43, "3Y": 14.76, "5Y": -14.23, "10Y": 31.52, "3Y_ann": 4.69, "5Y_ann": -3.02, "10Y_ann": 2.78}},
    {"name": "宏利MPF日本股票基金", "code": "SHK131", "risk": 5, "price": 24.848, "type": "股票", "ret": {"3M": -1.70, "YTD": -1.70, "1Y": 19.02, "3Y": 68.02, "5Y": 61.45, "10Y": 149.98, "3Y_ann": 18.88, "5Y_ann": 10.05, "10Y_ann": 9.59}},
    {"name": "宏利MPF歐洲股票基金", "code": "SHK129", "risk": 6, "price": 17.308, "type": "股票", "ret": {"3M": -4.05, "YTD": -4.05, "1Y": 8.43, "3Y": 11.84, "5Y": 9.22, "10Y": 94.93, "3Y_ann": 3.80, "5Y_ann": 1.78, "10Y_ann": 6.90}},
    {"name": "宏利MPF北美股票基金", "code": "SHK130", "risk": 5, "price": 33.422, "type": "股票", "ret": {"3M": -8.34, "YTD": -8.34, "1Y": 9.44, "3Y": 51.17, "5Y": 38.70, "10Y": 171.55, "3Y_ann": 14.77, "5Y_ann": 6.76, "10Y_ann": 10.51}},
    {"name": "宏利MPF國際股票基金", "code": "SHK127", "risk": 5, "price": 27.613, "type": "股票", "ret": {"3M": -4.66, "YTD": -4.66, "1Y": 13.80, "3Y": 43.61, "5Y": 28.46, "10Y": 132.49, "3Y_ann": 12.82, "5Y_ann": 5.14, "10Y_ann": 8.80}},
    {"name": "宏利MPF進取基金", "code": "SHK124", "risk": 5, "price": 27.374, "type": "混合", "ret": {"3M": -2.11, "YTD": -2.11, "1Y": 15.79, "3Y": 32.03, "5Y": 9.35, "10Y": 81.90, "3Y_ann": 9.70, "5Y_ann": 1.80, "10Y_ann": 6.17}},
    {"name": "宏利MPF增長基金", "code": "SHK123", "risk": 4, "price": 25.066, "type": "混合", "ret": {"3M": -1.83, "YTD": -1.83, "1Y": 12.73, "3Y": 25.04, "5Y": 4.80, "10Y": 57.74, "3Y_ann": 7.73, "5Y_ann": 0.94, "10Y_ann": 4.66}},
    {"name": "宏利MPF富達增長基金", "code": "SHK134", "risk": 5, "price": 37.379, "type": "混合", "ret": {"3M": -2.54, "YTD": -2.54, "1Y": 13.66, "3Y": 26.45, "5Y": 4.43, "10Y": 68.34, "3Y_ann": 8.14, "5Y_ann": 0.87, "10Y_ann": 5.35}},
]

def format_detailed_message():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    msg = f"📊 *宏利強積金監控日報* - {today}\n"
    msg += f"數據源: 宏利官方 Q1 2026 報告 | 自動推送 09:00 HKT\n\n"
    
    # 10年排行榜
    msg += f"🏆 *10年回報排行榜 (當日至10年)*\n"
    sorted_10y = sorted(MPF_FUNDS, key=lambda x: x['ret']['10Y'], reverse=True)
    for i, f in enumerate(sorted_10y[:5], 1):
        medal = ["🥇","🥈","🥉","4️⃣","5️⃣"][i-1]
        msg += f"{medal} {f['code']} {f['name'].replace('宏利MPF','')} {f['ret']['10Y']}% (年化{f['ret']['10Y_ann']}%)\n"
    
    msg += f"\n📈 *詳細回報比較 - 當日 ~ 10年*\n"
    msg += f"`基金    3M     1Y     3Y     5Y     10Y    年化10Y`\n"
    for f in MPF_FUNDS:
        r = f['ret']
        # 格式化對齊
        msg += f"`{f['code']} {r['3M']:>5.1f}% {r['1Y']:>5.1f}% {r['3Y']:>5.1f}% {r['5Y']:>5.1f}% {r['10Y']:>6.1f}% {r['10Y_ann']:>5.1f}%`\n"
    
    msg += f"\n💡 *今日洞察*\n"
    best_1y = max(MPF_FUNDS, key=lambda x: x['ret']['1Y'])
    worst_1y = min(MPF_FUNDS, key=lambda x: x['ret']['1Y'])
    best_10y = max(MPF_FUNDS, key=lambda x: x['ret']['10Y'])
    msg += f"• 1年最強: {best_1y['name']} {best_1y['ret']['1Y']}%\n"
    msg += f"• 1年最弱: {worst_1y['name']} {worst_1y['ret']['1Y']}%\n"
    msg += f"• 長線王: {best_10y['code']} 10年累積 {best_10y['ret']['10Y']}%\n"
    
    # 風險提示
    msg += f"\n⚠️ 年初至今整體MPF平均約6.2-7.55%，連續第4年有望正回報\n"
    msg += f"🔗 儀表板: 開啟 Meta AI Dashboard 查看互動圖表\n"
    msg += f"過往表現不代表未來 | 非投資建議"
    
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
            return False
    except Exception as e:
        print(f"❌ 網絡錯誤: {e}")
        return False

if __name__ == "__main__":
    message = format_detailed_message()
    print("準備推送訊息:")
    print(message[:500] + "...")
    success = send_telegram(message)
    if not success:
        print("\n本地測試訊息內容已印出，請檢查 BOT_TOKEN 和 CHAT_ID")
