from django.db import models

class OnceTime(models.Model):
    stock_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    date = models.DateField()
    closing_price = models.IntegerField()
    hts_total = models.IntegerField()
    prev_trading = models.IntegerField()
    MA5 = models.FloatField(null=True, blank=True)
    MA20 = models.FloatField(null=True, blank=True)
    MA60 = models.FloatField(null=True, blank=True)
    MA120 = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'once_time'
        unique_together = (('stock_code', 'date'),)
        ordering = ['-date']

    def __str__(self):
        return f"{self.stock_code} - {self.date}"
    
class FilteredOnceTime(models.Model):
    stock_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    closing_price = models.BigIntegerField()
    date = models.DateField()

    class Meta:
        db_table = 'filtered_once_time'  
        unique_together = ('stock_code', 'date')  # 복합 기본 키로 설정된 항목
    
    def __str__(self):
        return f"{self.stock_code} - {self.date}"

class Market(models.Model):
    StockName = models.CharField(max_length=255, db_column='StockName', primary_key=True)
    CurrentPoint = models.TextField(null=True, blank=True, db_column='CurrentPoint')
    UpDownPoint = models.TextField(null=True, blank=True, db_column='UpDownPoint')
    UpDownRate = models.TextField(null=True, blank=True, db_column='UpDownRate')
    UpDownFlag = models.TextField(null=True, blank=True, db_column='UpDownFlag')
    price_time = models.DateTimeField(db_column='price_time')

    class Meta:
        db_table = 'market'
        ordering = ['-price_time']
        unique_together = (('StockName', 'price_time'),)

        
class RealTime(models.Model):
    stock_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    market = models.CharField(max_length=10)
    status_code = models.CharField(max_length=20, null=False, blank=False)
    current_price = models.IntegerField()
    UpDownPoint = models.IntegerField(null=True, blank=True)
    PlusMinus = models.IntegerField(null=True, blank=True)
    UpDownRate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    opening_price = models.IntegerField(null=True, blank=True)
    high_price = models.IntegerField(null=True, blank=True)
    low_price = models.IntegerField(null=True, blank=True)
    price_time = models.DateTimeField(null=True, blank=True)
    per = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pbr = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stockcount = models.IntegerField(null=True, blank=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'real_time'
        unique_together = ('stock_code', 'id')

    def __str__(self):
        return self.name