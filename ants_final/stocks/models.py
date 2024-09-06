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





        


