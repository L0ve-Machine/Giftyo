# fan/views.py（再掲・一部追記）
from django.shortcuts import render, get_object_or_404, redirect
from influencer.models import Influencer, WishItem
# from gift.models import Gift             # 後ほど正式にモデルを定義したら有効化
from django.utils import timezone
from core.models import WarehouseInfo  # 追加

def home(request):
    influencers = Influencer.objects.all()
    return render(request, 'fan/home.html', {"influencers": influencers})




def gift_notify(request, slug):
    influencer = get_object_or_404(Influencer, slug=slug)
    wish_items = influencer.wish_items.filter(is_visible=True)

    if request.method == 'POST':
        # POSTされたデータを取得
        tracking_number = request.POST.get('tracking_number')
        fan_nickname = request.POST.get('fan_nickname', '')
        anonymous_message = request.POST.get('anonymous_message', '')
        sent_date = request.POST.get('sent_date') or timezone.now().date()
        wish_item_id = request.POST.get('wish_item_id')

        # 本実装では Gift モデルを用いてデータベース登録する
        # ↓ ダミー実装例 ↓
        # gift = Gift.objects.create(
        #     wish_item=WishItem.objects.get(id=wish_item_id),
        #     fan_nickname=fan_nickname,
        #     anonymous_message=anonymous_message,
        #     tracking_number=tracking_number,
        #     sent_date=sent_date,
        #     is_paid=False,
        # )
        # ここではまだ Gift モデルがないため登録せずにテンプレート表示
        return render(request, 'fan/gift_notify_done.html', {
            "influencer": influencer,
            "tracking_number": tracking_number,
        })

    # GET: フォーム表示
    return render(request, 'fan/gift_notify.html', {
        "influencer": influencer,
        "wish_items": wish_items,
    })

