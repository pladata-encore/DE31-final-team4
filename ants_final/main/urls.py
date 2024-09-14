from django.urls import path
from allauth.socialaccount.providers.google.views import oauth2_login, oauth2_callback
from .views import save_test_result
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('economic_awareness_test/', views.economic_awareness_test, name='economic_awareness_test'),
    
   

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
    
    # 테스트 결과
    
    path('save-test-result/', views.save_test_result, name='save_test_result'),
    path('save-test-result/', save_test_result, name='save_test_result'),

    
    # 검색
    path('search/', views.search_datawarehouse, name='search_datawarehouse'),

    # about 페이지
    path('about/', views.about, name='about'),

    #관심종목
    path('add_favorite_list/<str:stock_code>/', views.add_favorite_list, name='add_favorite_list'),
    path('mypage/', views.my_favorite_list, name='mypage'),
    # path('stock_/', views.my_favorite_list, name='my_favorite_list'),
    path('remove_stock/<str:stock_code>/', views.remove_stock, name='remove_stock'),

    # stock_detail_page 브랜치에서 생성
    # navigation bar 에서 stock을 누르면 해당 페이지로 이동
    path('stock/<str:stock_code>/', views.stock_detail_page, name='stock'),
    path('load-news/', views.load_news, name='load_news'),  # load_news 뷰에 연결
    
    # 주식 검색 결과를 처리할 URL
    path('stock_search/', views.stock_search, name='stock_search'),
]