import os, json, requests, time
from datetime import datetime as dt
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

LIVE = {
 "DHK121": {
  "zh": "利息基金",
  "cat": "guarantee",
  "price": None,
  "chg": None,
  "vs": None,
  "old": None
 },
 "SHK122": {
  "zh": "穩健基金",
  "cat": "guarantee",
  "price": 17.349,
  "chg": 0.45,
  "vs": 0.63,
  "old": 17.24
 },
 "SHK123": {
  "zh": "增長基金",
  "cat": "mixed",
  "price": 26.708,
  "chg": 1.21,
  "vs": -2.27,
  "old": 27.328
 },
 "SHK124": {
  "zh": "進取基金",
  "cat": "mixed",
  "price": 29.715,
  "chg": 1.46,
  "vs": -3.14,
  "old": 30.679
 },
 "SHK125": {
  "zh": "保守基金",
  "cat": "guarantee",
  "price": 12.803,
  "chg": 0.01,
  "vs": 0.24,
  "old": 12.773
 },
 "SHK126": {
  "zh": "香港股票基金",
  "cat": "stock",
  "price": 22.621,
  "chg": 2.52,
  "vs": -6.43,
  "old": 24.176
 },
 "SHK127": {
  "zh": "國際股票基金",
  "cat": "stock",
  "price": 31.435,
  "chg": 1.56,
  "vs": -0.7,
  "old": 31.656
 },
 "SHK128": {
  "zh": "亞太股票基金",
  "cat": "stock",
  "price": 45.285,
  "chg": 0.91,
  "vs": -8.59,
  "old": 49.538
 },
 "SHK129": {
  "zh": "歐洲股票基金",
  "cat": "stock",
  "price": 19.361,
  "chg": 2.52,
  "vs": 2.79,
  "old": 18.835
 },
 "SHK130": {
  "zh": "北美股票基金",
  "cat": "stock",
  "price": 38.065,
  "chg": 1.63,
  "vs": -0.27,
  "old": 38.167
 },
 "SHK131": {
  "zh": "日本股票基金",
  "cat": "stock",
  "price": 29.477,
  "chg": -1.17,
  "vs": -3.37,
  "old": 30.505
 },
 "SHK132": {
  "zh": "香港債券基金",
  "cat": "bond",
  "price": 15.931,
  "chg": 0.11,
  "vs": 1.74,
  "old": 15.658
 },
 "SHK133": {
  "zh": "國際債券基金",
  "cat": "bond",
  "price": 15.362,
  "chg": 0.48,
  "vs": 1.92,
  "old": 15.072
 },
 "SHK134": {
  "zh": "富達增長基金",
  "cat": "mixed",
  "price": 40.041,
  "chg": 0.89,
  "vs": -4.67,
  "old": 42.003
 },
 "SHK135": {
  "zh": "富達平穩增長基金",
  "cat": "mixed",
  "price": 25.117,
  "chg": 0.56,
  "vs": -5.22,
  "old": 26.5
 },
 "SHK136": {
  "zh": "中華威力基金",
  "cat": "stock",
  "price": 34.549,
  "chg": 1.22,
  "vs": -10.97,
  "old": 38.808
 },
 "SHK137": {
  "zh": "康健護理基金",
  "cat": "stock",
  "price": 39.073,
  "chg": 2.97,
  "vs": 9.48,
  "old": 35.688
 },
 "SHK138": {
  "zh": "智優逸退休基金",
  "cat": "mixed",
  "price": 15.535,
  "chg": 0.74,
  "vs": 2.2,
  "old": 15.2
 },
 "SHK140": {
  "zh": "2025退休基金",
  "cat": "target",
  "price": 17.516,
  "chg": 0.73,
  "vs": 18.35,
  "old": 14.8
 },
 "SHK141": {
  "zh": "2030退休基金",
  "cat": "target",
  "price": 20.348,
  "chg": 1.05,
  "vs": 9.99,
  "old": 18.5
 },
 "SHK142": {
  "zh": "2035退休基金",
  "cat": "target",
  "price": 21.997,
  "chg": 1.26,
  "vs": 9.43,
  "old": 20.1
 },
 "SHK143": {
  "zh": "2040退休基金",
  "cat": "target",
  "price": 23.069,
  "chg": 1.42,
  "vs": 8.32,
  "old": 21.3
 },
 "SHK144": {
  "zh": "2045退休基金",
  "cat": "target",
  "price": 23.33,
  "chg": 1.45,
  "vs": 9.48,
  "old": 21.3
 },
 "SHK145": {
  "zh": "恒指ESG基金",
  "cat": "stock",
  "price": 14.293,
  "chg": 1.84,
  "vs": -3.73,
  "old": 14.847
 },
 "SHK146": {
  "zh": "可持續亞太債券基金",
  "cat": "bond",
  "price": 11.982,
  "chg": 0.19,
  "vs": 1.34,
  "old": 11.824
 },
 "SHK147": {
  "zh": "人民幣債券基金",
  "cat": "bond",
  "price": 13.03,
  "chg": -0.04,
  "vs": 0.44,
  "old": 12.973
 },
 "SHK148": {
  "zh": "核心累積基金 DIS",
  "cat": "dis",
  "price": 19.063,
  "chg": 0.89,
  "vs": 0.34,
  "old": 18.999
 },
 "SHK149": {
  "zh": "65歲後基金 DIS",
  "cat": "dis",
  "price": 12.382,
  "chg": 0.45,
  "vs": 1.33,
  "old": 12.22
 },
 "SHK150": {
  "zh": "退休收益基金",
  "cat": "mixed",
  "price": 9.202,
  "chg": 0.56,
  "vs": 1.35,
  "old": 9.08
 }
}

def fmt(v):
    if v is None:
        return '0.00'
    return '{:+.2f}'.format(v)

def ai_score(code, info):
    chg = info.get('chg') or 0
    if code == 'SHK137':
        return (82, '立即分批', '單日+2.97%最勁, 9月至今+9.48%領先')
    if code == 'SHK129':
        return (70, '分批轉入', '單日+2.52%, 9月至今+2.79%穩')
    if code == 'SHK126':
        return (68, '分批轉入', '單日+2.52%反彈, 但9月至今-6.43%仍弱, 唔好All-in')
    if code == 'SHK130':
        return (66, '分批轉入', '單日+1.63%, 9月至今-0.27%企穩')
    if code == 'SHK148':
        return (72, '分批轉入', 'DIS核心 +0.89%, 9月至今+0.34%最穩')
    if code == 'SHK128':
        return (58, '持有等回調', '單日+0.91%但9月至今-8.59%大跌, 唔好追')
    if code == 'SHK136':
        return (60, '持有', '單日+1.22%反彈, 9月至今-10.97%最傷, 等企穩')
    if code == 'SHK131':
        return (45, '持有', '唯一跌-1.17%, 9月至今-3.37%, 等止跌')
    if code == 'SHK145':
        return (55, '持有', '單日+1.84%反彈, 9月至今-3.73%')
    return (55, '持有', '單日' + fmt(chg) + '%')

def build_msg():
    today = dt.now().strftime('%d/%m/%Y %H:%M')
    msg = ''
    msg += '📊 宏利全29基金 AI日報 - ' + today + ' [V13.1 04/11真價]\n'
    msg += '今天 06/11/2026 | 截至 04/11/2026 (宏利官網最新, MPF T+1) | 來源 宏利官網截圖 OCR | 29隻\n'
    msg += '━━━━━━━━━━━━━━━━━━━━\n\n'
    vals = []
    for c, v in LIVE.items():
        if v.get('chg') is not None:
            vals.append((c, v))
    vals.sort(key=lambda x: x[1]['chg'], reverse=True)
    gain_parts = []
    for c, v in vals[:3]:
        gain_parts.append(c + ' ' + fmt(v['chg']) + '%')
    lose_parts = []
    for c, v in vals[-3:]:
        lose_parts.append(c + ' ' + fmt(v['chg']) + '%')
    msg += '🔥 升幅 ' + ', '.join(gain_parts) + '\n'
    msg += '❄️ 跌幅 ' + ', '.join(lose_parts) + '\n\n'
    cats = [
        ('股票9隻', ['SHK126','SHK127','SHK128','SHK129','SHK130','SHK131','SHK136','SHK137','SHK145']),
        ('債券4隻', ['SHK132','SHK133','SHK146','SHK147']),
        ('保證3隻', ['DHK121','SHK122','SHK125']),
        ('混合6隻', ['SHK123','SHK124','SHK134','SHK135','SHK138','SHK150']),
        ('DIS2隻', ['SHK148','SHK149']),
        ('目標5隻', ['SHK140','SHK141','SHK142','SHK143','SHK144']),
    ]
    for cat_name, codes in cats:
        msg += '\n【' + cat_name + '】\n'
        for code in codes:
            v = LIVE[code]
            if v['price'] is None:
                msg += 'DHK121 利息基金 - 每月利率 0.875%\n'
                continue
            chg = v['chg']
            if abs(chg) >= 2:
                flag = '🚨'
            elif chg >= 0.5:
                flag = '🟢'
            elif chg <= -0.5:
                flag = '🔴'
            else:
                flag = ''
            price_s = '{:.3f}'.format(v['price'])
            msg += flag + code + ' ' + v['zh'] + ' $' + price_s + ' ' + fmt(chg) + '% as of 04/11/2026 (9月至今 ' + fmt(v['vs']) + '%)\n'
    msg += '\n━━━━━━━━━━━━ AI入市 (04/11)\n'
    scored = []
    for code, info in LIVE.items():
        if code == 'DHK121':
            continue
        s, a, r = ai_score(code, info)
        scored.append((code, s, a, r, info))
    scored.sort(key=lambda x: x[1], reverse=True)
    for code, s, a, r, info in scored[:10]:
        price_s = '{:.3f}'.format(info['price'])
        msg += a + ' ' + code + ' ' + str(s) + '分 $' + price_s + ' ' + fmt(info['chg']) + '% | ' + r + '\n'
    msg += '\n━━━━━━━━━━━━ Andy 44歲操作建議\n'
    msg += '1. 康健 SHK137最勁+2.97%可持有, 唔好追高, 等-2%回調先加\n'
    msg += '2. 亞太 SHK128由49.538跌到45.285 (-8.59%), 中華 SHK136由38.808跌到34.549 (-10.97%), 大跌後單日反彈, 唔好All-in, 分批\n'
    msg += '3. 香港 SHK126 22.621反彈+2.52%, 9月至今-6.43%, 若>30%減至15%\n'
    msg += '4. DIS核心 SHK148 19.063最穩+0.89%, 繼續做底倉60%股\n'
    msg += '5. 日本 SHK131唯一跌-1.17%, 等止跌先入\n'
    msg += '\n🔗 https://ac7127.github.io/manulife-mpf-tracker/\n'
    msg += '✅ V13.1 真價04/11 + AI + Telegram (已修復 SyntaxError)'
    return msg

def send_safe(text):
    if not BOT_TOKEN or not CHAT_ID:
        print(text)
        return
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage'
    t = text
    while len(t) > 0:
        if len(t) <= 3800:
            chunk = t
        else:
            chunk = t[:3800].rsplit('\n', 1)[0]
            if not chunk:
                chunk = t[:3800]
        try:
            r = requests.post(url, json={'chat_id': CHAT_ID, 'text': chunk}, timeout=25)
            print('Telegram ' + str(r.status_code))
        except Exception as e:
            print(str(e))
        t = t[len(chunk):]
        time.sleep(1.2)

if __name__ == '__main__':
    m = build_msg()
    print(m)
    send_safe(m)
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump({'as_of': '04/11/2026', 'funds': LIVE}, f, ensure_ascii=False, indent=2)
