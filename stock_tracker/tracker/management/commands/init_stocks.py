from django.core.management.base import BaseCommand
from tracker.models import Stock

# 使用指令 "python manage.py init_stocks" 來初始化資料庫中的股票資料
class Command(BaseCommand):
    help = '初始化資料庫中的股票資料'

    def handle(self, *args, **kwargs):
        # 預設的股票代碼列表
        default_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        
        for ticker in default_stocks:
            # 使用 get_or_create 來避免重複插入
            stock, created = Stock.objects.get_or_create(
                tickername=ticker
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'成功新增股票: {ticker}'))
            else:
                self.stdout.write(self.style.WARNING(f'股票已存在: {ticker}')) 