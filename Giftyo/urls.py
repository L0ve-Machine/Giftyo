# Giftyo/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from influencer.views import InfluencerSignUpView   # ← 追加

urlpatterns = [
    # 管理サイト
    path("admin/", admin.site.urls),

    # 運営側（core アプリ）ダッシュボード
    path("manage/", include("core.urls")),

    # ────────── 認証まわり ──────────
    # 標準ログイン・ログアウト・パスワード再設定フロー
    #   /login/            （名前: login）
    #   /logout/           （名前: logout）
    #   /password_reset/   ほか 3 URL
    path("", include("django.contrib.auth.urls")),

    # 新規登録（インフルエンサー）
    path("signup/", InfluencerSignUpView.as_view(), name="signup"),

    # ────────── 機能別アプリ ──────────
    # インフルエンサー機能（プロフィール／ダッシュボードなど）
    path("influencer/", include("influencer.urls", namespace="influencer")),

    # ファン側の一般ページ
    path("", include("fan.urls", namespace="fan")),
]

# 開発中はメディアを直接配信
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

