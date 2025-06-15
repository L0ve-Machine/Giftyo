from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from core.models import WarehouseInfo  # 追加

# fan/views.py
import random
import logging

from influencer.models import Influencer, WishItem, Gift



logger = logging.getLogger(__name__)



def confirm_payment(request, slug, gift_id):
    influencer = get_object_or_404(Influencer, slug=slug)
    gift = get_object_or_404(Gift, pk=gift_id, to_profile=influencer)
    # 必要ならここで金額情報を計算したり…
    return render(request, 'fan/payment_summary.html', {
        'influencer': influencer,
        'gift': gift,
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
    influencer    = get_object_or_404(Influencer, slug=slug)
    warehouse     = WarehouseInfo.objects.first()
    wish_items    = influencer.wish_items.filter(is_visible=True)
    selected_item = wish_items.first()

    # ── ここで初期化 ──
    error_message     = ''
    tracking_number   = ''
    fan_nickname      = ''
    anonymous_message = ''
    sent_date         = ''

    if request.method == 'POST':
        # フォーム値取得
        tracking_number   = request.POST.get('tracking_number', '').strip()
        fan_nickname      = request.POST.get('fan_nickname', '').strip()
        anonymous_message = request.POST.get('anonymous_message', '').strip()
        sent_date         = request.POST.get('sent_date') or timezone.now().date()

        # バリデーション
        if not tracking_number:
            error_message = '追跡番号は必須です'

        # エラーなければ Gift 作成 → 支払い内訳画面へ
        if not error_message:
            gift = Gift.objects.create(
                to_profile      = influencer,
                wish_item       = selected_item,
                sender_name     = fan_nickname or '匿名',
                tracking_number = tracking_number,
                sent_date       = sent_date,
                message         = anonymous_message,
            )
            # 支払い内訳テンプレートへ
            return render(request, 'fan/payment_summary.html', {
                'influencer':      influencer,
                'gift':            gift,
                # 以下サンプル。実際の計算結果を渡してください。
                'shipping_fee':    500,
                'anonymous_fee':   100,
                'wrapping_option':'スタンダード',
                'wrapping_fee':    200,
                'message_card_fee':150,
                'payment_fee':     50,
                'total_amount':    500 + 100 + 200 + 150 + 50,
            })

    # GET またはバリデーションエラー時はフォームを再表示
    return render(request, 'fan/gift_notify.html', {
        'influencer':        influencer,
        'warehouse':         warehouse,
        'wish_items':        wish_items,
        'selected_item':     selected_item,
        'error_message':     error_message,
        'tracking_number':   tracking_number,
        'fan_nickname':      fan_nickname,
        'anonymous_message': anonymous_message,
        'sent_date':         sent_date,
    })


def thank_you(request):
    return render(request, 'fan/thank_you.html')