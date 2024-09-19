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
        SELECT rt.*, ot.closing_price
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
    columns = ['stock_code', 'name', 'sector', 'market', 'status_code', 'current_price', 'UpDownPoint',
               'PlusMinus', 'UpDownRate', 'opening_price', 'high_price', 'low_price', 'price_time', 'per',
               'pbr', 'stockcount', 'id',  'closing_price']

    df = pd.DataFrame(rows, columns=columns)
    
    # #sector 빈값일때
    # df['sector'].fillna('Unknown', inplace=True)

    # 변동률 계산
    df['Change Rate (%)'] = (df['current_price'] - df['closing_price']) / df['closing_price'] * 100
    
    # 시가총액 계산 (current_price * stockcount)
    df['total'] = df['current_price'] * df['stockcount']
    
    df['UpDownRate'] = pd.to_numeric(df['UpDownRate'], errors='coerce')  # 숫자로 변환
    df['UpDownRate'] = df['UpDownRate'] * 100  # % 단위로 변환
    df['sector'] = df['sector'].fillna('기타')


    return df

# Streamlit을 사용하여 데이터 표시 및 트리맵 그리기
st.title("Stock Market Treemap")

# 데이터 불러오기
df = load_stock_data()

# Streamlit 세션 상태로 마켓 선택 상태 유지
if 'selected_market' not in st.session_state:
    st.session_state.selected_market = None

# 가로로 배치하는 layout 설정
col1, col2 = st.columns([1, 1])

# 마켓 선택과 기간 선택을 가로로 배치
with col1:
    st.subheader("Select a Market")
    # 마켓 선택 드롭다운 추가
    selected_market = st.selectbox(
        "Market", 
        options=['KOSPI200', 'KOSDAQ'],
        index=0  # 기본적으로 첫 번째 옵션 선택
    )
    st.session_state.selected_market = selected_market

with col2:
    st.subheader("Select a Time Period")
    # 기간 선택 드롭다운 추가
    time_options = ['1 Day', '1 Week', '1 Month', '3 Months', '6 Months', '1 year']
    selected_time_period = st.selectbox("Time Period", options=time_options)

# 필터링 함수에서 주말(토, 일)을 제외하는 기능 추가
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

    # 주말 제외 (토요일과 일요일 제거)
    filtered_df = df[(df['price_time'] >= time_threshold) & (df['price_time'].dt.weekday < 5)]

    return filtered_df

# 선택된 기간에 따라 데이터 필터링
filtered_df = df[df['market'] == st.session_state.selected_market]
filtered_df = filter_by_time_period(filtered_df, selected_time_period)

# 1일일 경우 'UpDownRate'를 사용하고, 그 외에는 'Change Rate (%)' 사용
if selected_time_period == '1 Day':
    filtered_df['color_value'] = filtered_df['UpDownRate']
else:
    filtered_df['color_value'] = filtered_df['Change Rate (%)']

# 시가총액의 범위를 고려하여 적절한 글씨 크기 조정 (스케일링 적용)
max_total = filtered_df['total'].max()

# 글씨 크기 조정을 위해 상한과 하한 설정
def adjust_font_size(total_value, max_total, min_size=10, max_size=25):
    size = (total_value / max_total) * (max_size - min_size) + min_size
    return max(min_size, min(size, max_size))

# 트리맵 생성
if not filtered_df.empty:
    fig = px.treemap(
        filtered_df,
        path=['sector', 'name'],
        values='total',
        color='color_value',
        color_continuous_scale='RdBu',
        title=f"{st.session_state.selected_market} - {selected_time_period} Stock Treemap"
    )

    fig.update_layout(
        uniformtext=dict(minsize=12, mode='show'),
        autosize=False,
        height=800,
        width=800,
        margin=dict(t=50, l=25, r=25, b=25)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("데이터가 없습니다.")
