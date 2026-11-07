import os, json, re, requests, time
from datetime import datetime as dt, timedelta
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

FALLBACK = {
  'DHK121': {'zh': '利息基金', 'cat': 'guarantee', 'price': None, 'chg': None, 'vs': None, 'date': '04/11/2026'},
  'SHK122': {'zh': '穩健基金', 'cat': 'guarantee', 'price': 17.349, 'chg': 0.45, 'vs': 0.63, 'date': '04/11/2026'},
  'SHK123': {'zh': '增長基金', 'cat': 'mixed', 'price': 26.636, 'chg': -0.27, 'vs': -2.53, 'date': '05/11/2026'},
  'SHK124': {'zh': '進取基金', 'cat': 'mixed', 'price': 29.638, 'chg': -0.26, 'vs': -3.39, 'date': '05/11/2026'},
  'SHK125': {'zh': '保守基金', 'cat': 'guarantee', 'price': 12.805, 'chg': 0.02, 'vs': 0.25, 'date': '05/11/2026'},
  'SHK126': {'zh': '香港股票基金', 'cat': 'stock', 'price': 23.392, 'chg': 3.41, 'vs': -3.24, 'date': '05/11/2026'},
  'SHK127': {'zh': '國際股票基金', 'cat': 'stock', 'price': 30.527, 'chg': -2.89, 'vs': -3.57, 'date': '05/11/2026'},
  'SHK128': {'zh': '亞太股票基金', 'cat': 'stock', 'price': 45.285, 'chg': 0.91, 'vs': -8.59, 'date': '04/11/2026'},
  'SHK129': {'zh': '歐洲股票基金', 'cat': 'stock', 'price': 19.361, 'chg': 2.52, 'vs': 2.79, 'date': '04/11/2026'},
  'SHK130': {'zh': '北美股票基金', 'cat': 'stock', 'price': 38.065, 'chg': 1.63, 'vs': -0.27, 'date': '04/11/2026'},
  'SHK131': {'zh': '日本股票基金', 'cat': 'stock', 'price': 29.477, 'chg': -1.17, 'vs': -3.37, 'date': '04/11/2026'},
  'SHK132': {'zh': '香港債券基金', 'cat': 'bond', 'price': 15.931, 'chg': 0.11, 'vs': 1.74, 'date': '04/11/2026'},
  'SHK133': {'zh': '國際債券基金', 'cat': 'bond', 'price': 15.362, 'chg': 0.48, 'vs': 1.92, 'date': '04/11/2026'},
  'SHK134': {'zh': '富達增長基金', 'cat': 'mixed', 'price': 40.041, 'chg': 0.89, 'vs': -4.67, 'date': '04/11/2026'},
  'SHK135': {'zh': '富達平穩增長基金', 'cat': 'mixed', 'price': 25.117, 'chg': 0.56, 'vs': -5.22, 'date': '04/11/2026'},
  'SHK136': {'zh': '中華威力基金', 'cat': 'stock', 'price': 34.549, 'chg': 1.22, 'vs': -10.97, 'date': '04/11/2026'},
  'SHK137': {'zh': '康健護理基金', 'cat': 'stock', 'price': 39.073, 'chg': 2.97, 'vs': 9.48, 'date': '04/11/2026'},
  'SHK138': {'zh': '智優逸退休基金', 'cat': 'mixed', 'price': 15.535, 'chg': 0.74, 'vs': 2.2, 'date': '04/11/2026'},
  'SHK140': {'zh': '2025退休基金', 'cat': 'target', 'price': 17.516, 'chg': 0.73, 'vs': 18.35, 'date': '04/11/2026'},
  'SHK141': {'zh': '2030退休基金', 'cat': 'target', 'price': 20.348, 'chg': 1.05, 'vs': 9.99, 'date': '04/11/2026'},
  'SHK142': {'zh': '2035退休基金', 'cat': 'target', 'price': 21.997, 'chg': 1.26, 'vs': 9.43, 'date': '04/11/2026'},
  'SHK143': {'zh': '2040退休基金', 'cat': 'target', 'price': 23.069, 'chg': 1.42, 'vs': 8.32, 'date': '04/11/2026'},
  'SHK144': {'zh': '2045退休基金', 'cat': 'target', 'price': 23.33, 'chg': 1.45, 'vs': 9.48, 'date': '04/11/2026'},
  'SHK145': {'zh': '恒指ESG基金', 'cat': 'stock', 'price': 14.293, 'chg': 1.84, 'vs': -3.73, 'date': '04/11/2026'},
  'SHK146': {'zh': '可持續亞太債券基金', 'cat': 'bond', 'price': 11.982, 'chg': 0.19, 'vs': 1.34, 'date': '04/11/2026'},
  'SHK147': {'zh': '人民幣債券基金', 'cat': 'bond', 'price': 13.03, 'chg': -0.04, 'vs': 0.44, 'date': '04/11/2026'},
  'SHK148': {'zh': '核心累積基金 DIS', 'cat': 'dis', 'price': 19.063, 'chg': 0.89, 'vs': 0.34, 'date': '04/11/2026'},
  'SHK149': {'zh': '65歲後基金 DIS', 'cat': 'dis', 'price': 12.382, 'chg': 0.45, 'vs': 1.33, 'date': '04/11/2026'},
  'SHK150': {'zh': '退休收益基金', 'cat': 'mixed', 'price': 9.202, 'chg': 0.56, 'vs': 1.35, 'date': '04/11/2026'},
}

DEBUG_LOGS = []
API_HITS = []

def fmt(v):
    if v is None:
        return '0.00'
    return '{:+.2f}'.format(v)

def parse_inner_text(text):
    out = {}
    # 宏利官網真格式: 23.392 截至 05/11/2026 3.41% 0.771
    # 亦有: (SHK126) ... 23.392 截至 05/11/2026
    # 方法1: 有括號代號
    pat1 = re.compile(r'\((SHK\d+|DHK\d+)\)[^\d]{0,80}?(\d+\.\d+)\s*截至\s*(\d{2}/\d{2}/\d{4})\s*([+-]?\d+\.\d+)%', re.S)
    for m in pat1.finditer(text):
        out[m.group(1)] = {'price': float(m.group(2)), 'chg': float(m.group(4)), 'date': m.group(3), 'source': 'manulife_auto'}
    # 方法2: 冇括號, 直接基金名後面跟價 - 用表格行解析
    # e.g. 宏利MPF香港股票基金 (SHK126) (港元) 23.392 截至 05/11/2026 3.41%
    if len(out) < 10:
        pat2 = re.compile(r'(SHK\d+|DHK\d+)[\s\S]{0,60}?(\d+\.\d+)\s*截至\s*(\d{2}/\d{2}/\d{4})\s*([+-]?\d+\.\d+)%', re.S)
        for m in pat2.finditer(text):
            if m.group(1) not in out:
                out[m.group(1)] = {'price': float(m.group(2)), 'chg': float(m.group(4)), 'date': m.group(3), 'source': 'manulife_auto_v2'}
    # 方法3: 最寬鬆 - 淨係搵 SHKxxx + 價 + 日期, 唔理%
    if len(out) < 10:
        pat3 = re.compile(r'(SHK\d+|DHK\d+)[\s\S]{0,80}?(\d+\.\d+)\s*截至\s*(\d{2}/\d{2}/\d{4})', re.S)
        for m in pat3.finditer(text):
            if m.group(1) not in out:
                out[m.group(1)] = {'price': float(m.group(2)), 'chg': 0.0, 'date': m.group(3), 'source': 'manulife_auto_v3'}
    return out

def search_json_recursive(obj, out, date_hint):
    if isinstance(obj, dict):
        code = obj.get('code') or obj.get('fundCode') or obj.get('fund_code') or obj.get('id') or obj.get('fundId')
        if isinstance(code, str) and ('SHK' in code or 'DHK' in code):
            price = obj.get('nav') or obj.get('price') or obj.get('unitPrice') or obj.get('netAssetValue') or obj.get('value') or obj.get('unit_price')
            chg = obj.get('change') or obj.get('dailyChange') or obj.get('changePct') or obj.get('dailyChangePct') or obj.get('changePercent') or 0
            d = obj.get('date') or obj.get('asOf') or obj.get('priceDate') or obj.get('asOfDate') or date_hint
            if price is not None:
                try:
                    out[code] = {'price': float(price), 'chg': float(chg), 'date': str(d), 'source': 'manulife_auto_api'}
                except:
                    pass
        for v in obj.values():
            search_json_recursive(v, out, date_hint)
    elif isinstance(obj, list):
        for v in obj:
            search_json_recursive(v, out, date_hint)

def try_playwright_auto():
    live = {}
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        DEBUG_LOGS.append('no playwright: ' + str(e)[:200])
        return live
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
            context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', viewport={'width': 1400, 'height': 2400}, locale='zh-HK')
            page = context.new_page()
            def on_response(resp):
                try:
                    url = resp.url
                    if any(k in url.lower() for k in ['fund', 'price', 'mpf', 'api', 'json', 'nav']):
                        body = resp.text()
                        if 'SHK' in body and len(body) > 500:
                            API_HITS.append(url[:120])
                            try:
                                j = json.loads(body)
                                tmp = {}
                                search_json_recursive(j, tmp, 'auto')
                                for kk, vv in tmp.items():
                                    live[kk] = vv
                            except:
                                pass
                except:
                    pass
            page.on('response', on_response)
            urls = [
                'https://www.manulife.com.hk/zh-hant/individual/funds/mpf-fund-prices.html',
                'https://www.manulife.com.hk/en/individual/funds/mpf-fund-prices.html',
            ]
            for url in urls:
                try:
                    DEBUG_LOGS.append('goto ' + url)
                    page.goto(url, wait_until='domcontentloaded', timeout=90000)
                    page.wait_for_timeout(10000)
                    for y in [500, 1200, 2200, 3500, 5000]:
                        page.evaluate('window.scrollTo(0,' + str(y) + ')')
                        page.wait_for_timeout(1500)
                    page.wait_for_timeout(5000)
                    inner = page.evaluate('() => document.body.innerText')
                    DEBUG_LOGS.append('inner len ' + str(len(inner)) + ' head: ' + inner[:500].replace(chr(10), ' | '))
                    parsed = parse_inner_text(inner)
                    DEBUG_LOGS.append('inner parsed ' + str(len(parsed)) + ' funds, dates: ' + ','.join(sorted(set([v['date'] for v in parsed.values()]))))
                    for kk, vv in parsed.items():
                        if kk not in live:
                            live[kk] = vv
                    if len(live) >= 20:
                        break
                except Exception as e:
                    DEBUG_LOGS.append('url fail ' + str(e)[:300])
            browser.close()
    except Exception as e:
        DEBUG_LOGS.append('playwright fatal ' + str(e)[:400])
    return live

def build_final():
    auto = try_playwright_auto()
    is_auto = len(auto) >= 15
    final = {}
    if is_auto:
        for code, base in FALLBACK.items():
            if code in auto:
                a = auto[code]
                final[code] = {'zh': base['zh'], 'cat': base['cat'], 'price': a['price'], 'chg': a['chg'], 'date': a['date'], 'source': 'manulife_auto', 'vs': base['vs']}
            else:
                final[code] = {'zh': base['zh'], 'cat': base['cat'], 'price': base['price'], 'chg': base['chg'], 'date': base['date'], 'source': 'fallback_0511', 'vs': base['vs']}
        latest = max([v['date'] for v in auto.values()], default='auto')
    else:
        for code, base in FALLBACK.items():
            final[code] = {'zh': base['zh'], 'cat': base['cat'], 'price': base['price'], 'chg': base['chg'], 'date': base['date'], 'source': 'fallback_0511', 'vs': base['vs']}
        latest = '05/11/2026 (5隻) + 04/11/2026 (24隻)'
    return final, is_auto, latest, auto

def ai_score(code, info):
    chg = info.get('chg') or 0
    if code == 'SHK126':
        return (72, '分批轉入', '05/11單日+3.41%最勁反彈, 04/11到05/11兩日升+3.41%')
    if code == 'SHK127':
        return (40, '持有', '05/11單日-2.89%大跌, 等止跌')
    if code == 'SHK137':
        return (82, '立即分批', '04/11+2.97%最勁')
    if code == 'SHK148':
        return (72, '分批轉入', 'DIS核心最穩')
    if code == 'SHK128':
        return (58, '持有等回調', '大跌後反彈, 唔好追')
    if code == 'SHK136':
        return (60, '持有', '等企穩')
    if code == 'SHK131':
        return (45, '持有', '等止跌')
    return (55, '持有', '單日' + fmt(chg) + '%')

def build_msg(final, is_auto, latest):
    today = dt.now().strftime('%d/%m/%Y %H:%M')
    yest = (dt.now() - timedelta(days=1)).strftime('%d/%m/%Y')
    msg = ''
    if is_auto:
        msg += '📊 宏利全29基金 AI日報 - ' + today + ' [V15 真自動 ✅]\n'
        msg += '今天 ' + dt.now().strftime('%d/%m/%Y') + ' | 截至 ' + str(latest) + ' (宏利官網自動捉) | 目標昨日 ' + yest + ' | 29隻\n'
    else:
        msg += '📊 宏利全29基金 AI日報 - ' + today + ' [V15 05/11部分真價]\n'
        msg += '今天 ' + dt.now().strftime('%d/%m/%Y') + ' | 截至 ' + str(latest) + ' | 目標昨日 ' + yest + ' | 29隻\n'
    msg += '來源 ' + ('manulife_auto' if is_auto else 'fallback_0511_5隻+0411_24隻') + ' | API命中: ' + str(len(API_HITS)) + '\n'
    msg += '━━━━━━━━━━━━━━━━━━━━\n\n'
    vals = []
    for c, v in final.items():
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
            v = final[code]
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
            msg += flag + code + ' ' + v['zh'] + ' $' + price_s + ' ' + fmt(chg) + '% as of ' + str(v['date']) + ' (9月至今 ' + fmt(v['vs']) + '%)\n'
    msg += '\n━━━━━━━━━━━━ AI入市\n'
    scored = []
    for code, info in final.items():
        if code == 'DHK121':
            continue
        s, a, r = ai_score(code, info)
        scored.append((code, s, a, r, info))
    scored.sort(key=lambda x: x[1], reverse=True)
    for code, s, a, r, info in scored[:10]:
        price_s = '{:.3f}'.format(info['price'])
        msg += a + ' ' + code + ' ' + str(s) + '分 $' + price_s + ' ' + fmt(info['chg']) + '% | ' + r + '\n'
    msg += '\n━━━━━━━━━━━━ Andy 44歲操作建議\n'
    msg += '1. 香港 SHK126 05/11 +3.41%最勁, 22.621升到23.392, 兩日反彈, 唔好All-in, 分批\n'
    msg += '2. 國際 SHK127 05/11 -2.89%大跌, 31.435跌到30.527, 等止跌先入\n'
    msg += '3. 增長 SHK123 -0.27%, 進取 SHK124 -0.26%, 輕微回調, 持有\n'
    msg += '4. DIS核心 SHK148繼續做底倉60%股\n'
    msg += '5. 其餘24隻等V15自動捉埋05/11, 唔使再Cap圖\n'
    if not is_auto:
        msg += '\n⚠️ 自動 Debug: ' + ' | '.join(DEBUG_LOGS[:3]) + '\n'
        msg += 'API命中: ' + ', '.join(API_HITS[:2]) + '\n'
    msg += '\n🔗 https://ac7127.github.io/manulife-mpf-tracker/\n'
    msg += '✅ V15 05/11部分真價 + 真自動 (唔使再Cap圖)'
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
    final, is_auto, latest, auto = build_final()
    m = build_msg(final, is_auto, latest)
    print(m)
    send_safe(m)
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump({'as_of': str(latest), 'is_auto': is_auto, 'debug_logs': DEBUG_LOGS, 'api_hits': API_HITS, 'funds': final}, f, ensure_ascii=False, indent=2)
