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

# 결과 저장
class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result1 = models.CharField(max_length=100)
    result2 = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}님의 테스트 결과"

    class Meta:
        db_table = 'test_result'
    
#서칭
class DataWarehouse(models.Model):
    topic = models.CharField(max_length=100)
    term = models.CharField(max_length=255)
    details = models.TextField()

    class Meta:
        db_table = 'dictionary'  # 데이터베이스 테이블 이름을 'dictionary'로 지정

    def __str__(self):
        return self.term
    

# class RealTime(models.Model):
#     stock_code = models.CharField(max_length=10)
#     name = models.CharField(max_length=100)
#     current_price = models.DecimalField(max_digits=15, decimal_places=2)
#     UpDownRate = models.DecimalField(max_digits=15, decimal_places=2)
#     UpDownPoint = models.DecimalField(max_digits=15, decimal_places=2)
#     id = models.AutoField(primary_key=True)

#     class Meta:
#         db_table = 'real_time'
#         unique_together = ('stock_code', 'id')


from stocks.models import RealTime

# mypage
class Mbti(models.Model):
    stock_code = models.CharField(max_length=10, primary_key=True)  # 종목코드는 문자열, 기본적으로 6자리
    mbti = models.CharField(max_length=10)

    def __str__(self):
        return self.mbti
    
    class Meta:
        db_table = 'mbti'

class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(RealTime, on_delete=models.CASCADE,db_column='stock_id')
    stock_code = models.CharField(max_length=10, blank=True, null=True)
    mbti = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} 관심종목: {self.stock_code.name}'
    
    class Meta:
        db_table = 'favorite_list'
        unique_together = ('user', 'stock_code')

#test 결과   
class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result1 = models.CharField(max_length=100)
    result2 = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}님의 테스트 결과"
    
    class Meta:
        db_table = 'test_result'