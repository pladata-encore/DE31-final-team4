import os
import django
import streamlit as st
import pandas as pd
from django.db.models import OuterRef, Subquery, F
from django.db.models.functions import TruncDate

# Django 설정 불러오기
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ants_final.settings")
django.setup()

from stocks.models import OnceTime,RealTime


# 주식 데이터를 불러오는 함수 정의
@st.cache_data
def load_stock_data():
    # RealTime의 price_time에서 날짜만 추출 (TruncDate 사용)
    once_time_subquery = OnceTime.objects.filter(
        stock_code=OuterRef('stock_code'),
        name=OuterRef('name'),
        date=TruncDate(F('price_time'))  # RealTime의 날짜와 OnceTime의 date 필드 비교
    ).values('hts_total', 'closing_price')[:1]  # 시가총액과 종가 가져오기

    # RealTime과 OnceTime을 종목코드와 날짜를 기준으로 연결
    queryset = RealTime.objects.annotate(
        hts_total=Subquery(once_time_subquery.values('hts_total')),
        closing_price=Subquery(once_time_subquery.values('closing_price'))
    )

    # 데이터를 리스트로 변환하여 Pandas DataFrame으로 반환
    data = []
    for stock in queryset:
        data.append({
            'Market': stock.market,
            'Name': stock.name,
            'Sector': stock.sector,
            'Current Price': stock.current_price,
            'UpDownRate': stock.UpDownRate,
            'Hts Total': stock.hts_total,        # OnceTime에서 가져온 시가총액
            'Closing Price': stock.closing_price, # OnceTime에서 가져온 종가
            'Price Time': stock.price_time
        })

#Streamlit을 사용하여 데이터 표시 및 트리맵 그리기
st.title("Stock Market Treemap")

df=load_stock_data()

# 사용자에게 Market 필터링 옵션 제공
market_options = ['KOSPI', 'KOSDAQ'] 
selected_market = st.selectbox("Select a Market", options=market_options)


# 선택된 마켓에 따라 데이터 필터링
filtered_df = df[df['Market'] == selected_market]