import os
import django
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Django 설정 불러오기
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ants_final.settings")  # 프로젝트 이름을 'ants_final'로 설정
django.setup()

from stocks.models import OnceTime, Market  # Market 모델이 추가되었을 경우

# Streamlit 대시보드 설정
st.title("Stock Price and Market Data Dashboard - Separated Graphs")

# 사용자 입력: 주식 티커(symbol)와 기간 선택 (OnceTime 데이터)
st.sidebar.header("OnceTime Data Input")
ticker_symbol = st.sidebar.text_input("Ticker Symbol (OnceTime)", "000020")  # 기본값
start_date = st.sidebar.date_input("Start Date (OnceTime)", pd.to_datetime("2014-01-01"))
end_date = st.sidebar.date_input("End Date (OnceTime)", datetime.today())

# # 사용자 입력: 주식 이름과 기간 선택 (Market 데이터)
# st.sidebar.header("Market Data Input")

# # 고정된 KOSPI와 KOSDAQ만 선택 가능하게 설정
# StockName = st.sidebar.selectbox("Select StockName (Market)", ["KOSPI", "KOSDAQ"])

# # 사이드바에서 날짜 입력
# yesterday = datetime.today() - timedelta(days=1)
# start_date_market = st.sidebar.date_input("Market Start Date", yesterday)
# end_date_market = st.sidebar.date_input("Market End Date", datetime.today())  # 오늘 날짜로 기본값 설정

# OnceTime 데이터를 불러오는 함수
def load_oncetime_data(ticker, start, end):
    data = OnceTime.objects.filter(
        stock_code=ticker,
        date__range=[start, end]
    ).values('date', 'closing_price', 'hts_total', 'prev_trading', 'MA5', 'MA20', 'MA60', 'MA120')
    return pd.DataFrame(list(data))

# # Market 데이터를 불러오는 함수
# def load_market_data(StockName, start, end):
#     data = Market.objects.filter(
#         StockName=StockName,
#         price_time__range=[start, end]
#     ).values('price_time', 'CurrentPoint', 'UpDownPoint', 'UpDownRate')
#     return pd.DataFrame(list(data))

# OnceTime 데이터 로드
oncetime_data = load_oncetime_data(ticker_symbol, start_date, end_date)

# Market 데이터 로드
# market_data = load_market_data(StockName, start_date_market, end_date_market)

# OnceTime 데이터 그래프: Closing Price (반응형 Plotly 그래프 사용)
st.subheader(f"{ticker_symbol} Closing Price (OnceTime Data)")
if not oncetime_data.empty:
    # Plotly를 사용한 반응형 선 그래프
    fig = px.line(oncetime_data, x='date', y='closing_price', title=f'{ticker_symbol} Closing Price')
    # closing_price 선을 진하게, 검은색으로 설정
    fig.update_traces(line=dict(color='black', width=1))  # 선의 색상과 두께 조정

    # 이동 평균(MA) 추가
    fig.add_scatter(x=oncetime_data['date'], y=oncetime_data['MA5'], mode='lines', name='MA5', line=dict(dash='dash', color='blue'))
    fig.add_scatter(x=oncetime_data['date'], y=oncetime_data['MA20'], mode='lines', name='MA20', line=dict(dash='dash', color='orange'))
    fig.add_scatter(x=oncetime_data['date'], y=oncetime_data['MA60'], mode='lines', name='MA60', line=dict(dash='dash', color='green'))
    fig.add_scatter(x=oncetime_data['date'], y=oncetime_data['MA120'], mode='lines', name='MA120', line=dict(dash='dash', color='red'))

    # Plotly 차트를 Streamlit에 표시
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No data available for the selected period.")

# OnceTime 데이터 그래프: Trading Volume (반응형 Plotly 막대 그래프)
st.subheader(f"{ticker_symbol} Trading Volume (OnceTime Data)")
if not oncetime_data.empty:
    # Plotly를 사용한 반응형 막대 그래프
    fig2 = px.bar(oncetime_data, x='date', y='prev_trading', title=f'{ticker_symbol} Trading Volume', labels={'prev_trading': 'Trading Volume'})

    # Plotly 차트를 Streamlit에 표시
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.error("No data available for the selected period.")


# # Market 데이터 그래프 (여전히 Matplotlib 사용)
# st.subheader(f"{StockName} Current Point (Market Data)")
# if not market_data.empty:
#     fig3, ax3 = plt.subplots(figsize=(12, 6))
#     ax3.plot(market_data['price_time'], market_data['CurrentPoint'], label=f'{StockName} Current Point', color='blue')
#     ax3.set_xlabel("Time")
#     ax3.set_ylabel("Current Point")
#     ax3.legend()
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     st.pyplot(fig3)
# else:
#     st.error("No data found for the selected period.")
