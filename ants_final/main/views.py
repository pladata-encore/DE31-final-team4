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
from django.shortcuts import render
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
from stocks.models import Market  # stocks 앱에서 Market 모델을 임포트
from datetime import datetime

# 그래프를 생성하고 base64로 인코딩하는 함수
def add_graphs():
    # 오늘 날짜의 시작 시간과 끝 시간 설정
    today_start = datetime.combine(timezone.now().date(), datetime.min.time())
    today_end = datetime.combine(timezone.now().date(), datetime.max.time())

    # KOSPI 및 KOSDAQ 데이터 중 오늘 날짜의 데이터만 가져옴
    kospi_data = Market.objects.filter(stock_name="KOSPI", price_time__range=[today_start, today_end])
    kosdaq_data = Market.objects.filter(stock_name="KOSDAQ", price_time__range=[today_start, today_end])

    # KOSPI 그래프 생성 (X축, Y축 제거)
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(kospi_data.values_list('price_time', flat=True), kospi_data.values_list('current_point', flat=True), label="KOSPI", color="blue")
    ax1.set_title("KOSPI (Today)")
    ax1.xaxis.set_visible(False)  # X축 숨김
    ax1.yaxis.set_visible(False)  # Y축 숨김
    ax1.legend()

    # KOSDAQ 그래프 생성 (X축, Y축 제거)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(kosdaq_data.values_list('price_time', flat=True), kosdaq_data.values_list('current_point', flat=True), label="KOSDAQ", color="green")
    ax2.set_title("KOSDAQ (Today)")
    ax2.xaxis.set_visible(False)  # X축 숨김
    ax2.yaxis.set_visible(False)  # Y축 숨김
    ax2.legend()

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

    # 그래프 데이터를 템플릿으로 전달
    return render(request, 'main/home.html', {'graphic1': graphic1, 'graphic2': graphic2})
