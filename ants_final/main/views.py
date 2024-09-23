from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.db.models import OuterRef, Subquery

# def home(request):
#     return render(request, 'main/home.html')

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
from django.http import JsonResponse
from .models import DataWarehouse
from django.db.models import Q

def search_datawarehouse(request):
    query = request.GET.get('q', '')  # 쿼리 파라미터 'q'를 가져옴
    results = []
    
    # 검색어가 있을 경우 필터링 수행
    if query:
        results = DataWarehouse.objects.filter(
            Q(term__icontains=query) | Q(details__icontains=query)
        ).values('term', 'details')  # 검색 결과에서 term과 details만 반환
    
    if not results:
        return JsonResponse({'results': [], 'message': "No results found."})

    return JsonResponse({'results': list(results), 'message': None})






import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.utils import timezone
from django.shortcuts import render
from stocks.models import Market
from datetime import datetime
import pandas as pd

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
    type_choice = request.GET.get('type', '급상승')  # 기본값은 'rising'
    
    if type_choice == '급상승':
        stocks = RealTime.objects.filter(price_time=latest_time, UpDownPoint__gt=0).order_by('-UpDownRate')[:10]  # 급상승 순서
    else:
        stocks = RealTime.objects.filter(price_time=latest_time, UpDownPoint__lt=0).order_by('UpDownRate')[:10]  # 급하락 순서

    # 상위 3개의 섹터 데이터를 가져옴
    top_sectors = get_top_sectors()
    
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
        'stocks': stocks,
        'type': type_choice,  # 급상승/급하락 차트 선택
        'top_sectors': top_sectors  # 추가된 섹터 정보
    }

    # 템플릿 렌더링
    return render(request, 'main/home.html', context)


def about(request):
    return render(request, 'main/about.html')



# #####트리맵
from django.shortcuts import render
from stocks.models import FilteredOnceTime, RealTime  # 사용 중인 모델을 임포트
import plotly.express as px  # Plotly 사용
from django.db import connection
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def load_stock_data(selected_market, selected_time_period):
    # 가장 최근의 real_time 데이터의 마지막 업데이트 시간 가져오기
    with connection.cursor() as cursor:
        cursor.execute('SELECT MAX(price_time) FROM real_time WHERE market = %s', [selected_market])
        last_price_time = cursor.fetchone()[0]

    # print(f"Last price time: {last_price_time}")  # 마지막 업데이트 시간 확인

    # 선택한 기간에 맞는 과거 시간을 계산
    if selected_time_period == '1 Day':
        time_threshold = last_price_time  # 1일 선택 시 현재 시점 그대로 사용
    elif selected_time_period == '1 Week':
        time_threshold = last_price_time - timedelta(weeks=1)
    elif selected_time_period == '1 Month':
        time_threshold = last_price_time - timedelta(days=30)
    elif selected_time_period == '3 Months':
        time_threshold = last_price_time - timedelta(days=90)
    elif selected_time_period == '6 Months':
        time_threshold = last_price_time - timedelta(days=180)
    elif selected_time_period == '1 Year':
        time_threshold = last_price_time - timedelta(days=365)
    else:
        time_threshold = last_price_time  # 기본적으로 1일 기준

    # print(f"Time threshold for {selected_time_period}: {time_threshold}")  # 선택한 기간의 과거 시간 확인

    # 1일 기간 쿼리: 조인 없이 real_time 테이블에서만 데이터를 가져옴
    if selected_time_period == '1 Day':
        query = '''
        SELECT stock_code, name, sector, market, current_price, stockcount, UpDownRate, price_time
        FROM real_time
        WHERE market = %s AND price_time = %s;
        '''
        with connection.cursor() as cursor:
            cursor.execute(query, (selected_market, last_price_time))
            rows = cursor.fetchall()

        # 결과를 DataFrame으로 변환
        columns = ['stock_code', 'name', 'sector', 'market', 'current_price', 'stockcount', 'UpDownRate', 'price_time']
        df = pd.DataFrame(rows, columns=columns)

        # print(f"Data for 1 Day: {df.head()}")  # 1일 기간 데이터 확인

        # 변동률 계산: UpDownRate 값을 그대로 사용
        df['Change Rate (%)'] = pd.to_numeric(df['UpDownRate'], errors='coerce')

    else:
        # 1일 이외의 기간 쿼리: filtered_once_time과 조인하여 데이터를 가져옴
        query = '''
        WITH latest_closing_price AS (
            SELECT stock_code, name, MAX(date) AS latest_date
            FROM filtered_once_time
            WHERE date <= %s
            GROUP BY stock_code, name
        )
        SELECT rt.stock_code, rt.name, rt.sector, rt.market, rt.current_price, rt.stockcount, rt.UpDownRate, ot.closing_price, rt.price_time
        FROM real_time rt
        INNER JOIN latest_closing_price lcp
            ON rt.stock_code = lcp.stock_code AND rt.name = lcp.name
        INNER JOIN filtered_once_time ot
            ON lcp.stock_code = ot.stock_code AND lcp.name = ot.name AND lcp.latest_date = ot.date
        WHERE rt.market = %s AND rt.price_time = %s;
        '''
        with connection.cursor() as cursor:
            cursor.execute(query, (time_threshold, selected_market, last_price_time))
            rows = cursor.fetchall()

        # 결과를 DataFrame으로 변환
        columns = ['stock_code', 'name', 'sector', 'market', 'current_price', 'stockcount', 'UpDownRate', 'closing_price', 'price_time']
        df = pd.DataFrame(rows, columns=columns)

        # print(f"Data for period {selected_time_period}: {df.head()}")  # 선택한 기간 데이터 확인

        # 1일 이외의 기간에 대해 변동률 계산
        df['Change Rate (%)'] = (df['current_price'] - df['closing_price']) / df['closing_price'] * 100

    # 시가총액 계산
    df['market_cap'] = df['current_price'] * df['stockcount']
    # print(f"Market cap calculation: {df[['stock_code', 'market_cap']].head()}")  # 시가총액 계산 결과 확인
    
    # 'sector' 컬럼의 빈 값 및 null 값을 '기타'로 변경
    df['sector'] = df['sector'].replace(' ', '기타')  # 빈 문자열을 '기타'로 변경
    df['sector'] = df['sector'].replace('', '기타')  # 빈 문자열을 '기타'로 변경
    df['sector'] = df['sector'].fillna('기타')  # null 값을 '기타'로 변경

    # 코스닥 선택 시 시가총액 상위 500개 종목만 필터링
    if selected_market == 'KOSDAQ':
        df = df.nlargest(500, 'market_cap')
        # print(f"Top 500 stocks by market cap for KOSDAQ: {df.head()}")  # 코스닥 시가총액 상위 500개 종목 확인

    # 섹터별로 그룹화하여 시가총액 상위 10개 종목만 남기기
    df = df.groupby('sector').apply(lambda x: x.nlargest(10, 'market_cap')).reset_index(drop=True)

    # print(f"Top 10 stocks by market cap per sector: {df.head()}")  # 섹터별 시가총액 상위 10개 종목 확인

    return df

# 트리맵을 그리는 함수
def treemap_view(request):
    # 선택된 시장 및 기간 가져오기
    selected_market = request.GET.get('market', 'KOSPI200')
    selected_time_period = request.GET.get('period', '1 Day')

    # 데이터 로드
    df = load_stock_data(selected_market, selected_time_period)
    df['market_cap_억'] = df['market_cap'] / 1e8 # 시가총액 억단위로 보이게 설정중

    # Plotly 트리맵 생성
    fig = px.treemap(
        df,
        path=['sector', 'name'],  # 섹터와 이름 계층 구조
        values='market_cap_억',  # 시가총액을 크기로 설정
        color='Change Rate (%)',  # 변동률에 따라 색상 설정
        color_continuous_scale=['blue', '#FAFAFA', 'red'],  # 파랑-흰색-빨강
        color_continuous_midpoint=0,  # 0을 기준으로 색상을 나눔
        custom_data=['name', 'Change Rate (%)','market_cap_억'],  # 추가 데이터로 변동률을 제공
    )

    fig.add_annotation(
        x=0.99,  # X축 위치 (오른쪽)
        y=0.99,  # Y축 위치 (상단)
        text="(단위: 억 원)",  # 표시할 텍스트
        showarrow=False,  # 화살표 숨기기
        font=dict(size=15, color="black", family="NanumR"),  # 글씨 크기와 색상 설정
        xanchor="right",  # 오른쪽 정렬
        yanchor="top",  # 위쪽 정렬
    )
    fig.update_traces(
        textposition='middle center',
        # hovertemplate에서 %{customdata[0]} 부분을 제거하여 불필요한 항목을 숨김
        # hovertemplate='<b>%{label}</b><br>변동률: %{customdata[1]:.2f}%<br>시가총액: %{value:,.0f} 원<br>',
        hovertemplate='<b>%{label}</b><br>변동률: %{customdata[1]:.2f}%<br>시가총액: %{customdata[2]:,.0f}<br>',
        texttemplate='<b>%{label}<br>%{customdata[1]:.2f}%</b>',  # 트리맵 내에서도 변동률 표시
        marker=dict(line=dict(width=0.2, color='rgb(255, 255, 255)')), 
        textfont=dict(size=15, family="NanumR"),  # 글씨 크기
        hoverlabel=dict(
            font=dict(size=16, family="NanumR"),
        ),
    )
    
        # 레이아웃을 업데이트하여 그래프가 화면을 꽉 차게 설정
    fig.update_layout(
            coloraxis_colorbar=dict(
            title="변동률(%)",
            tickfont=dict(size=14, color='black', family="NanumR"),
            titlefont=dict(size=16, color='black', family="NanumR"),
            len=0.4, 
            thickness=20,
            yanchor="top",
            y=1,
        ),
        margin=dict(t=0, l=30, r=0, b=20),
        height=800,  
        width=1300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )



    # 그래프를 HTML로 변환
    graph_html = fig.to_html(full_html=False)

    # 템플릿에 그래프와 선택된 값 전달
    return render(request, 'main/map.html', {
        'graph_html': graph_html,
        'selected_market': selected_market,
        'selected_time_period': selected_time_period
    })


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
            defaults={'stock_code': latest_stock.stock_code, 'mbti': stock_mbti.mbti}
        )
        return redirect('mypage')
        # return JsonResponse({'status': 'added'})

    else:
        return redirect('mypage')
        # return JsonResponse({'status': 'error'})
    
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
    test_result1 = TestResult.objects.filter(user=request.user).order_by('-id').first()
    test_result2 = TestResult2.objects.filter(user=request.user).order_by('-id').first()

    context = {
        'mbti_stock': stock_infos_list,
        'mbti': mbti_value,
        'stock_info': stock_info_list,
        'test_result1': test_result1,
        'test_result2': test_result2,
        'my_list' : my_list,
    }

    return render(request, 'mypage/mypage.html', context)


from django.shortcuts import redirect, get_object_or_404
from .models import UserStock, DividendVolatility, Mbti, News

@login_required
def remove_stock(request, stock_code):
    user_stocks = UserStock.objects.filter(stock_code=stock_code, user=request.user)
    
    for user_stock in user_stocks:
        user_stock.delete()

    return redirect('mypage')
    # return JsonResponse({'status': 'removed'})


from stocks.models import OnceTime
import json

# stock_detail_page 브랜치에서 생성
# localhost:8000/stock으로 들어가면 해당 페이지 리턴
def stock_detail_page(request, stock_code="005930"):
    # 종목 코드를 이용해서 주식 정보를 DB에서 가져오는 코드(1일 외 기간)
    stock_data = OnceTime.objects.filter(stock_code=stock_code).order_by('date')
    
    #1일 차트에 사용할 RealTime 데이터 (1일 이외의 기간은 사용하지 않음)
    real_time_data = RealTime.objects.filter(stock_code=stock_code).order_by('price_time')

    dividend_data = get_object_or_404(DividendVolatility, stock_code=stock_code)
    
    # 주식 mbti 정보 가져오기
    stock_mbti = get_object_or_404(Mbti, stock_code=stock_code)

    # news 정보 가져오기
    news_list = News.objects.filter(stock_code=stock_code).order_by('-pubDate')[:3]
    
    # 날짜 및 종가 데이터를 JSON 형태로 변환
    dates = [str(x.date) for x in stock_data]
    closing_prices = [x.closing_price for x in stock_data]
    
    # RealTime 데이터에서 캔들차트용 데이터
    candle_data = [{
        'x': data.price_time.strftime('%Y-%m-%dT%H:%M:%SZ'),  # ISO 8601 형식으로 변환
        'o': data.opening_price,
        'h': data.high_price,
        'l': data.low_price,
        'c': data.current_price
    } for data in real_time_data]

    
    # 이동평균 데이터 가져오기
    ma5 = [x.MA5 for x in stock_data]
    ma20 = [x.MA20 for x in stock_data]
    ma60 = [x.MA60 for x in stock_data]
    ma120 = [x.MA120 for x in stock_data]
  
    
    # 사용자가 이 종목을 관심 목록에 추가했는지 확인하는 변수
    try:
        is_favorite = UserStock.objects.filter(user=request.user, stock_code=stock_code).exists()
    except:
        is_favorite = False
    favorite_icon = 'images/filled_star.png' if is_favorite else 'images/empty_star.png'

    # Real_time 종목 현재가

    latest_stock = RealTime.objects.filter(stock_code=stock_code).order_by('-id').first()
    stock_info ={
        'current_price': latest_stock.current_price,
        'UpDownRate': latest_stock.UpDownRate,
        'UpDownPoint': latest_stock.UpDownPoint,
        'id': latest_stock.id,
    }
    
    context = {
        'stock_code': stock_code,
        'dates': json.dumps(dates),  # JSON으로 직렬화
        'closing_prices': json.dumps(closing_prices),  # JSON으로 직렬화
        'ma5': json.dumps(ma5),  # MA20
        'ma20': json.dumps(ma20),  # MA20
        'ma60': json.dumps(ma60),  # MA60
        'ma120': json.dumps(ma120),  # MA120
        'candle_data': json.dumps(candle_data),  # RealTime 캔들 데이터
        'name': stock_data.first().name,
        'prev_dividend_rate': dividend_data.prev_dividend_rate ,
        'pred_dividend_rate': dividend_data.pred_dividend_rate ,
        'dividend_stability': dividend_data.dividend_stability, 
        'volatility': dividend_data.volatility,
        'year': dividend_data.year,
        'mbti': stock_mbti.mbti,
        'news_list': news_list,
        'is_favorite': is_favorite,
        'favorite_icon': favorite_icon,
        'stock_info': stock_info,
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
    

#민혁의 섹션
from django.db import connection

def get_top_sectors():
    query = '''
        WITH RankedData AS (
        SELECT rt1.sector, 
               rt1.name, 
               rt1.price_time, 
               rt1.UpDownRate,
               ROW_NUMBER() OVER (PARTITION BY rt1.sector ORDER BY rt1.price_time DESC, rt1.UpDownRate DESC) as row_num
        FROM real_time rt1
        WHERE rt1.sector IS NOT NULL
        AND rt1.sector != ''
        AND rt1.UpDownRate IS NOT NULL
    )
    , FilteredData AS (
        SELECT sector, UpDownRate
        FROM RankedData
        WHERE row_num <= 7
    )
    SELECT sector, AVG(UpDownRate) as avg_updownrate
    FROM FilteredData
    GROUP BY sector
    ORDER BY avg_updownrate DESC
    LIMIT 5;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    print(result)  # 상위 3개의 섹터를 출력하여 확인

    sector_avg_list = [
        {
            'sector': row[0],
            'avg_updownrate': row[1],
            'image': get_sector_image(row[0])  # 각 섹터에 맞는 이미지를 추가
        }
        for row in result
    ]

    return sector_avg_list




# 섹터에 맞는 이미지를 리턴하는 함수
def get_sector_image(sector_name):
    # 이미지 파일 이름과 섹터 이름을 매핑
    sector_image_map = {
        "의료정밀기기": "의료정밀.png",
        "기타서비스": "기타서비스.png",
        "화학": "화학.png",
        "건설업": "건설.png",
        "제약": "제약.png",
        "서비스업": "서비스.png",
        "일반전기전자": "일반전기전자.png",
        "건설": "건설.png",
        "증권": "증권.png",
        "금융업": "금융.png",
        "리츠": "리츠.png",
        "오락문화": "오락문화.png",
        "운수.장비": "운수장비.png",
        "유통": "유통.png",
        "음식.담배": "음식.png",
        "음식료품": "음식.png",
        "금속": "금속.png",
        "기계": "기계.png",
        "기계.장비": "기계장비.png",
        "전기.전자": "전기전자.png",
        "운수.창고": "운송.png",
        "의약품": "의약품.png",
        "섬유.의복": "섬유의복.png",
        "금융": "금융2.png",
        "운송장비부품": "운송장비부품.png",
        "전기.가스업": "전기가스업.png",
        "철강.금속": "철강금속.png",
        "종이.목재": "종이목재.png",
        "비금속": "비금속.png",
        "의료정밀": "의료정밀2.png",
        "통신업": "통신.png",
        "보험": "보험.png",
        "외국증권": "외국증권.png",
        "섬유.의류": "섬유의류.png",
        "비금속광물": "비금속광물.png",
        "운송": "운송-1.png",
        "인프라투용": "인프라.png",
        "출판.매체": "출판매체.png",
        "인프라투용": "인프라.png",
    }

    # 매핑되지 않은 섹터는 기본 이미지를 반환
    return sector_image_map.get(sector_name, "default_icon.png")

from django.http import JsonResponse

# 특정 섹터에 대한 최근 10개의 데이터를 반환하는 함수
def get_sector_details(request, sector_name):
    # 주어진 섹터에 대한 고유한 name과 데이터를 가져옴
    sector_data = list(
        RealTime.objects.filter(sector=sector_name)
        .order_by('-price_time','-UpDownRate')[:7]
        .values('name', 'current_price', 'UpDownRate')
    )

    return JsonResponse(sector_data, safe=False)

from django.core.cache import cache

def stock_autocomplete(request):
    query = request.GET.get('stock_query', '')
    cache_key = f'stock_autocomplete_{query}'
    stocks = cache.get(cache_key)
    if not stocks:
        stocks = list(RealTime.objects.filter(Q(stock_code__icontains=query) | Q(name__icontains=query))\
                      .values('name', 'stock_code').distinct())[:5]
        # Python에서 추가로 중복 제거 (name과 stock_code로만 중복 제거)
        unique_stocks = []
        seen = set()
        
        for stock in stocks:
            # 튜플 (name, stock_code) 로 중복 여부 확인
            stock_tuple = (stock['name'], stock['stock_code'])
            if stock_tuple not in seen:
                seen.add(stock_tuple)
                unique_stocks.append(stock)
        # 캐시에 저장
        cache.set(cache_key, unique_stocks, 60 * 60 * 12)  # 12시간 캐싱
        stocks = unique_stocks
    return JsonResponse(stocks, safe=False) 
