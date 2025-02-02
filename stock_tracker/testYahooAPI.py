import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, date

# 設定參數
end_date = datetime.now()
end_date = date.today()
start_date = end_date - timedelta(days=60)  # 取得最近60天的數據
interval = '1d'  # 設定時間週期為 1 天

ticker = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
sp500_data = yf.download(
    ticker, 
    start=start_date.strftime('%Y-%m-%d'),
    end=end_date.strftime('%Y-%m-%d'),
    interval=interval
)

# 顯示數據
print("\n取得的數據範圍：")
print(f"開始時間：{start_date.strftime('%Y-%m-%d')}")
print(f"結束時間：{end_date.strftime('%Y-%m-%d')}")
print("\n數據預覽：")
print(sp500_data)