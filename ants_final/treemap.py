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
    
    # 변동률 계산
    df['Change Rate (%)'] = (df['current_price'] - df['closing_price']) / df['closing_price'] * 100
    
    # 시가총액 계산 (current_price * stockcount)
    df['total'] = df['current_price'] * df['stockcount']

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
            st.session_state.selected_market = 'KOSPI200'
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

    # 선택된 기간에 따라 데이터 필터링
    filtered_df = filter_by_time_period(filtered_df, selected_time_period)

    # 1일일 경우 'UpDownRate'를 사용하고, 그 외에는 'Change Rate (%)' 사용
    if selected_time_period == '1 Day':
        filtered_df['color_value'] = filtered_df['UpDownRate']
    else:
        filtered_df['color_value'] = filtered_df['Change Rate (%)']


    st.write("color_value 확인", filtered_df['color_value'])
    
    # 시가총액의 범위를 고려하여 적절한 글씨 크기 조정 (스케일링 적용)
    max_total = filtered_df['total'].max()

    # 글씨 크기 조정을 위해 상한과 하한 설정
    def adjust_font_size(total_value, max_total, min_size=10, max_size=25):
        # 시가총액에 비례한 글씨 크기 조정, 최소 10, 최대 25
        size = (total_value / max_total) * (max_size - min_size) + min_size
        return max(min_size, min(size, max_size))  # min_size와 max_size 사이로 제한

    # 트리맵 생성
    if not filtered_df.empty:
        fig = px.treemap(
            filtered_df,
            path=['sector', 'name'],
            values='total',  # 시가총액에 따른 박스 크기
            color='color_value',  # UpDownRate 또는 Change Rate(%)를 색상 값으로 사용
            color_continuous_scale='RdBu',
            title=f"{selected_market} - {selected_time_period} Stock Treemap"
        )

        # 글씨 크기를 시가총액에 따라 조정하고, 상한과 하한 적용
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>변동률: %{color_value:.2f}%',
            texttemplate='%{label}<br>%{color_value:.2f}%',
            # textfont=dict(size=filtered_df['total'].apply(lambda x: adjust_font_size(x, max_total))),
            # insidetextfont=dict(size=filtered_df['total'].apply(lambda x: adjust_font_size(x, max_total)))
        )

        fig.update_layout(
            uniformtext=dict(minsize=10, mode='hide'),
            autosize=False,
            height=800,
            width=800,
            margin=dict(t=50, l=25, r=25, b=25)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("데이터가 없습니다.")



#     if not filtered_df.empty:
        
#         #데이터 잘 들어오는지 확인
#         # st.write("변동률 (Change Rate %):")
#         # st.dataframe(filtered_df[['name', 'UpDownRate', 'Change Rate (%)']])
#         st.dataframe(filtered_df.sort_values(by='total', ascending=False))
#         st.write("UpDownRate 값 확인:")
#         st.dataframe(filtered_df[['name', 'UpDownRate']].sort_values(by='UpDownRate'))

#       # 트리맵 그리기
#         if selected_time_period == '1 Day':
#             fig = px.treemap(
#                 filtered_df,
#                 path=['sector', 'name'],
#                 values='total',
#                 color='UpDownRate',
#                 color_continuous_scale='RdBu',
#                 title=f"Treemap of {selected_market} Market - 1 Day Change"
#             )
#         else:
#             fig = px.treemap(
#                 filtered_df,
#                 path=['sector', 'name'],
#                 values='total',
#                 color='Change Rate (%)',
#                 color_continuous_scale='RdBu',
#                 title=f"Treemap of {selected_market} Market - {selected_time_period} Change"
#             )

#         # hovertemplate을 명확하게 설정
#         fig.update_traces(
#             # hovertemplate=(
#             #     '<b>%{label}</b><br>' +
#             #     '시가총액: %{value}<br>' +   # 시가총액 표시
#             #     '변동률: %{color:.2f}%'      # 변동률 정확히 표시
#             # ),
#             textinfo='label+percent entry',  # 이름과 변동률만 표시
#             textfont=dict(size=14),
#             insidetextfont=dict(size=25)  # 내부 텍스트 크기
#         )

#         # uniformtext로 최소 텍스트 크기 지정
#         fig.update_layout(
#             uniformtext=dict(minsize=10, mode='hide'),  # 텍스트가 너무 작지 않게 설정
#             autosize=False,
#             height=800,
#             width=800,
#             margin=dict(t=50, l=25, r=25, b=25)
#         )

#         # Plotly 차트를 Streamlit에 표시
#         st.plotly_chart(fig, use_container_width=True, height=1000)


        
             
        
        
        
        
#     else:
#         st.write(f"No data available for {selected_market} Market.")
# else:
#     st.write("Please select a market.")

# # 삼성전자 데이터를 필터링하고 출력
# samsung_data = df[df['name'].str.contains("삼성전자", case=False)]

# if not samsung_data.empty:
#     st.subheader("삼성전자 데이터")
#     st.dataframe(samsung_data)
# else:
#     st.write("삼성전자 데이터가 없습니다.")