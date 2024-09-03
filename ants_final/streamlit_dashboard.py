import os
import django
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
# Django 설정 불러오기
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ants_final.settings")
django.setup()

from stocks.models import OnceTime

# Streamlit 대시보드 설정
st.title("Stock Price Dashboard - Django Integrated")

# 사용자 입력: 주식 티커(symbol)와 기간 선택
st.sidebar.header("User Input")
ticker_symbol = st.sidebar.text_input("Ticker Symbol", "000020")  # 기본값을 동화약품으로 설정
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2014-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime(f"{datetime.today().strftime('%Y-%m-%d')}"))

# Django ORM을 사용해 데이터 가져오기
def load_data(ticker, start, end):
    data = OnceTime.objects.filter(
        stock_code=ticker,
        date__range=[start, end]
    ).values('date', 'closing_price', 'hts_total', 'prev_trading', 'MA5', 'MA20', 'MA60', 'MA120')
    return pd.DataFrame(list(data))

data = load_data(ticker_symbol, start_date, end_date)

# 데이터 확인
st.write(data)

# 주식 데이터 표시
st.subheader(f"{ticker_symbol} Closing Price")

# 차트 그리기
if 'date' in data.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['date'], data['closing_price'], label='Close Price', color='black')
    ax.plot(data['date'], data['MA5'], label='MA5', color='blue', linestyle='--')
    ax.plot(data['date'], data['MA20'], label='MA20', color='orange', linestyle='--')
    ax.plot(data['date'], data['MA60'], label='MA60', color='green', linestyle='--')
    ax.plot(data['date'], data['MA120'], label='MA120', color='red', linestyle='--')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)
else:
    st.error("The 'date' column is missing from the data.")
