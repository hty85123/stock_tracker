# 使用 Python 3.9 作為基礎映像
FROM python:3.9-slim

# 設置環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Taipei

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt
COPY requirement.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirement.txt

# 複製專案文件
COPY . .

# 建立資料卷掛載點
VOLUME ["/app/data"]

# 暴露端口
EXPOSE 8000

# 啟動命令
CMD ["sh", "-c", "python manage.py migrate && python manage.py init_stocks && python manage.py runserver 0.0.0.0:8000"]
