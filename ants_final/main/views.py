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

@login_required
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

@login_required
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

@login_required
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


# 결과
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import TestResult
import json

@csrf_exempt
@login_required
@require_POST
def save_test_result(request):
    try:
        data = json.loads(request.body)
        result1 = data.get('result1')
        result2 = data.get('result2')
        user = request.user

        # 테스트 결과 저장
        test_result = TestResult(user=user, result1=result1, result2=result2)
        test_result.save()

        return JsonResponse({'status': 'success'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt  # AJAX 요청 시 CSRF 검사를 비활성화
@login_required  # 사용자가 로그인되어 있어야만 결과를 저장 가능
def save_test_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result1 = data.get('result1')
        result2 = data.get('result2')

        # TestResult 모델에 결과 저장
        TestResult.objects.create(user=request.user, result1=result1, result2=result2)

        return JsonResponse({'message': 'Test result saved successfully!'}, status=200)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
    # mypage에 테스트 결과 보여주기 (예송이한테 있으면 이건 삭제하고merge)
@login_required
def mypage(request):
    try:
        test_result = TestResult.objects.get(user=request.user)
    except TestResult.DoesNotExist:
        test_result = None
    
    return render(request, 'mypage.html', {'test_result': test_result})

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
# def add_graphs():
#     # 오늘 날짜의 시작 시간과 끝 시간 설정 (오전 9시 ~ 오후 4시)
#     today_start = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
#     today_end = timezone.now().replace(hour=16, minute=0, second=0, microsecond=0)

#     # KOSPI 및 KOSDAQ 데이터 중 오늘 날짜의 데이터만 가져옴
#     kospi_data = Market.objects.filter(StockName="KOSPI", price_time__range=[today_start, today_end])
#     kosdaq_data = Market.objects.filter(StockName="KOSDAQ", price_time__range=[today_start, today_end])

#     # 데이터가 없을 때 대비 (빈 그래프 생성)
#     if not kospi_data.exists():
#         kospi_data = Market.objects.filter(StockName="KOSPI").order_by('-price_time')[:10]
#     if not kosdaq_data.exists():
#         kosdaq_data = Market.objects.filter(StockName="KOSDAQ").order_by('-price_time')[:10]

#     # 데이터를 pandas DataFrame으로 변환 (시간 순으로 정렬)
#     kospi_df = pd.DataFrame(list(kospi_data.values('price_time', 'CurrentPoint')))
#     kosdaq_df = pd.DataFrame(list(kosdaq_data.values('price_time', 'CurrentPoint')))

#     # 쉼표 제거 후 숫자로 변환
#     kospi_df['CurrentPoint'] = kospi_df['CurrentPoint'].str.replace(',', '')
#     kospi_df['CurrentPoint'] = pd.to_numeric(kospi_df['CurrentPoint'], errors='coerce')

#     kosdaq_df['CurrentPoint'] = kosdaq_df['CurrentPoint'].str.replace(',', '')
#     kosdaq_df['CurrentPoint'] = pd.to_numeric(kosdaq_df['CurrentPoint'], errors='coerce')

#     # 선형 보간 적용 (결측값을 선형으로 보간)
#     kospi_df['CurrentPoint'] = kospi_df['CurrentPoint'].interpolate(method='linear')
#     kosdaq_df['CurrentPoint'] = kosdaq_df['CurrentPoint'].interpolate(method='linear')

#     kospi_df['price_time'] = pd.to_datetime(kospi_df['price_time'])
#     kosdaq_df['price_time'] = pd.to_datetime(kosdaq_df['price_time'])

#     kospi_df = kospi_df.sort_values(by='price_time')
#     kosdaq_df = kosdaq_df.sort_values(by='price_time')

#     # KOSPI 그래프 생성
#     fig1, ax1 = plt.subplots(figsize=(8, 6))
#     ax1.plot(kospi_df['price_time'], kospi_df['CurrentPoint'], label="KOSPI", color="blue")
#     ax1.set_title("KOSPI (Today)")
#     ax1.xaxis.set_visible(True)  # 시간 축 표시
#     ax1.yaxis.set_visible(True)  # 값 축 표시
#     ax1.set_xlabel("Time")  # X축 레이블 설정
#     ax1.set_ylabel("CurrentPoint")  # Y축 레이블 설정

#     # KOSDAQ 그래프 생성
#     fig2, ax2 = plt.subplots(figsize=(8, 6))
#     ax2.plot(kosdaq_df['price_time'], kosdaq_df['CurrentPoint'], label="KOSDAQ", color="green")
#     ax2.set_title("KOSDAQ (Today)")
#     ax2.xaxis.set_visible(True)  # 시간 축 표시
#     ax2.yaxis.set_visible(True)  # 값 축 표시
#     ax2.set_xlabel("Time")  # X축 레이블 설정
#     ax2.set_ylabel("CurrentPoint")  # Y축 레이블 설정

#     # KOSPI 그래프를 base64로 인코딩
#     buffer1 = BytesIO()
#     fig1.savefig(buffer1, format="png")
#     buffer1.seek(0)
#     image_png1 = buffer1.getvalue()
#     buffer1.close()
#     graphic1 = base64.b64encode(image_png1).decode('utf-8')

#     # KOSDAQ 그래프를 base64로 인코딩
#     buffer2 = BytesIO()
#     fig2.savefig(buffer2, format="png")
#     buffer2.seek(0)
#     image_png2 = buffer2.getvalue()
#     buffer2.close()
#     graphic2 = base64.b64encode(image_png2).decode('utf-8')

#     return graphic1, graphic2

# def home(request):

#     # 그래프 데이터 생성
#     graphic1, graphic2 = add_graphs()

#     # 가장 최근의 KOSPI 및 KOSDAQ 데이터 가져오기
#     kospi = Market.objects.filter(StockName='KOSPI').order_by('-price_time').first()
#     kosdaq = Market.objects.filter(StockName='KOSDAQ').order_by('-price_time').first()

#     # 템플릿에 전달할 값 설정
#     context = {
#         'graphic1': graphic1,
#         'graphic2': graphic2,
#         'KOSPI_UpDownPoint': kospi.UpDownPoint if kospi else 'N/A',
#         'KOSPI_UpDownRate': kospi.UpDownRate if kospi else 'N/A',
#         'KOSDAQ_UpDownPoint': kosdaq.UpDownPoint if kosdaq else 'N/A',
#         'KOSDAQ_UpDownRate': kosdaq.UpDownRate if kosdaq else 'N/A',
#     }

#     # 템플릿 렌더링
#     return render(request, 'main/home.html', context)

import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
from django.utils import timezone
from django.shortcuts import render

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
    
    # 가장 최근의 KOSPI CurrentPoint 가져오기
    latest_kospi_point = kospi_df['CurrentPoint'].iloc[-1]  # 마지막 값
    
    # 차트 색상 결정
    if latest_kospi_point > 0:
        color = "red"
    elif latest_kospi_point < 0:
        color = "blue"
    else:
        color = "gray"
    
    # 그래프 그리기
    ax1.plot(kospi_df['price_time'], kospi_df['CurrentPoint'], label="KOSPI", color=color)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_visible(False)
    
    # KOSDAQ 그래프 생성
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    # 가장 최근의 KOSDAQ CurrentPoint 가져오기
    latest_kosdaq_point = kosdaq_df['CurrentPoint'].iloc[-1]  # 마지막 값
    
    # 차트 색상 결정
    if latest_kosdaq_point > 0:
        color = "red"
    elif latest_kosdaq_point < 0:
        color = "blue"
    else:
        color = "gray"
    
    # 그래프 그리기
    ax2.plot(kosdaq_df['price_time'], kosdaq_df['CurrentPoint'], label="KOSDAQ", color=color)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.xaxis.set_visible(False)
    ax2.yaxis.set_visible(False)

    # KOSPI 그래프를 base64로 인코딩
    buffer1 = BytesIO()
    fig1.savefig(buffer1, format="png", bbox_inches='tight', pad_inches=0)
    buffer1.seek(0)
    image_png1 = buffer1.getvalue()
    buffer1.close()
    graphic1 = base64.b64encode(image_png1).decode('utf-8')

    # KOSDAQ 그래프를 base64로 인코딩
    buffer2 = BytesIO()
    fig2.savefig(buffer2, format="png", bbox_inches='tight', pad_inches=0)
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
        'KOSPI_CurrentPoint' : kospi.CurrentPoint if kospi else 'N/A',
        'KOSDAQ_UpDownPoint': kosdaq.UpDownPoint if kosdaq else 'N/A',
        'KOSDAQ_UpDownRate': kosdaq.UpDownRate if kosdaq else 'N/A',
        'KOSDAQ_CurrentPoint' : kosdaq.CurrentPoint if kosdaq else 'N/A',
        
    }

    # 템플릿 렌더링
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html')


# 관심종목
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserStock, Mbti, TestResult
from stocks.models import RealTime
from django.db.models import Count

@login_required
def add_favorite_list(request, stock_code):
    # 가장 최신의 stock 정보를 real_time 테이블에서 가져오기
    latest_stock = RealTime.objects.filter(stock_code=stock_code).order_by('-id').first()

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
    user = request.user

    # 관심 종목
    user_stocks = UserStock.objects.filter(user=request.user).select_related('stock_id')
    stock_info = {}

    my_list = []
    mbti_value = ""
    stock_infos_list = []
    stock_info_list = []
    test_results = []

    
    if not user_stocks.exists():
    # 빈 데이터를 처리하는 로직을 추가하거나, 필요한 경우 예외처리
        context = {
            'mbti_stock': stock_infos_list,
            'mbti': mbti_value,
            'stock_info': stock_info_list,
            'test_results': test_results,
            'my_list' : my_list,
        }
        return render(request, 'mypage/mypage.html', context)
    
    else:
        for user_stock in user_stocks:
            stock_code = user_stock.stock_id.stock_code
            # 최신 RealTime 객체를 가져옵니다.
            latest_stock = RealTime.objects.filter(stock_code=stock_code).order_by('-id').first()
            if latest_stock:
                stock_mbti = Mbti.objects.filter(stock_code=stock_code).first()
                mbti_value = stock_mbti.mbti if stock_mbti else None
                if stock_code not in stock_info or (stock_info.get(stock_code) and latest_stock.id > stock_info[stock_code].get('id', 0)):
                    stock_info[stock_code] = {
                        'stock_code': latest_stock.stock_code,
                        'name': latest_stock.name,
                        'current_price': latest_stock.current_price,
                        'UpDownRate': latest_stock.UpDownRate,
                        'UpDownPoint': latest_stock.UpDownPoint,
                        'id': latest_stock.id,
                        'mbti': mbti_value
                    }
            my_list.append(stock_code)

    stock_info_list = list(stock_info.values())
    stock_info_list.sort(key=lambda x: x['id'], reverse=True)
    
    # mbti 별 추천 종목
    most_mbti = UserStock.objects.filter(user=user) \
        .values('mbti') \
        .annotate(mbti_count=Count('mbti')) \
        .order_by('-mbti_count') \
        .first()

    mbti_value = most_mbti['mbti']

    # 2. Mbti 모델에서 해당 mbti에 해당하는 모든 stock_code를 구함
    mbti_stocks = Mbti.objects.filter(mbti=mbti_value).values_list('stock_code', flat=True)

    # 3. RealTime에서 해당 stock_code에 대한 주식 정보를 pbr과 -id 기준으로 정렬 후 상위 10개 가져오기
    latest_stocks = RealTime.objects.filter(stock_code__in=mbti_stocks) \
        .order_by('-id', 'pbr')[:10]

    stock_info = {}

    for latest_stock in latest_stocks:
        stock_code = latest_stock.stock_code

        # Mbti 모델에서 해당 stock_code에 대한 MBTI 값을 가져옵니다.
        stock_mbti = Mbti.objects.filter(stock_code=stock_code).first()
        mbti_value = stock_mbti.mbti if stock_mbti else None

        # stock_info 딕셔너리에 주식 정보를 추가합니다.
        stock_info[stock_code] = {
            'stock_code': latest_stock.stock_code,
            'name': latest_stock.name,
            'current_price': latest_stock.current_price,
            'UpDownRate': latest_stock.UpDownRate,
            'UpDownPoint': latest_stock.UpDownPoint,
            'id': latest_stock.id,
            # 'mbti': mbti_value
        }

    # 데이터를 리스트로 변환
    stock_infos_list = list(stock_info.values())
    

    # 테스트 결과 확인용
    test_results = TestResult.objects.filter(user=request.user).first()

    context = {
        'mbti_stock': stock_infos_list,
        'mbti': mbti_value,
        'stock_info': stock_info_list,
        'test_results': test_results,
        'my_list' : my_list,
    }

    return render(request, 'mypage/mypage.html', context)


from django.shortcuts import redirect, get_object_or_404
from .models import UserStock

@login_required
def remove_stock(request, stock_code):
    user_stocks = UserStock.objects.filter(stock_code=stock_code, user=request.user)
    
    for user_stock in user_stocks:
        user_stock.delete()

    return redirect('mypage')