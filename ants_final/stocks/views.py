import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from django.http import HttpResponse
from .models import OnceTime
from datetime import datetime

def stock_chart(request):
    # `once_time` 테이블에서 데이터 가져오기
    data = OnceTime.objects.all().order_by('date')
    
    dates = [entry.date for entry in data]
    ma5 = [entry.MA5 for entry in data]
    ma20 = [entry.MA20 for entry in data]
    ma60 = [entry.MA60 for entry in data]
    ma120 = [entry.MA120 for entry in data]
    
    # 차트 생성
    fig, ax = plt.subplots()
    
    ax.plot(dates, ma5, label='MA5', color='blue', linewidth=1.5)
    ax.plot(dates, ma20, label='MA20', color='orange', linewidth=1.5)
    ax.plot(dates, ma60, label='MA60', color='green', linewidth=1.5)
    ax.plot(dates, ma120, label='MA120', color='red', linewidth=1.5)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Moving Averages')
    ax.legend()
    
    # 이미지 버퍼에 차트 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    return HttpResponse(buffer, content_type='image/png')


