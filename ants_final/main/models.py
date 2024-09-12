from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# main/models.py

class TestOption(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    test_option = models.ForeignKey(TestOption, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    points = models.IntegerField()

    def __str__(self):
        return self.text
    
#서칭
class DataWarehouse(models.Model):
    topic = models.CharField(max_length=100)
    term = models.CharField(max_length=255)
    details = models.TextField()

    class Meta:
        db_table = 'dictionary'  # 데이터베이스 테이블 이름을 'dictionary'로 지정

    def __str__(self):
        return self.term
    

# 관심종목
# class Stock(models.Model):
#     name = models.CharField(max_length=100)
#     stock_code = models.CharField(max_length=10)

#     def __str__(self):
#         return self.name
    
#     class Meta:
#         db_table = 'stock_symbol'

# real_time table data 들고오는 모델
# class RealTimeStock(models.Model):
#     stock_code = models.CharField(max_length=10)
#     name = models.CharField(max_length=100)
#     current_price = models.DecimalField(max_digits=15, decimal_places=2)
#     UpDownRate = models.DecimalField(max_digits=15, decimal_places=2)
#     UpDownPoint = models.DecimalField(max_digits=15, decimal_places=2)
#     id = models.AutoField(primary_key=True)

#     class Meta:
#         db_table = 'real_time' 
#         unique_together = ('stock_code', 'id')

# class UserStock(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     stock_code = models.ForeignKey(RealTimeStock, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.user.username} 관심종목: {self.stock_code.name}'
    
#     class Meta:
#         db_table = 'favorite_list'
#         unique_together = ('user', 'stock_code')

##################stocks.model로 이사 갔습니다#######################################
# class RealTimeStock(models.Model):
#     stock_code = models.CharField(max_length=10)
#     name = models.CharField(max_length=100)
#     current_price = models.DecimalField(max_digits=15, decimal_places=2)
#     UpDownRate = models.DecimalField(max_digits=15, decimal_places=2)
#     UpDownPoint = models.DecimalField(max_digits=15, decimal_places=2)
#     id = models.AutoField(primary_key=True)

#     class Meta:
#         db_table = 'real_time'
#         unique_together = ('stock_code', 'id')
##########################################################################################

from stocks.models import RealTime


class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(RealTime, on_delete=models.CASCADE,db_column='stock_id')
    stock_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} 관심종목: {self.stock_code.name}'
    
    class Meta:
        db_table = 'favorite_list'
        unique_together = ('user', 'stock_code')


class DividendVolatility(models.Model):
    stock_code = models.CharField(max_length=6, primary_key=True)  # 종목코드는 문자열, 기본적으로 6자리
    prev_dividend_rate = models.FloatField()  # 전년도 배당률
    pred_dividend_rate = models.FloatField()  # 예측 배당률
    dividend_stability = models.CharField(max_length=1)  # 배당성 (A, B, C 같은 문자)
    volatility = models.CharField(max_length=1)  # 변동성
    year = models.IntegerField()  # 연도
    stock_name = models.CharField(max_length=100)  # 종목명
    
    def __str__(self):
        return f"{self.stock_name} ({self.stock_code})"
    class Meta:
        db_table = 'dividend_volatility'  # 테이블 이름을 명시적으로 설정


class Mbti(models.Model):
    stock_code = models.CharField(max_length=6, primary_key=True)  # 종목코드는 문자열, 기본적으로 6자리
    mbti = models.CharField(max_length=6)

    class Meta:
        db_table = 'mbti'  # 테이블 이름을 명시적으로 설정

class News(models.Model):
    stock_code = models.CharField(max_length=6)  # 종목코드는 문자열, 기본적으로 6자리
    name = models.CharField(max_length=100)
    pubDate = models.DateTimeField(max_length=30)
    title = models.TextField()
    description = models.TextField()
    originallink = models.TextField(primary_key=True)

    class Meta:
        db_table = 'news'  # 테이블 이름을 명시적으로 설정