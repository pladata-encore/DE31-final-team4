from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.db.models import OuterRef, Subquery

def home(request):
    return render(request, 'main/home.html')

def custom_logout(request):
    logout(request)
    # request.session.flush() 
    return redirect('home')

def economic_awareness_test(request):
    return render(request, 'main/economic_awareness_test.html')

# 추가된 뷰 함수들

def google_login(request):
    # Google 로그인 처리 로직을 여기에 추가
    return redirect('home')  # 로그인 후 홈 페이지로 리디렉션

def google_callback(request):
    # Google 로그인 콜백 처리 로직을 여기에 추가
    return redirect('home')  # 콜백 처리 후 홈 페이지로 리디렉션

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter  # Google OAuth 어댑터를 사용하여 로그인 처리

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import TestOption, Question, Answer

def test_option_1(request):
    test_option = get_object_or_404(TestOption, name="Test Option 1")
    questions = Question.objects.filter(test_option=test_option)

    if request.method == 'POST':
        selected_answers = []
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                selected_answer = get_object_or_404(Answer, pk=answer_id)
                selected_answers.append(selected_answer)

        # 선택된 답변에 따라 점수 또는 결과를 계산하는 로직 추가
        return render(request, 'main/result.html', {'selected_answers': selected_answers})

    return render(request, 'main/test_option_1.html', {'questions': questions})

def test_option_2(request):
    test_option = get_object_or_404(TestOption, name="Test Option 2")
    questions = Question.objects.filter(test_option=test_option)

    if request.method == 'POST':
        selected_answers = []
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                selected_answer = get_object_or_404(Answer, pk=answer_id)
                selected_answers.append(selected_answer)

        # 선택된 답변에 따라 점수 또는 결과를 계산하는 로직 추가
        return render(request, 'main/result.html', {'selected_answers': selected_answers})

    return render(request, 'main/test_option_2.html', {'questions': questions})

def test_option_3(request):
    test_option = get_object_or_404(TestOption, name="Test Option 3")
    questions = Question.objects.filter(test_option=test_option)

    if request.method == 'POST':
        selected_answers = []
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                selected_answer = get_object_or_404(Answer, pk=answer_id)
                selected_answers.append(selected_answer)

        # 선택된 답변에 따라 점수 또는 결과를 계산하는 로직 추가
        return render(request, 'main/result.html', {'selected_answers': selected_answers})

    return render(request, 'main/test_option_3.html', {'questions': questions})


#서칭
from .models import DataWarehouse
from django.db.models import Q

def search_datawarehouse(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = DataWarehouse.objects.filter(
            Q(term__icontains=query) | Q(details__icontains=query)
        )
    if not results:
        message = "No results found."
    else:
        message = None
    
    return render(request, 'base.html', {'results': results, 'message': message, 'query': query})




import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.utils import timezone
from django.shortcuts import render
from stocks.models import Market
from datetime import datetime
import pandas as pd

# 그래프를 생성하고 base64로 인코딩하는 함수
def add_graphs():
    # 오늘 날짜의 시작 시간과 끝 시간 설정 (오전 9시 ~ 오후 4시)
    today_start = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
    today_end = timezone.now().replace(hour=16, minute=0, second=0, microsecond=0)

    # KOSPI 및 KOSDAQ 데이터 중 오늘 날짜의 데이터만 가져옴
    kospi_data = Market.objects.filter(StockName="KOSPI", price_time__range=[today_start, today_end])
    kosdaq_data = Market.objects.filter(StockName="KOSDAQ", price_time__range=[today_start, today_end])

    # 데이터가 없을 때 대비 (빈 그래프 생성)
    if not kospi_data.exists():
        kospi_data = Market.objects.filter(StockName="KOSPI").order_by('-price_time')[:10]
    if not kosdaq_data.exists():
        kosdaq_data = Market.objects.filter(StockName="KOSDAQ").order_by('-price_time')[:10]

    # 데이터를 pandas DataFrame으로 변환 (시간 순으로 정렬)
    kospi_df = pd.DataFrame(list(kospi_data.values('price_time', 'CurrentPoint')))
    kosdaq_df = pd.DataFrame(list(kosdaq_data.values('price_time', 'CurrentPoint')))

    # 쉼표 제거 후 숫자로 변환
    kospi_df['CurrentPoint'] = kospi_df['CurrentPoint'].str.replace(',', '')
    kospi_df['CurrentPoint'] = pd.to_numeric(kospi_df['CurrentPoint'], errors='coerce')

    kosdaq_df['CurrentPoint'] = kosdaq_df['CurrentPoint'].str.replace(',', '')
    kosdaq_df['CurrentPoint'] = pd.to_numeric(kosdaq_df['CurrentPoint'], errors='coerce')

    # 선형 보간 적용 (결측값을 선형으로 보간)
    kospi_df['CurrentPoint'] = kospi_df['CurrentPoint'].interpolate(method='linear')
    kosdaq_df['CurrentPoint'] = kosdaq_df['CurrentPoint'].interpolate(method='linear')

    kospi_df['price_time'] = pd.to_datetime(kospi_df['price_time'])
    kosdaq_df['price_time'] = pd.to_datetime(kosdaq_df['price_time'])

    kospi_df = kospi_df.sort_values(by='price_time')
    kosdaq_df = kosdaq_df.sort_values(by='price_time')

    # KOSPI 그래프 생성
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(kospi_df['price_time'], kospi_df['CurrentPoint'], label="KOSPI", color="blue")
    ax1.set_title("KOSPI (Today)")
    ax1.xaxis.set_visible(True)  # 시간 축 표시
    ax1.yaxis.set_visible(True)  # 값 축 표시
    ax1.set_xlabel("Time")  # X축 레이블 설정
    ax1.set_ylabel("CurrentPoint")  # Y축 레이블 설정

    # KOSDAQ 그래프 생성
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(kosdaq_df['price_time'], kosdaq_df['CurrentPoint'], label="KOSDAQ", color="green")
    ax2.set_title("KOSDAQ (Today)")
    ax2.xaxis.set_visible(True)  # 시간 축 표시
    ax2.yaxis.set_visible(True)  # 값 축 표시
    ax2.set_xlabel("Time")  # X축 레이블 설정
    ax2.set_ylabel("CurrentPoint")  # Y축 레이블 설정

    # KOSPI 그래프를 base64로 인코딩
    buffer1 = BytesIO()
    fig1.savefig(buffer1, format="png")
    buffer1.seek(0)
    image_png1 = buffer1.getvalue()
    buffer1.close()
    graphic1 = base64.b64encode(image_png1).decode('utf-8')

    # KOSDAQ 그래프를 base64로 인코딩
    buffer2 = BytesIO()
    fig2.savefig(buffer2, format="png")
    buffer2.seek(0)
    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic2 = base64.b64encode(image_png2).decode('utf-8')

    return graphic1, graphic2

def home(request):

    # 그래프 데이터 생성
    graphic1, graphic2 = add_graphs()

    # 가장 최근의 KOSPI 및 KOSDAQ 데이터 가져오기
    kospi = Market.objects.filter(StockName='KOSPI').order_by('-price_time').first()
    kosdaq = Market.objects.filter(StockName='KOSDAQ').order_by('-price_time').first()

    # 템플릿에 전달할 값 설정
    context = {
        'graphic1': graphic1,
        'graphic2': graphic2,
        'KOSPI_UpDownPoint': kospi.UpDownPoint if kospi else 'N/A',
        'KOSPI_UpDownRate': kospi.UpDownRate if kospi else 'N/A',
        'KOSDAQ_UpDownPoint': kosdaq.UpDownPoint if kosdaq else 'N/A',
        'KOSDAQ_UpDownRate': kosdaq.UpDownRate if kosdaq else 'N/A',
    }

    # 템플릿 렌더링
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html')

# 관심종목
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RealTimeStock, UserStock, Mbti, TestResult

@login_required
def add_favorite_list(request, stock_code):
    # 가장 최신의 stock 정보를 real_time 테이블에서 가져오기
    latest_stock = RealTimeStock.objects.filter(stock_code=stock_code).order_by('-id').first()

    if latest_stock is not None:
        stock_mbti = Mbti.objects.filter(stock_code=stock_code).first()

        UserStock.objects.get_or_create(
            user=request.user,
            stock_id=latest_stock,
            defaults={'stock_code': latest_stock.stock_code, 'mbti': stock_mbti}
        )
        return redirect('mypage')
    else:
        return redirect('mypage')

    
@login_required
def my_favorite_list(request):
    user_stocks = UserStock.objects.filter(user=request.user).select_related('stock_id')
    stock_info = {}
    
    # 각 stock_code의 최신 RealTimeStock 객체를 선택합니다.
    for user_stock in user_stocks:
        stock_code = user_stock.stock_id.stock_code
        # 최신 RealTimeStock 객체를 가져옵니다.
        latest_stock = RealTimeStock.objects.filter(stock_code=stock_code).order_by('-id').first()
        if latest_stock:
            stock_mbti = Mbti.objects.filter(stock_code=stock_code).first()
            mbti_value = stock_mbti.mbti if stock_mbti else None
            if stock_code not in stock_info or latest_stock.id > stock_info[stock_code]['id']:
                stock_info[stock_code] = {
                    'stock_code': latest_stock.stock_code,
                    'name': latest_stock.name,
                    'current_price': latest_stock.current_price,
                    'UpDownRate': latest_stock.UpDownRate,
                    'UpDownPoint': latest_stock.UpDownPoint,
                    'id': latest_stock.id,
                    'mbti': mbti_value
                }
    
    # stock_info의 값을 리스트로 변환하고, id 기준으로 정렬합니다.
    stock_info_list = list(stock_info.values())
    stock_info_list.sort(key=lambda x: x['id'], reverse=True)
    
    return render(request, 'mypage/mypage.html', {'stock_info': stock_info_list})

from django.shortcuts import redirect, get_object_or_404
from .models import UserStock

@login_required
def remove_stock(request, stock_code):
    # 사용자와 일치하는 모든 UserStock 객체를 가져옵니다.
    user_stocks = UserStock.objects.filter(stock_code=stock_code, user=request.user)
    
    # 가져온 모든 객체를 삭제합니다.
    for user_stock in user_stocks:
        user_stock.delete()

    # 원래 페이지로 리디렉션
    return redirect('mypage')

@login_required
def user_test_results(request):
    test_results = TestResult.objects.filter(user=request.user).first()
    
    context = {
        'test_results': test_results
    }

    return render(request, 'mypage/mypage.html', context)
