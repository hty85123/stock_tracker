import pandas as pd
import logging

logger = logging.getLogger(__name__)

def calculate_moving_averages(records_df):
    """計算移動平均線"""
    # 創建 DataFrame 的副本以避免 SettingWithCopyWarning
    df = records_df.copy()
    df.loc[:, 'ma5'] = df['Close'].rolling(window=5).mean()
    df.loc[:, 'ma20'] = df['Close'].rolling(window=20).mean()
    return df

def check_golden_cross(records_df):
    """檢查是否出現黃金交叉"""
    if len(records_df) < 2:
        return False
    
    today = records_df.iloc[-1]
    yesterday = records_df.iloc[-2]
    
    if pd.notna(today['ma5']) and pd.notna(today['ma20']) and \
       pd.notna(yesterday['ma5']) and pd.notna(yesterday['ma20']):
        if yesterday['ma5'] <= yesterday['ma20'] and today['ma5'] > today['ma20']:
            return True
    return False

def check_death_cross(records_df):
    """檢查是否出現死亡交叉"""
    if len(records_df) < 2:
        return False
    
    today = records_df.iloc[-1]
    yesterday = records_df.iloc[-2]
    
    if pd.notna(today['ma5']) and pd.notna(today['ma20']) and \
       pd.notna(yesterday['ma5']) and pd.notna(yesterday['ma20']):
        if yesterday['ma5'] >= yesterday['ma20'] and today['ma5'] < today['ma20']:
            return True
    return False

def analyze_stock(stock_data):
    """分析股票數據並發送通知"""
    # 確保我們使用的是 DataFrame
    if isinstance(stock_data, pd.Series):
        df = pd.DataFrame([stock_data])
    else:
        df = pd.DataFrame(stock_data)
    
    # 計算技術指標
    df = calculate_moving_averages(df)
    
    signals = []
    
    # 檢查黃金交叉
    if check_golden_cross(df):
        signals.append(f"黃金交叉: 5日均線突破20日均線，可能為買入訊號")
    
    # 檢查死亡交叉
    if check_death_cross(df):
        signals.append(f"死亡交叉: 5日均線跌破20日均線，可能為賣出訊號")
    
    return df, signals