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
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import TestResult, TestResult2
import json

@csrf_exempt
@login_required
@require_POST
def save_test_result_option1(request):
    try:
        data = json.loads(request.body)
        result1 = data.get('result1')
        result2 = data.get('result2')

        # TestResult 모델에 결과 저장
        TestResult.objects.update_or_create(
            user=request.user,
            defaults={'result1': result1, 'result2': result2}
        )
        
        return JsonResponse({'status': 'success'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
@require_POST
def save_test_result_option2(request):
    try:
        data = json.loads(request.body)
        result1 = data.get('result1')
        result2 = data.get('result2')

        # TestResult2 모델에 결과 저장
        TestResult2.objects.update_or_create(
            user=request.user,
            defaults={'result1': result1, 'result2': result2}
        )
        
        return JsonResponse({'status': 'success'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def mypage(request):
    try:
        test_result = TestResult.objects.filter(user=request.user).first()
        test_result2 = TestResult2.objects.filter(user=request.user).first()
    except TestResult.DoesNotExist:
        test_result = None
    except TestResult2.DoesNotExist:
        test_result2 = None

    return render(request, 'mypage.html', {'test_result': test_result, 'test_result2': test_result2})


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

from django.db.models import Max

def home(request):

    # 그래프 데이터 생성
    graphic1, graphic2 = add_graphs()

    # 가장 최근의 KOSPI 및 KOSDAQ 데이터 가져오기
    kospi = Market.objects.filter(StockName='KOSPI').order_by('-price_time').first()
    kosdaq = Market.objects.filter(StockName='KOSDAQ').order_by('-price_time').first()

    # RealTime 테이블에서 가장 최신의 데이터를 기준으로 필터링
    latest_time = RealTime.objects.aggregate(latest_time=Max('price_time'))['latest_time']

    # 최신 데이터를 기준으로 필터링한 후, 상승/하락 종목을 정렬
    type_choice = request.GET.get('type', 'rising')  # 기본값은 'rising'
    
    if type_choice == 'rising':
        stocks = RealTime.objects.filter(price_time=latest_time, UpDownPoint__gt=0).order_by('-UpDownRate')[:10]  # 급상승 순서
    else:
        stocks = RealTime.objects.filter(price_time=latest_time, UpDownPoint__lt=0).order_by('UpDownRate')[:10]  # 급하락 순서
    
    # 템플릿에 전달할 값 설정
    context = {
        'graphic1': graphic1,
        'graphic2': graphic2,
        'KOSPI_UpDownPoint': kospi.UpDownPoint if kospi else 'N/A',
        'KOSPI_UpDownRate': kospi.UpDownRate if kospi else 'N/A',
        'KOSDAQ_UpDownPoint': kosdaq.UpDownPoint if kosdaq else 'N/A',
        'KOSDAQ_UpDownRate': kosdaq.UpDownRate if kosdaq else 'N/A',
        'stocks': stocks,
        'type': type_choice  # 급상승/급하락 차트 선택
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
        print("stock_mbti : ", stock_mbti.mbti)
        UserStock.objects.get_or_create(
            user=request.user,
            stock_id=latest_stock,
            defaults={'stock_code': latest_stock.stock_code, 'mbti': stock_mbti.mbti}
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

from stocks.models import OnceTime
import json
from .models import DividendVolatility, Mbti, News
# stock_detail_page 브랜치에서 생성
# localhost:8000/stock으로 들어가면 해당 페이지 리턴
def stock_detail_page(request, stock_code="005930"):
    # 종목 코드를 이용해서 주식 정보를 DB에서 가져오는 코드
    stock_data = OnceTime.objects.filter(stock_code=stock_code).order_by('date')
    dividend_data = get_object_or_404(DividendVolatility, stock_code=stock_code)
    
    # 주식 mbti 정보 가져오기
    stock_mbti = get_object_or_404(Mbti, stock_code=stock_code)

    # news 정보 가져오기
    news_list = News.objects.filter(stock_code=stock_code).order_by('-pubDate')[:3]
    
    # 날짜 및 종가 데이터를 JSON 형태로 변환
    dates = [str(x.date) for x in stock_data]
    closing_prices = [x.closing_price for x in stock_data]
    
    context = {
        'stock_code': stock_code,
        'dates': json.dumps(dates),  # JSON으로 직렬화
        'closing_prices': json.dumps(closing_prices),  # JSON으로 직렬화
        'name': stock_data.first().name,
        'prev_dividend_rate': dividend_data.prev_dividend_rate ,
        'pred_dividend_rate': dividend_data.pred_dividend_rate ,
        'dividend_stability': dividend_data.dividend_stability, 
        'volatility': dividend_data.volatility,
        'year': dividend_data.year,
        'mbti': stock_mbti.mbti,
        'news_list': news_list,
    }
    return render(request, 'main/stock_detail.html', context)

from django.http import JsonResponse

def load_news(request):
    stock_code = request.GET.get('stock_code')
    page = int(request.GET.get('page', 1))
    page_size = 3
    start = (page - 1) * page_size
    end = start + page_size
    news_list = News.objects.filter(stock_code=stock_code).order_by('-pubDate')[start:end]
    data = {
        'news_list': [{'title': news.title, 'description': news.description, 'pubDate': str(news.pubDate), 'originallink': news.originallink} for news in news_list]
    }
    
    return JsonResponse(data)

def stock_search(request):
    stock_query = request.GET.get('stock_query', '')

    # 종목 코드 또는 종목명으로 검색
    stock = RealTime.objects.filter(Q(stock_code=stock_query) | Q(name=stock_query)).first()  # 종목 코드 혹은 종목명으로 검색
    print(stock)
    # 검색 성공 시 해당 주식 상세 페이지로 리디렉션
    if stock is not None:
        return redirect('stock', stock_code=stock.stock_code)
    return render(request, 'main/no_results.html', {'stock_query': stock_query})
    
    





