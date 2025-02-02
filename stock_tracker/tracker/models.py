from django.db import models

# Create your models here.

class Stock(models.Model):
    tickername = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tickername

class Record(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='records')
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    date = models.DateField()
    ma5 = models.FloatField(null=True, blank=True)  # 5日均線
    ma20 = models.FloatField(null=True, blank=True)  # 20日均線
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('stock', 'date')# 確保同一支股票同一天只有一筆資料
