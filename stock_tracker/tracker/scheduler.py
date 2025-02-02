from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import logging
from datetime import timedelta, date
import atexit
import yfinance as yf
from .models import Stock, Record
from django.db import IntegrityError
from tenacity import retry, stop_after_attempt, wait_exponential

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

scheduler = None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_stock_data():
    """
    從Yahoo Finance API獲取股票資料並存入資料庫
    """
    logger.info("正在獲取股票資料...")
    
    # 取得所有要追蹤的股票
    stocks = Stock.objects.all()
    if not stocks:
        logger.warning("沒有追蹤的股票")
        return
        
    # 設定日期範圍
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    try:
        # 建立股票代號列表
        tickers = ' '.join([stock.tickername for stock in stocks])
        
        # 一次性下載所有股票資料
        data = yf.download(
            tickers,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            interval='1d',
            group_by='ticker'
        )
        
        # 處理單一股票和多股票的資料結構差異
        if len(stocks) == 1:
            data = {stocks[0].tickername: data}
        
        # 為每支股票處理資料
        for stock in stocks:
            try:
                stock_data = data[stock.tickername]
                
                for index, row in stock_data[::-1].iterrows():
                    try:
                        Record.objects.create(
                            stock=stock,
                            date=index.date(),
                            open=row['Open'],
                            high=row['High'],
                            low=row['Low'],
                            close=row['Close']
                        )
                    except IntegrityError:
                        logger.debug(f"股票 {stock.tickername} 在 {index.date()} 及之前的資料已存在")
                        break
                
                logger.info(f"成功更新股票 {stock.tickername} 的資料")
                
            except Exception as e:
                logger.error(f"處理股票 {stock.tickername} 資料時發生錯誤: {str(e)}")
                
    except Exception as e:
        logger.error(f"下載股票資料時發生錯誤: {str(e)}", exc_info=True)

def start():
    global scheduler
    if not getattr(settings, 'SCHEDULER_AUTOSTART', True):
        logger.info("排程器已被設定為停用")
        return

    if scheduler is None:
        logger.info("正在初始化排程器...")
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            fetch_stock_data,
            'interval',  # 改用 interval 設定
            minutes=1,   # 每分鐘執行一次
            # 'cron',
            # hour=16,  # 設定在每天下午 4 點執行
            # minute=00,
            id='fetch_stock_data_job',
            replace_existing=True
        )
        scheduler.start()
        logger.info("排程器已啟動，設定為每天下午 4 點執行")
        
        atexit.register(lambda: scheduler.shutdown()) 