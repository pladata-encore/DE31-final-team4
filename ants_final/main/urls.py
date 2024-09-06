from django.urls import path
from allauth.socialaccount.providers.google.views import oauth2_login, oauth2_callback

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('economic-awareness-test/', views.economic_awareness_test, name='economic_awareness_test'),
    
   

    # 구글 소셜 로그인
    # path("google/login/", views.google_login, name="google_login"),
    # path("google/callback/", views.google_callback, name="google_callback"),
    # path("google/login/finish/", views.GoogleLogin.as_view(), name="google_login_finish"),
    path('accounts/google/login/', oauth2_login, name='google_login'),  # 구글 로그인 URL
    path('accounts/google/callback/', oauth2_callback, name='google_callback'),  # 구글 콜백 URL
    path('accounts/google/login/finish/', views.GoogleLogin.as_view(), name='google_login_finish'),  # 만약 필요한 경우 추가 뷰

    # 테스트 페이지
    path('test-option-1/', views.test_option_1, name='test_option_1'),
    path('test-option-2/', views.test_option_2, name='test_option_2'),
    path('test-option-3/', views.test_option_3, name='test_option_3'),
    
    # 검색
    path('search/', views.search_datawarehouse, name='search_datawarehouse'),

    # about 페이지
    path('about/', views.about, name='about'),
]
