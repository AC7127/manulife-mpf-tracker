# 宏利強積金監控代理 - GitHub 自動化版

> 每日 09:00 HKT 自動推送當日至10年詳細回報比較到 Telegram
> Bot: @mpf_daily_andy_choi_bot | Chat ID: 8711230455

## 📦 包含檔案
- `mpf_bot.py` - 主程式，包含15隻宏利基金完整數據 (當日至10年回報)
- `.github/workflows/daily.yml` - GitHub Actions 自動化設定
- `README.md` - 本說明

## 🚀 3分鐘部署步驟

### 1. 建立 GitHub Repo
1. 去 https://github.com/new 建立新 repo，名稱例如 `manulife-mpf-tracker`
2. 將 `mpf_bot.py` 上傳到根目錄
3. 建立資料夾 `.github/workflows/`，將 `daily.yml` 放進去
   - 結構應該係：
   ```
   mpf_bot.py
   .github/
     workflows/
       daily.yml
   ```

### 2. 設定 Secrets (重要！)
1. 去你個 Repo -> Settings -> Secrets and variables -> Actions
2. 按 `New repository secret` 建立兩個：
   - Name: `BOT_TOKEN` 
     Value: `8645545130:AAGVfZCuytaFiFz6F4dC9g6tLImLthHVR-Y` 
     (⚠️ 建議去 @BotFather 按 /mybots -> Revoke 換個新 Token 再用，舊Token已曝光)
   - Name: `CHAT_ID`
     Value: `8711230455`

### 3. 啟動自動推送
1. 去 Repo -> Actions -> 你會見到 "宏利強積金每日監控推送"
2. 按 `Run workflow` -> `Run workflow` 手動測試一次
3. 去你 Telegram @mpf_daily_andy_choi_bot 應該即刻收到訊息
4. 之後每日 09:00 HKT 自動推送，無需再手動

## 📊 推送內容
- 10年回報排行榜
- 詳細回報比較表 (3M/YTD/1Y/3Y/5Y/10Y/年化10Y)
- 今日洞察 (最強/最弱基金)
- 風險提示

數據來源：Manulife Global Select (MPF) Scheme Quarterly Fund Fact Sheet 截至 2026-03-31

## 🔒 安全
- Token 請用 GitHub Secrets，唔好直接寫喺 code
- 呢個 repo 建議設為 Private
- 每次推送後舊 Token 要 Revoke

## 🛠️ 本地測試
```bash
export BOT_TOKEN="你的Token"
export CHAT_ID="8711230455"
pip install requests
python mpf_bot.py
```

## 📈 基金數據
包含15隻核心基金：
- 股票基金: 康健護理 SHK137, 亞太 SHK128, 中華威力 SHK136, 香港 SHK126, 恒指ESG SHK145, 日本 SHK131, 歐洲 SHK129, 北美 SHK130, 國際 SHK127
- 混合基金: 進取 SHK124, 增長 SHK123, 富達增長 SHK134

過往表現不代表未來表現 | 非投資建議
