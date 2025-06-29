from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from core.models import WarehouseInfo  # 追加

# fan/views.py
import random
import logging

from influencer.models import Influencer, WishItem, Gift



logger = logging.getLogger(__name__)



from django.conf import settings   # 追加

def confirm_payment(request, slug, gift_id):
    influencer = get_object_or_404(Influencer, slug=slug)
    gift       = get_object_or_404(Gift, pk=gift_id, to_profile=influencer)

    return render(request, "fan/payment_summary.html", {
        "influencer": influencer,
        "gift":       gift,
        "shipping_fee":    1500,
        "anonymous_fee":   1200,
        "wrapping_option": "スタンダード",
        "wrapping_fee":    500,
        "message_card_fee":0,
        "payment_fee":     130,
        "total_amount":    3330,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,  # ★追加
    })



def influencer_list(request):
    # ———————— 検索キーワード取得 ————————
    q = request.GET.get('q', '').strip()

    # ———————— ベースクエリ ————————
    # 公開フラグが立っているものだけ絞る
    qs = Influencer.objects.filter(is_public=True)

    # ———————— 検索絞り込み ————————
    if q:
        qs = qs.filter(display_name__icontains=q)

    # ———————— ランダム3名取得 ————————
    random_influencers = qs.order_by('?')[:3]

    # デバッグログ（任意）
    logger.debug(
        "Search q=%r → total=%d, random=%s",
        q,
        qs.count(),
        list(random_influencers.values_list('display_name', flat=True))
    )

    # ———————— テンプレートへ渡す ————————
    return render(request, 'fan/home.html', {
        'influencers': qs,                 # 検索済み or 全件
        'random_influencers': random_influencers,
        'q': q,                            # テンプレートで再表示したい場合
    })





def gift_notify(request, slug):
    influencer = get_object_or_404(Influencer, slug=slug)
    warehouse  = WarehouseInfo.objects.first()

    # 公開中の WishItem 一覧
    wish_items = influencer.wish_items.filter(is_visible=True)

    # -------- ここを変更: ?item=<id> があれば優先 --------
    item_id = request.GET.get("item")
    if item_id:
        # 指定 id が公開中でなければ 404
        selected_item = get_object_or_404(wish_items, pk=item_id)
    else:
        selected_item = wish_items.first()
    # ------------------------------------------------------

    # 以降は既存ロジック
    error_message     = ''
    tracking_number   = ''
    fan_nickname      = ''
    anonymous_message = ''
    sent_date         = ''

    if request.method == 'POST':
        tracking_number   = request.POST.get('tracking_number', '').strip()
        fan_nickname      = request.POST.get('fan_nickname', '').strip()
        anonymous_message = request.POST.get('anonymous_message', '').strip()
        sent_date         = request.POST.get('sent_date') or timezone.now().date()

        if not tracking_number:
            error_message = '追跡番号は必須です'

        if not error_message:
            gift = Gift.objects.create(
                to_profile      = influencer,
                wish_item       = selected_item,
                sender_name     = fan_nickname or "匿名",
                tracking_number = tracking_number,
                sent_date       = sent_date,
                message         = anonymous_message,
                shipping_fee     = 500,
                anonymous_fee    = 100,
                wrapping_fee     = 200,
                message_card_fee = 150,
                payment_fee      = 50,
            )
            return render(request, "fan/payment_summary.html", {
                "influencer":      influencer,
                "gift":            gift,
                "shipping_fee":    500,
                "anonymous_fee":   100,
                "wrapping_option": "スタンダード",
                "wrapping_fee":    200,
                "message_card_fee":150,
                "payment_fee":     50,
                "total_amount":    500 + 100 + 200 + 150 + 50,
                "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
            })

    return render(request, "fan/gift_notify.html", {
        "influencer":        influencer,
        "warehouse":         warehouse,
        "wish_items":        wish_items,
        "selected_item":     selected_item,
        "error_message":     error_message,
        "tracking_number":   tracking_number,
        "fan_nickname":      fan_nickname,
        "anonymous_message": anonymous_message,
        "sent_date":         sent_date,
    })


def thank_you(request):
    """
    Stripe 決済完了後にリダイレクトされるサンクスページ。
    ?influencer=<slug> が付いていれば、そのインフルエンサー情報を表示する。
    """
    slug = request.GET.get("influencer")           # 例: /thank-you/?influencer=test
    influencer = (
        get_object_or_404(Influencer, slug=slug)   # slug があれば取得
        if slug else None                          # 無ければ None
    )

    return render(request, "fan/thank_you.html", {
        "influencer": influencer,                  # テンプレート側でリンク等に使う
    })




# fan/views.py
import os
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Stripe 初期化
stripe.api_key = settings.STRIPE_SECRET_KEY

# ----------------------- Checkout Session 生成 -----------------------
@require_POST
def create_checkout_session(request, slug, gift_id):
    """
    ギフト 1 件分の Stripe Checkout セッションを作成して
    JSON で {id: <session_id>} を返す。
    """
    influencer = get_object_or_404(Influencer, slug=slug)
    gift = get_object_or_404(Gift, pk=gift_id, to_profile=influencer)

    # ------- 決済金額を取得（total_amount が無ければ自前計算） -------
    amount_jpy = getattr(
        gift,
        "total_amount",
        gift.shipping_fee
        + gift.anonymous_fee
        + gift.wrapping_fee
        + gift.message_card_fee
        + gift.payment_fee,
    )

    # ------- 決済成功時に ?influencer=<slug> を付けて戻す -------
    success_url = (
        request.build_absolute_uri(reverse("fan:thank_you"))
        + f"?influencer={influencer.slug}"
    )

    # ------- Checkout Session 作成 -------
    session = stripe.checkout.Session.create(
        mode="payment",
        client_reference_id=str(gift.id),
        line_items=[
            {
                "price_data": {
                    "currency": "jpy",
                    "unit_amount": amount_jpy,
                    "product_data": {
                        "name": f"Gift to {influencer.display_name}",
                    },
                },
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=request.build_absolute_uri(reverse("fan:payment_cancel")),
    )

    return JsonResponse({"id": session.id})

# ----------------------- 決済キャンセル -----------------------
def payment_cancel(request):
    return render(request, "fan/payment_cancel.html")

# ----------------------- Webhook -----------------------
@csrf_exempt
def stripe_webhook(request):
    payload       = request.body
    sig_header    = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    # ───────── 決済完了 ─────────
    if event["type"] == "checkout.session.completed":
        session  = event["data"]["object"]
        gift_id  = session.get("client_reference_id")

        if gift_id:
            try:
                # Gift と WishItem を同時に取得
                gift = Gift.objects.select_related("wish_item").get(pk=gift_id)

                # ① Gift の支払いフラグを更新
                gift.is_paid = True
                gift.paid_at = timezone.now()
                gift.save(update_fields=["is_paid", "paid_at"])

                # ② 対象 WishItem を非表示化
                if gift.wish_item and gift.wish_item.is_visible:
                    gift.wish_item.is_visible = False
                    gift.wish_item.save(update_fields=["is_visible"])

            except Gift.DoesNotExist:
                logger.error("Gift %s not found", gift_id)

    return HttpResponse(status=200)

