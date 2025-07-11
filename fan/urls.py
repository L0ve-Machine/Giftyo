# fan/urls.py
from django.urls import path
from . import views                          # ★ モジュールごと import
from influencer.views import influencer_public_profile

app_name = "fan"

urlpatterns = [
    # 1. トップページ
    path("", views.influencer_list, name="home"),
    path('all/', views.influencer_list_all, name='influencer_list_all'),

    # 2. インフルエンサー詳細
    path("u/<slug:slug>/", influencer_public_profile, name="influencer_public"),

    # 3. ギフト通知フォーム
    path("u/<slug:slug>/notify/", views.gift_notify, name="gift_notify"),

    # 4. 支払い内訳確認
    path(
        "u/<slug:slug>/confirm-payment/<int:gift_id>/",
        views.confirm_payment,
        name="confirm_payment",
    ),

    # 5. Stripe Checkout セッション生成（POST）
    path(
        "u/<slug:slug>/pay/<int:gift_id>/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),

    # 6. 決済キャンセル
    path("payment-cancel/", views.payment_cancel, name="payment_cancel"),

    # 7. 決済完了サンクス
    path("thank-you/", views.thank_you, name="thank_you"),

    # 8. Webhook 受信
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
]
