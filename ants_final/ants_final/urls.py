"""
URL configuration for ants_final project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth.views import LogoutView  # 로그아웃 뷰 가져오기

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # main 앱의 URL을 메인으로 연결
    path('accounts/logout/', views.custom_logout, name='logout'),  # custom_logout 사용
    path('accounts/', include('allauth.urls')),  # allauth를 통한 계정 관리




]