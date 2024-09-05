from django.contrib import admin

# Register your models here.
# main/admin.py
from .models import TestOption, Question, Answer

admin.site.register(TestOption)
admin.site.register(Question)
admin.site.register(Answer)


# 관심종목
from .models import Stock, UserStock

admin.site.register(Stock)
admin.site.register(UserStock)