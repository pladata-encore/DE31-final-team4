from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('economic-awareness-test/', views.economic_awareness_test, name='economic_awareness_test'),
    
    # 구글 소셜 로그인
    # path("google/login/", views.google_login, name="google_login"),
    # path("google/callback/", views.google_callback, name="google_callback"),
    # path("google/login/finish/", views.GoogleLogin.as_view(), name="google_login_todjango"),

    path('logout/', views.custom_logout, name='custom_logout'),


    path('test-option-1/', views.test_option_1, name='test_option_1'),
    path('test-option-2/', views.test_option_2, name='test_option_2'),
    path('test-option-3/', views.test_option_3, name='test_option_3'),

    path('search/', views.search_datawarehouse, name='search_datawarehouse'),
]
