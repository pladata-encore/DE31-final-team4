import os
import django
import streamlit as st
import pandas as pd
from datetime import timedelta, datetime
import plotly.express as px

# Streamlit 페이지 설정
st.set_page_config(layout="wide")  # 페이지를 전체 너비로 설정

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

# Streamlit 세션 상태로 마켓 선택 상태 유지
if 'selected_market' not in st.session_state:
    st.session_state.selected_market = None

# 가로로 배치하는 layout 설정
col0, col1, col2, col3 = st.columns([2, 2, 2, 2])

# 마켓 선택과 기간 선택을 가로로 배치
with col1:
    st.subheader("Select a Market")
    
    col_market1, col_market2 = st.columns([1, 1])
    
    with col_market1:
        if st.button("KOSPI"):
            st.session_state.selected_market = 'KOSPI'
    with col_market2:
        if st.button("KOSDAQ"):
            st.session_state.selected_market = 'KOSDAQ'

with col2:
    st.subheader("Select a Time Period")
    time_options = ['1 Day', '1 Week', '1 Month', '3 Months', '6 Months', '1 year']
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
    elif period == '6 Months':
        time_threshold = current_time - timedelta(days=180)
    elif period == '1 year':
        time_threshold = current_time - timedelta(days=365)
    
    return df[df['price_time'] >= time_threshold]

# 마켓이 선택된 경우에만 필터링 수행
selected_market = st.session_state.selected_market

if selected_market:
    filtered_df = df[df['market'] == selected_market]

    # 시가총액 기준으로 내림차순 정렬하여 상위 100개 데이터만 선택
    filtered_df = filtered_df.sort_values(by='hts_total', ascending=False).head(100)

    # 선택된 기간에 따라 데이터 필터링
    filtered_df = filter_by_time_period(filtered_df, selected_time_period)

    if not filtered_df.empty:
        st.write("변동률 (Change Rate %):")
        st.dataframe(filtered_df[['name', 'UpDownPoint', 'Change Rate (%)']])

        # 트리맵 그리기
        if selected_time_period == '1 Day':
            fig = px.treemap(
                filtered_df,
                path=['sector', 'name'],
                values='hts_total',
                color='UpDownPoint',
                color_continuous_scale='RdBu',
                title=f"Treemap of {selected_market} Market - 1 Day Change"
            )
        else:
            fig = px.treemap(
                filtered_df,
                path=['sector', 'name'],
                values='hts_total',
                color='Change Rate (%)',
                color_continuous_scale='RdBu',
                title=f"Treemap of {selected_market} Market - {selected_time_period} Change"
            )

        fig.update_traces(
            textinfo='label+value+percent entry',
            textfont=dict(size=14),
            hoverinfo='label+value+percent parent',
            insidetextfont=dict(size=14)
        )

        fig.update_layout(
            autosize=False,
            height=800,
            width=800,
            margin=dict(t=50, l=25, r=25, b=25)
        )
        
        st.plotly_chart(fig, use_container_width=True, height=1000)
    else:
        st.write(f"No data available for {selected_market} Market.")
else:
    st.write("Please select a market.")
