# influencer/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Influencer, WishItem, Gift
from .forms import InfluencerForm, WishItemForm
from core.models import WarehouseInfo
from .models import ShippingAddress
from .forms import ShippingAddressForm
from django.contrib import messages

@login_required
def influencer_profile_view(request):
    """
    ログイン中のユーザーが、自身の Influencer プロフィールを作成・編集するビュー
    （プロフィール画像／自己紹介／SNSリンク／公開設定 を扱う）
    """
    try:
        profile = request.user.influencer_profile
    except Influencer.DoesNotExist:
        profile = None

    if request.method == 'POST':
        # 画像アップロード対応のため request.FILES を渡す
        form = InfluencerForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            inf = form.save(commit=False)
            inf.user = request.user
            inf.save()
            return redirect('influencer:dashboard')
    else:
        form = InfluencerForm(instance=profile)

    return render(request, 'influencer/profile_edit.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def gift_mark_read_view(request, pk):
    if request.method == 'POST':
        # 自分のギフトだけを操作可能に
        gift = get_object_or_404(
            Gift,
            pk=pk,
            to_profile=request.user.influencer_profile
        )
        gift.is_read = True
        gift.save()
    return redirect('influencer:dashboard')



@login_required
def shipping_address_view(request):
    profile = request.user.influencer_profile
    try:
        address = profile.shipping_address
    except ShippingAddress.DoesNotExist:
        address = None

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            shipping        = form.save(commit=False)
            shipping.influencer = profile
            shipping.save()
            # 成功メッセージをセットしてリダイレクト
            messages.success(request, '保存しました！')
            return redirect('influencer:shipping_address')
        else:
            # ここが必ず else の中に入るようインデントを確認
            messages.error(request, '入力内容を確認してください。')
            # このままレンダーするとエラーメッセージのみが表示されます
    else:
        form = ShippingAddressForm(instance=address)

    return render(request, 'influencer/shipping_address.html', {
        'form': form,
    })


@login_required
def influencer_dashboard_view(request):
    try:
        profile = request.user.influencer_profile
    except Influencer.DoesNotExist:
        return redirect('influencer:profile')

    # 未読ギフトを取得
    unread_gifts = Gift.objects.filter(
        to_profile=profile,
        is_read=False
    ).order_by('-created_at')

    # WishItem 一覧
    wish_list = profile.wish_items.all().order_by('order', '-created_at')

    return render(request, 'influencer/dashboard.html', {
        'profile': profile,
        'wish_list': wish_list,
        'unread_gifts': unread_gifts,  # ここでテンプレートに渡す
    })


@login_required
def wishitem_create_view(request):
    """
    WishItem の新規登録ビュー
    """
    try:
        influencer = request.user.influencer_profile
    except Influencer.DoesNotExist:
        # プロフィールがなければ先にプロフィール作成ページへ
        return redirect('influencer:profile')

    if request.method == 'POST':
        # 画像アップロード対応のため request.FILES を渡す
        form = WishItemForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False にしてから influencer をセット
            wish = form.save(commit=False)
            wish.influencer = influencer
            wish.save()
            return redirect('influencer:dashboard')
    else:
        form = WishItemForm(initial={
            # もしデフォルトで order を「末尾に追加」したい場合はここで設定可
            # 例: 'order': influencer.wish_items.count() + 1
        })

    return render(request, 'influencer/wishitem_form.html', {
        'form': form,
        'action': '作成',  # テンプレート側で「作成」か「編集」を判別してラベル変更
    })


@login_required
def wishitem_edit_view(request, pk):
    """
    WishItem の編集ビュー
    """
    # 他ユーザーの WishItem を編集できないようチェック
    wish = get_object_or_404(WishItem, pk=pk, influencer__user=request.user)

    if request.method == 'POST':
        # 画像アップロード対応のため request.FILES を渡す
        form = WishItemForm(request.POST, request.FILES, instance=wish)
        if form.is_valid():
            form.save()
            return redirect('influencer:dashboard')
    else:
        form = WishItemForm(instance=wish)

    return render(request, 'influencer/wishitem_form.html', {
        'form': form,
        'action': '編集',
    })


@login_required
def wishitem_delete_view(request, pk):
    """
    WishItem の削除確認／実行ビュー
    """
    wish = get_object_or_404(WishItem, pk=pk, influencer__user=request.user)

    if request.method == 'POST':
        wish.delete()
        return redirect('influencer:dashboard')

    # GET の場合は削除確認ページを表示
    return render(request, 'influencer/wishitem_confirm_delete.html', {
        'wish': wish
    })



def influencer_public_profile(request, slug):
    """
    公開用プロフィールページ（ファン向け）
    URL: /u/<slug>/
      ・プロフィール情報（アイコン／表示名／自己紹介／SNSリンク）
      ・公開設定(is_public=True)かつ is_visible=True の WishItem 一覧 を表示
      ・WarehouseInfo などをテンプレートに渡す例
    """
    influencer = get_object_or_404(Influencer, slug=slug, is_public=True)

    # ダッシュボードと同じく、全WishItemを取得（並び順: order → -created_at）
    wish_items = influencer.wish_items.all().order_by('order', '-created_at')
    # ※公開フラグで絞りたい場合は .filter(is_visible=True) を追加してください

    # core アプリの WarehouseInfo を取得（例として最初の1件）
    warehouse = WarehouseInfo.objects.first()

    return render(request, 'fan/influencer_public.html', {
        'influencer': influencer,
        'wish_items': wish_items,
        'warehouse': warehouse,
    })



def gift_notify(request, slug):
    """
    ギフト通知ページ（ファンが「このギフトを贈る」ボタンを押したときに遷移する画面）
    URL: /u/<slug>/notify/
    """
    influencer = get_object_or_404(Influencer, slug=slug)
    # POST 処理は別途実装
    return render(request, 'influencer/gift_notify.html', {
        'influencer': influencer
    })


