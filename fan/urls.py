# fan/urls.py
from django.urls import path
from . import views
from influencer.views import influencer_public_profile, gift_notify

app_name = 'fan'


urlpatterns = [
    # 1. トップページ
    path('', views.home, name='home'),

    # 2. インフルエンサー公開プロフィール詳細
    #    influencer.views から直接ビュー関数をインポートして使う
    path('u/<slug:slug>/', influencer_public_profile, name='influencer_public'),

    # 3. 発送通知フォーム
    path('u/<slug:slug>/notify/', gift_notify, name='gift_notify'),
]