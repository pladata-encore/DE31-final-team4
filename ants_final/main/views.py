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


# 관심종목
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RealTimeStock, UserStock
from datetime import date

@login_required
def add_favorite_list(request, stock_code):
    # stock = get_object_or_404(RealTimeStock, stock_code=stock_code)
    latest_stock = RealTimeStock.objects.filter(stock_code=stock_code).order_by('-id').first()
    UserStock.objects.get_or_create(user=request.user, stock=latest_stock)
    return redirect('my_favorite_list')


# real_time table 정보 가져오기
@login_required
def my_favorite_list(request):
    user_stocks = UserStock.objects.filter(user=request.user)
    stock_info = []

    for user_stock in user_stocks:
        # 실시간 정보를 가져오기
        real_time_stock = get_object_or_404(RealTimeStock, stock_code=user_stock.stock.stock_code)
        stock_info.append({
            'stock_code': real_time_stock.stock_code,
            'name': real_time_stock.name,
            'current_price': real_time_stock.current_price,
            'UpDownRate': real_time_stock.UpDownRate,
            'UpDownPoint': real_time_stock.UpDownPoint,
            "id":real_time_stock.id,
        })

    return render(request, 'mypage/mypage.html', {'stock_info': stock_info})

