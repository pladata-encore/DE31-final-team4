from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.db.models import OuterRef, Subquery

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

# @login_required
# def add_favorite_list(request, stock_code):
#     # stock = get_object_or_404(RealTimeStock, stock_code=stock_code)
#     latest_stock = RealTimeStock.objects.filter(stock_code=stock_code).order_by('-id').first()
#     if latest_stock is not None:
#         # UserStock에 해당 유저의 관심종목으로 추가
#         UserStock.objects.get_or_create(user=request.user, stock_code=latest_stock)
#         return redirect('my_favorite_list')
#     else:
#         # 만약 stock_code가 존재하지 않으면 처리 (에러 페이지나 다른 동작을 정의할 수 있음)
#         return redirect('error_page')
@login_required
def add_favorite_list(request, stock_code):
    latest_stock = RealTimeStock.objects.filter(stock_code=stock_code).order_by('-id').first()
    if latest_stock is not None:
        # UserStock에 해당 유저의 관심종목으로 추가
        UserStock.objects.get_or_create(
            user=request.user, 
            stock_id=latest_stock,  # 외래키로 RealTimeStock 객체를 저장
            stock_code=latest_stock.stock_code  # stock_code 필드에 텍스트로 저장
        )
        return redirect('my_favorite_list')
    else:
        # 만약 stock_code가 존재하지 않으면 처리
        return redirect('error_page')


# real_time table 정보 가져오기
# @login_required
# def my_favorite_list(request):
#     user_stocks = UserStock.objects.filter(user=request.user)
#     stock_info = []

#     for user_stock in user_stocks:

#         real_time_stocks = RealTimeStock.objects.filter(stock_code=user_stock.stock_id.stock_id)
        
#         if real_time_stocks.exists():
#             # 여러 객체 중에서 가장 최신 객체를 선택 (예: 가장 높은 id를 가진 객체)
#             latest_stock = real_time_stocks.order_by('-id').first()
#             stock_info.append({
#                 'stock_code': latest_stock.stock_code,
#                 'name': latest_stock.name,
#                 'current_price': latest_stock.current_price,
#                 'UpDownRate': latest_stock.UpDownRate,
#                 'UpDownPoint': latest_stock.UpDownPoint,
#                 "id": latest_stock.id,
#             })
#     return render(request, 'mypage/mypage.html', {'stock_info': stock_info})

def my_favorite_list(request):
    user_stocks = UserStock.objects.filter(user=request.user).select_related('stock_id')
    stock_info = {}
    
    # 각 stock_code의 최신 RealTimeStock 객체를 선택합니다.
    for user_stock in user_stocks:
        stock_code = user_stock.stock_id.stock_code
        # 최신 RealTimeStock 객체를 가져옵니다.
        latest_stock = RealTimeStock.objects.filter(stock_code=stock_code).order_by('-id').first()
        if latest_stock:
            if stock_code not in stock_info or latest_stock.id > stock_info[stock_code]['id']:
                stock_info[stock_code] = {
                    'stock_code': latest_stock.stock_code,
                    'name': latest_stock.name,
                    'current_price': latest_stock.current_price,
                    'UpDownRate': latest_stock.UpDownRate,
                    'UpDownPoint': latest_stock.UpDownPoint,
                    'id': latest_stock.id
                }
    
    # stock_info의 값을 리스트로 변환하고, id 기준으로 정렬합니다.
    stock_info_list = list(stock_info.values())
    stock_info_list.sort(key=lambda x: x['id'], reverse=True)
    
    return render(request, 'mypage/mypage.html', {'stock_info': stock_info_list})