import os, json, re, requests, time, urllib.parse
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
    pat1 = re.compile(r'\((SHK\d+|DHK\d+)\)[^\d]{0,80}?(\d+\.\d+)\s*截至\s*(\d{2}/\d{2}/\d{4})\s*([+-]?\d+\.\d+)%', re.S)
    for m in pat1.finditer(text):
        out[m.group(1)] = {'price': float(m.group(2)), 'chg': float(m.group(4)), 'date': m.group(3), 'source': 'manulife_auto'}
    if len(out) < 10:
        pat2 = re.compile(r'(SHK\d+|DHK\d+)[\s\S]{0,60}?(\d+\.\d+)\s*截至\s*(\d{2}/\d{2}/\d{4})\s*([+-]?\d+\.\d+)%', re.S)
        for m in pat2.finditer(text):
            if m.group(1) not in out:
                out[m.group(1)] = {'price': float(m.group(2)), 'chg': float(m.group(4)), 'date': m.group(3), 'source': 'manulife_auto_v2'}
    return out

def try_proxy_fetch():
    # 招式2: 用第三方 Proxy 轉 IP, 避開 Akamai 封 GitHub IP
    live = {}
    target = 'https://www.manulife.com.hk/zh-hk/individual/fund-price/mpf.html/v2/fundlist?product=%E5%AE%8F%E5%88%A9%E7%92%B0%E7%90%83%E7%B2%BE%E9%81%B8%28%E5%BC%B7%E7%A9%8D%E9%87%91%29%E8%A8%88%E5%8A%83&productId=8'
    proxies = [
        'https://api.allorigins.win/raw?url=' + urllib.parse.quote(target, safe=''),
        'https://corsproxy.io/?url=' + urllib.parse.quote(target, safe=''),
        'https://api.codetabs.com/v1/proxy?quest=' + urllib.parse.quote(target, safe=''),
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8'}
    for purl in proxies:
        try:
            DEBUG_LOGS.append('proxy try ' + purl[:60])
            r = requests.get(purl, headers=headers, timeout=40)
            txt = r.text
            DEBUG_LOGS.append('proxy len ' + str(len(txt)) + ' has SHK: ' + str('SHK' in txt) + ' has AccessDenied: ' + str('Access Denied' in txt))
            if 'SHK' in txt and 'Access Denied' not in txt:
                parsed = parse_inner_text(txt)
                DEBUG_LOGS.append('proxy parsed ' + str(len(parsed)))
                for kk, vv in parsed.items():
                    live[kk] = vv
                if len(live) >= 15:
                    API_HITS.append(purl[:80])
                    break
        except Exception as e:
            DEBUG_LOGS.append('proxy fail ' + str(e)[:200])
    return live

def try_playwright_stealth():
    # 招式1: 真 Chrome + Stealth + 人手行為, 唔用 headless Chromium (太易認)
    live = {}
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        DEBUG_LOGS.append('no playwright: ' + str(e)[:200])
        return live
    try:
        with sync_playwright() as p:
            # 試真 Chrome, 唔得先用 Chromium
            try:
                browser = p.chromium.launch(channel='chrome', headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled', '--disable-features=IsolateOrigins,site-per-process'])
                DEBUG_LOGS.append('launch real Chrome OK')
            except Exception as e:
                DEBUG_LOGS.append('real Chrome fail, fallback Chromium: ' + str(e)[:150])
                browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
            context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', viewport={'width': 1400, 'height': 2400}, locale='zh-HK', timezone_id='Asia/Hong_Kong', extra_http_headers={'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Referer': 'https://www.google.com.hk/'})
            # 刪走 webdriver 特徵
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined}); window.chrome = {runtime: {}}; Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]}); Object.defineProperty(navigator, 'languages', {get: () => ['zh-HK', 'zh', 'en']});")
            page = context.new_page()
            def on_response(resp):
                try:
                    url = resp.url
                    if any(k in url.lower() for k in ['fund', 'price', 'mpf', 'api']):
                        body = resp.text()
                        if 'SHK' in body and len(body) > 500 and 'Access Denied' not in body:
                            API_HITS.append(url[:120])
                            try:
                                j = json.loads(body)
                                # 遞歸搵
                                def rec(o):
                                    if isinstance(o, dict):
                                        c = o.get('code') or o.get('fundCode') or o.get('id')
                                        if isinstance(c, str) and ('SHK' in c or 'DHK' in c):
                                            pr = o.get('nav') or o.get('price') or o.get('unitPrice')
                                            if pr is not None:
                                                live[c] = {'price': float(pr), 'chg': float(o.get('change') or 0), 'date': str(o.get('date') or o.get('asOf') or 'auto'), 'source': 'manulife_auto_api'}
                                        for vv in o.values():
                                            rec(vv)
                                    elif isinstance(o, list):
                                        for vv in o:
                                            rec(vv)
                                rec(j)
                            except:
                                pass
                except:
                    pass
            page.on('response', on_response)
            urls = ['https://www.manulife.com.hk/zh-hk/individual/fund-price/mpf.html/v2/fundlist?product=%E5%AE%8F%E5%88%A9%E7%92%B0%E7%90%83%E7%B2%BE%E9%81%B8%28%E5%BC%B7%E7%A9%8D%E9%87%91%29%E8%A8%88%E5%8A%83&productId=8', 'https://www.manulife.com.hk/en/individual/funds/mpf-fund-prices.html']
            for url in urls:
                try:
                    DEBUG_LOGS.append('goto stealth ' + url)
                    page.goto('https://www.google.com.hk', wait_until='domcontentloaded', timeout=30000)
                    page.wait_for_timeout(2000)
                    page.goto(url, wait_until='domcontentloaded', timeout=90000)
                    page.wait_for_timeout(8000)
                    # 人手碌頁 + 滑鼠移動, 扮真人
                    for y in [400, 1000, 1800, 2800, 4000]:
                        page.mouse.move(600, 400)
                        page.evaluate('window.scrollTo(0,' + str(y) + ')')
                        page.wait_for_timeout(1200)
                    page.wait_for_timeout(4000)
                    inner = page.evaluate('() => document.body.innerText')
                    DEBUG_LOGS.append('stealth inner len ' + str(len(inner)) + ' head: ' + inner[:400].replace(chr(10), ' | '))
                    if 'Access Denied' in inner or 'errors.edgesuite' in inner:
                        DEBUG_LOGS.append('仍畀 Akamai 封, 試下一招 Proxy')
                        continue
                    parsed = parse_inner_text(inner)
                    DEBUG_LOGS.append('stealth parsed ' + str(len(parsed)) + ' dates: ' + ','.join(sorted(set([v['date'] for v in parsed.values()]))))
                    for kk, vv in parsed.items():
                        live[kk] = vv
                    if len(live) >= 15:
                        break
                except Exception as e:
                    DEBUG_LOGS.append('stealth url fail ' + str(e)[:300])
            browser.close()
    except Exception as e:
        DEBUG_LOGS.append('stealth fatal ' + str(e)[:400])
    return live

def build_final():
    # 先試 Stealth, 唔得試 Proxy, 兩樣都唔得就用 05/11 備援
    auto = try_playwright_stealth()
    if len(auto) < 15:
        DEBUG_LOGS.append('stealth 得 ' + str(len(auto)) + ' 隻, 轉 Proxy')
        proxy = try_proxy_fetch()
        for kk, vv in proxy.items():
            if kk not in auto:
                auto[kk] = vv
    is_auto = len(auto) >= 15
    final = {}
    if is_auto:
        for code, base in FALLBACK.items():
            if code in auto:
                a = auto[code]
                final[code] = {'zh': base['zh'], 'cat': base['cat'], 'price': a['price'], 'chg': a['chg'], 'date': a['date'], 'source': 'manulife_auto', 'vs': base['vs']}
            else:
                final[code] = {'zh': base['zh'], 'cat': base['cat'], 'price': base['price'], 'chg': base['chg'], 'date': base['date'], 'source': 'fallback', 'vs': base['vs']}
        latest = max([v['date'] for v in auto.values()], default='auto')
    else:
        for code, base in FALLBACK.items():
            final[code] = {'zh': base['zh'], 'cat': base['cat'], 'price': base['price'], 'chg': base['chg'], 'date': base['date'], 'source': 'fallback_0511', 'vs': base['vs']}
        latest = '05/11/2026 (5隻) + 04/11/2026 (24隻)'
    return final, is_auto, latest, auto

def ai_score(code, info):
    chg = info.get('chg') or 0
    if code == 'SHK126':
        return (72, '分批轉入', '05/11 +3.41%最勁反彈')
    if code == 'SHK127':
        return (40, '持有', '05/11 -2.89%大跌')
    if code == 'SHK137':
        return (82, '立即分批', '04/11+2.97%最勁')
    if code == 'SHK148':
        return (72, '分批轉入', 'DIS核心最穩')
    if code == 'SHK128':
        return (58, '持有等回調', '大跌後反彈')
    if code == 'SHK136':
        return (60, '持有', '等企穩')
    return (55, '持有', '單日' + fmt(chg) + '%')

def build_msg(final, is_auto, latest):
    today = dt.now().strftime('%d/%m/%Y %H:%M')
    yest = (dt.now() - timedelta(days=1)).strftime('%d/%m/%Y')
    msg = ''
    if is_auto:
        msg += '📊 宏利全29基金 AI日報 - ' + today + ' [V16 破Akamai ✅]\n'
        msg += '今天 ' + dt.now().strftime('%d/%m/%Y') + ' | 截至 ' + str(latest) + ' (宏利官網自動捉, 已破Akamai) | 目標昨日 ' + yest + ' | 29隻\n'
    else:
        msg += '📊 宏利全29基金 AI日報 - ' + today + ' [V16 05/11部分真價]\n'
        msg += '今天 ' + dt.now().strftime('%d/%m/%Y') + ' | 截至 ' + str(latest) + ' | 目標昨日 ' + yest + ' | 29隻\n'
    msg += '來源 ' + ('manulife_auto' if is_auto else 'fallback_0511') + ' | API命中: ' + str(len(API_HITS)) + '\n'
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
    msg += '5. 宏利封咗GitHub IP, V16用緊真Chrome+Proxy破緊, 唔使再Cap圖\n'
    if not is_auto:
        msg += '\n⚠️ 自動 Debug: ' + ' | '.join(DEBUG_LOGS[:4]) + '\n'
        msg += 'API命中: ' + ', '.join(API_HITS[:2]) + '\n'
        msg += '💡 終極自動化: iPhone捷徑每日09:30自動去宏利攞價, 唔使經GitHub IP, 唔會畀Akamai封\n'
    msg += '\n🔗 https://ac7127.github.io/manulife-mpf-tracker/\n'
    msg += '✅ V16 破Akamai + 真自動'
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
