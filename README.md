# stock_tracker

## 選題動機與可能之潛力

在現代投資市場中，投資者面臨著資訊爆炸的挑戰，每天都有大量的市場資訊需要處理。
技術分析作為一種重要的投資工具，需要投資者持續觀察價格走勢和技術指標的變化。然而，人工監控既耗時又容易受到情緒影響，往往會使投資者錯過關鍵的交易時機。相反地，自動化的股價資料爬取與監控，能最有效率地提供最客觀的資訊。
因此，若能建立一套自動化的股價資料爬取與監控系統，便能有效減少投資者處理資訊的負擔，提升決策效率，並降低因情緒影響而錯失交易機會的風險。

若我們能完善相關功能，自動化的股價資料爬取與監控系統，存在支援以下情境之可能：
1. 解析股價資料，在出現重要技術訊號時，通過聊天軟體推送通知，讓使用者及時掌握市場機會。
2. 收集和儲存歷史交易數據。相關資料可用於分析交易策略之成效，供使用者持續優化投資決策。
3. 讓投資者能分享、訂閱的投資策略。存在發展成為投資策略分享平台之潛力。

目前，本系統已實現以下功能：
1. 自動化資料收集與分析
- 使用 Yahoo Finance API 自動獲取股票資料
- 每天下午 4 點自動執行資料更新(抓取美股收盤資料)
2. 技術指標計算與訊號偵測
- 計算 5 日與 20 日移動平均線
- 自動偵測黃金交叉與死亡交叉
3. 訊號通知機制
- 當出現買賣訊號時，系統會記錄相關資訊
- 預留通知軟體 API 串接介面
4. 資料儲存與管理
- 使用 SQLite 資料庫儲存股票資料
- 支援多支股票同時追蹤

系統採用 Docker 容器化部署，確保環境一致性，便於未來擴充功能。下一步計畫加入更多技術指標、整合通知軟體 API，並開發使用者介面，讓投資者能更方便地管理其投資組合與策略。

## 本地運行方式
1. 安裝所需套件
``` bash
pip install -r requirement.txt
```
2. 複製環境變數檔案(並依需求修改)
``` bash
cp .env.example .env
```
3. 初始化資料庫
``` bash
python manage.py migrate 
```
4. 初始化股票資料(可至`init_stocks.py`中調整股票清單)
``` bash
python manage.py init_stocks
```
5. 啟動服務
``` bash
python manage.py runserver
```
其中，當前scheduler設定為一天爬取一次資料，可以藉由修改 `tracker/scheduler.py` 中的 `scheduler.addjob()`函數調整相關設定以進行功能測試。

## Docker 運行方式
1. 建立Docker Image
```bash
docker build -t stock-tracker .
```
2. 運行 Docker Image
- docker run
```bash
docker run -d -p 8000:8000 -v $(pwd)/data:/app/data:rw --env-file .env --name stock-tracker stock-tracker
```
- docker-compose
```bash
docker compose up -d #啟動服務
docker compose logs -f #查看日誌
docker compose down #停止服務
```
