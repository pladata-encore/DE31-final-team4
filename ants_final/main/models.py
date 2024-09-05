from django.db import models

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
    
# 관심종목
from django.contrib.auth.models import User

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} 관심종목: {self.stock.name}'




#서칭
class DataWarehouse(models.Model):
    topic = models.CharField(max_length=100)
    term = models.CharField(max_length=255)
    details = models.TextField()

    class Meta:
        db_table = 'dictionary'  # 데이터베이스 테이블 이름을 'dictionary'로 지정

    def __str__(self):
        return self.term
