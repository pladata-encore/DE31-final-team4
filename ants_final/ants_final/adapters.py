from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated and request.user.socialaccount_set.filter(provider='google').exists():
            return '/accounts/google/login'  # 구글 로그인 성공 시 리디렉션 경로
        return super().get_login_redirect_url(request)
