from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

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

# @login_required
# def post_login_redirect(request):
#     """
#     사용자가 로그인한 후 소셜 로그인인지 일반 로그인인지 확인하고 리다이렉션.
#     """
#     if request.user.socialaccount_set.exists():
#         # 사용자가 소셜 로그인을 했다면
#         return redirect('/accounts/google/login/')
#     else:
#         # 일반 로그인이라면
#         return redirect('/accounts/login/')


# def test_option_1(request):
#     return render(request, 'main/test_option_1.html')

# def test_option_2(request):
#     return render(request, 'main/test_option_2.html')

# def test_option_3(request):
#     return render(request, 'main/test_option_3.html')


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

#트리맵
from django.shortcuts import render
from stocks.models import OnceTime, RealTime  # 사용 중인 모델을 임포트
import plotly.express as px  # Plotly 사용
from django.db import connection
import pandas as pd
from datetime import datetime, timedelta

# 데이터 로드 함수
def load_stock_data(selected_market, selected_time_period):
    # 가장 최근의 real_time 데이터의 마지막 업데이트 시간 가져오기
    with connection.cursor() as cursor:
        cursor.execute('SELECT MAX(price_time) FROM real_time')
        last_price_time = cursor.fetchone()[0]

    # 현재 시간 대신 가장 최근 업데이트된 시간 사용
    time_threshold = last_price_time

    # SQL 쿼리 작성: 선택한 시장과 기간에 맞게 종가 데이터를 가져옴
    query = '''
    WITH latest_closing_price AS (
        SELECT stock_code, name, MAX(date) AS latest_date
        FROM once_time
        WHERE date <= %s
        GROUP BY stock_code, name
    )
    SELECT rt.stock_code, rt.name, rt.sector, rt.market, rt.current_price, rt.stockcount, rt.UpDownRate, ot.closing_price, rt.price_time
    FROM real_time rt
    INNER JOIN latest_closing_price lcp
        ON rt.stock_code = lcp.stock_code AND rt.name = lcp.name
    INNER JOIN once_time ot
        ON lcp.stock_code = ot.stock_code AND lcp.name = ot.name AND lcp.latest_date = ot.date
    WHERE rt.market = %s AND rt.price_time = %s;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query, (time_threshold, selected_market, last_price_time))
        rows = cursor.fetchall()

    # 결과를 DataFrame으로 변환
    columns = ['stock_code', 'name', 'sector', 'market', 'current_price', 'stockcount', 'UpDownRate', 'closing_price', 'price_time']
    df = pd.DataFrame(rows, columns=columns)

    # 1일 선택 시 UpDownRate 값 사용
    if selected_time_period == '1 Day':
        df['Change Rate (%)'] = pd.to_numeric(df['UpDownRate'], errors='coerce')
        # df['Change Rate (%)'] = df['UpDownRate'] * 100
    else:
        # 1일 이외의 기간에 대해 변동률 계산
        df['Change Rate (%)'] = (df['current_price'] - df['closing_price']) / df['closing_price'] * 100

    # 시가총액 계산
    df['market_cap'] = df['current_price'] * df['stockcount']

    # 섹터별로 그룹화하여 시가총액 상위 10개 종목만 남기기
    df = df.groupby('sector').apply(lambda x: x.nlargest(10, 'market_cap')).reset_index(drop=True)

    return df

# 트리맵을 그리는 함수
def treemap_view(request):
    selected_market = request.GET.get('market', 'KOSPI200')
    selected_time_period = request.GET.get('period', '1 Day')

    # 데이터 로드
    df = load_stock_data(selected_market, selected_time_period)

    # 회사 이름과 변동률을 함께 표시
    df['label'] = df['name'] + '<br>' + df['Change Rate (%)'].round(2).astype(str) + '%'

    # 트리맵 생성
    fig = px.treemap(df,
                     path=['sector', 'label'],  # label에 회사명과 변동률 포함
                     values='market_cap',  # 시가총액 기준으로 상자 크기 설정
                     color='Change Rate (%)',  # 색상은 변동률에 따라 설정
                     color_continuous_scale=['blue', 'black', 'red'],
                     title=f"{selected_market} 주식 시장 트리맵")

    # 섹터명에 대해서는 작은 텍스트, 종목명에 대해서는 큰 텍스트를 설정
    fig.update_traces(
        hovertemplate=None,
        textposition='middle center',
        # 각 아이템에 대해 글씨 크기 지정
        texttemplate=[
            '<span style="font-size:12px">%{label}</span>' if d['level'] == 1 else '<span style="font-size:20px">%{label}</span>'
            for d in fig.data[0]['ids']
        ],
        insidetextfont=dict(color='white'),
    )

    # HTML로 변환
    graph_html = fig.to_html(full_html=False)

    return render(request, 'main/map.html', {'graph_html': graph_html, 'selected_market': selected_market, 'selected_time_period': selected_time_period})

#streamlit용 view였음..
# import subprocess
# import os
# from django.http import HttpResponseRedirect

# # Django의 views.py에서 Streamlit 실행
# def treemap_view(request):
#     # Streamlit이 이미 실행 중인지 확인하는 방법은 생략하고,
#     # 매번 요청이 들어올 때 Streamlit을 실행하도록 처리.
#     try:
#         # Streamlit이 이미 실행 중인지 체크하고, 실행 중이 아니라면 실행
#         result = subprocess.run(['lsof', '-i', ':8501'], stdout=subprocess.PIPE)
#         if 'Streamlit' not in str(result.stdout):
#             # Streamlit이 실행 중이지 않다면, 백그라운드에서 Streamlit을 실행
#             subprocess.Popen(['streamlit', 'run', 'your_app.py', '--server.port', '8501'], 
#                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     except Exception as e:
#         print(f"Error launching Streamlit: {e}")

#     # Streamlit 앱으로 리디렉션
#     return HttpResponseRedirect('http://localhost:8501')
