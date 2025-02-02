# stock_tracker
## 本地運行方式
1. Clone專案
2. 運行以下指令
``` bash
pip install -r requirement.txt #安裝所需套件
cp .env.example .env #複製環境變數檔案並依需求修改
python manage.py migrate #初始化資料庫
python manage.py init_stocks #初始化股票資料
python manage.py runserver #啟動服務
```
3. 由於scheduler目前被設定成一天只會運行一次，可以修改 `tracker/scheduler` 中 `scheduler.addjob()`函數設定進行測試以確保程式可正常運行。

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
