import os
import django
import streamlit as st
import pandas as pd
from datetime import timedelta, datetime
import plotly.express as px

# Django 설정 불러오기
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ants_final.settings")
django.setup()

from django.db import connection
from stocks.models import RealTime

# 주식 데이터를 불러오는 함수 정의
@st.cache_data
def load_stock_data():
    query = '''
        SELECT rt.*, ot.hts_total, ot.closing_price
        FROM real_time rt
        LEFT JOIN once_time ot
        ON rt.stock_code = ot.stock_code
        AND DATE(rt.price_time) = ot.date
    '''
    # Raw SQL을 실행하여 데이터를 Pandas DataFrame으로 변환
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # 컬럼 이름을 지정하여 DataFrame 생성
    columns = ['stock_code', 'name', 'sector', 'market', 'status_code', 'current_price', 'UpDownRate',
               'PlusMinus', 'UpDownPoint', 'opening_price', 'high_price', 'low_price', 'price_time', 'per',
               'pbr', 'stockcount', 'id', 'hts_total', 'closing_price']

    df = pd.DataFrame(rows, columns=columns)
    
    # 변동률 계산
    df['Change Rate (%)'] = (df['current_price'] - df['closing_price']) / df['closing_price'] * 100

    return df

# Streamlit을 사용하여 데이터 표시 및 트리맵 그리기
st.title("Stock Market Treemap")

# 데이터 불러오기
df = load_stock_data()

# 좌측에 마켓 선택 버튼, 우측에 기간 필터링을 배치하는 레이아웃
col1, col2 = st.columns([2, 1])

# 좌측 (col1) - KOSPI/KOSDAQ 선택 버튼
with col1:
    st.subheader("Select a Market")
    selected_market = None
    if st.button("KOSPI"):
        selected_market = 'KOSPI'
    elif st.button("KOSDAQ"):
        selected_market = 'KOSDAQ'

# 우측 (col2) - 기간 필터링 선택
with col2:
    st.subheader("Select a Time Period")
    time_options = ['1 Day', '1 Week', '1 Month', '3 Months']
    selected_time_period = st.selectbox("Time Period", options=time_options)

# 데이터 필터링 함수
def filter_by_time_period(df, period):
    current_time = datetime.now()
    
    if period == '1 Day':
        time_threshold = current_time - timedelta(days=1)
    elif period == '1 Week':
        time_threshold = current_time - timedelta(weeks=1)
    elif period == '1 Month':
        time_threshold = current_time - timedelta(days=30)
    elif period == '3 Months':
        time_threshold = current_time - timedelta(days=90)
    
    return df[df['price_time'] >= time_threshold]

# 마켓이 선택된 경우에만 필터링 수행
if selected_market:
    # 선택된 마켓에 따라 데이터 필터링
    filtered_df = df[df['market'] == selected_market]

    # 선택된 기간에 따라 데이터 필터링
    filtered_df = filter_by_time_period(filtered_df, selected_time_period)

    # 트리맵 그리기
    if not filtered_df.empty:
        if selected_time_period == '1 Day':
            # 1일 기준 트리맵 (UpDownPoint 사용)
            fig = px.treemap(
                filtered_df,
                path=['sector', 'name'],               # 트리맵에서 섹터와 이름을 경로로 설정
                values='hts_total',                    # 시가총액을 크기로 설정
                color='UpDownPoint',                    # 1일 변동률(UpDownPoint)을 색상으로 설정
                color_continuous_scale='RdBu',         # 변동률에 따른 색상 스케일 (빨간색-파란색)
                title=f"Treemap of {selected_market} Market - 1 Day Change"
            )
        else:
            # 1주, 1달, 3달 트리맵 (Change Rate 사용)
            fig = px.treemap(
                filtered_df,
                path=['sector', 'name'],               # 트리맵에서 섹터와 이름을 경로로 설정
                values='hts_total',                    # 시가총액을 크기로 설정
                color='Change Rate (%)',               # 변동률(Change Rate)을 색상으로 설정
                color_continuous_scale='RdBu',         # 변동률에 따른 색상 스케일 (빨간색-파란색)
                title=f"Treemap of {selected_market} Market - {selected_time_period} Change"
            )

        st.plotly_chart(fig,use_container_width=True, height=800)
    else:
        st.write(f"No data available for {selected_market} Market.")
else:
    st.write("Please select a market.")
