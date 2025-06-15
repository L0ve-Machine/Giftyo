# fan/urls.py
from django.urls import path
from .views import influencer_list, gift_notify, confirm_payment, thank_you
from influencer.views import influencer_public_profile

app_name = 'fan'

urlpatterns = [
    # 1. トップページ
    path('', influencer_list, name='home'),

    # 2. インフルエンサー詳細
    path('u/<slug:slug>/', influencer_public_profile, name='influencer_public'),

    # 3. ギフト通知フォーム
    path('u/<slug:slug>/notify/', gift_notify, name='gift_notify'),

    # 4. ギフト支払い確認画面
    path(
        'u/<slug:slug>/confirm-payment/<int:gift_id>/',
        confirm_payment,
        name='confirm_payment'
    ),
    path('thank-you/', thank_you, name='thank_you'),
]
