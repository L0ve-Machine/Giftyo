# Giftyo/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from accounts.forms import EmailOrUsernameAuthenticationForm
from influencer.views import InfluencerSignUpView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("manage/", include("core.urls")),

    # ログイン
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=EmailOrUsernameAuthenticationForm,
        ),
        name="login",
    ),

    # カスタム logout を include("auth.urls") の前に定義
    path(
        "logout/",
        LogoutView.as_view(next_page="login"),
        name="logout"
    ),

    # 標準のパス（password_change や password_reset など）
    path("", include("django.contrib.auth.urls")),

    # インフルエンサー用サインアップ
    path("signup/", InfluencerSignUpView.as_view(), name="signup"),

    # その他ルート
    path("influencer/", include("influencer.urls", namespace="influencer")),
    path("", include("fan.urls", namespace="fan")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
