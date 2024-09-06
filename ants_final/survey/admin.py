from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SurveyQuestion, SurveyResponse

admin.site.register(SurveyQuestion)
admin.site.register(SurveyResponse)
