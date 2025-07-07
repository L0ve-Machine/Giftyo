from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Influencer, WishItem, Gift
from .forms import InfluencerForm, WishItemForm
from core.models import WarehouseInfo
from .models import ShippingAddress
from .forms import ShippingAddressForm
from django.contrib import messages


from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm  # 同じアプリなのでこれでOK

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


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
            shipping = form.save(commit=False)
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

    # WishItem 一覧（※ダッシュボードでは自分用なので全件表示）
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
    """
    influencer = get_object_or_404(Influencer, slug=slug, is_public=True)

    # ── 公開中 & 未ギフトのみ取得 ──
    wish_items = (
        influencer.wish_items
        .filter(is_visible=True, gifts__isnull=True)
        .order_by('order', '-created_at')
    )

    # 倉庫情報
    warehouse = WarehouseInfo.objects.first()

    # SNSリンク用リスト（Noneは自動的に除外されるので、テンプレートでループ処理OK）
    sns_urls = [
        influencer.instagram_url,
        influencer.twitter_url,
        influencer.tiktok_url,
        influencer.free_url1,
        influencer.free_url2,
    ]

    return render(request, 'fan/influencer_public.html', {
        'influencer': influencer,
        'wish_items': wish_items,
        'warehouse': warehouse,
        'sns_urls': sns_urls,  # ←★ 追加ここ！
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


from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class InfluencerSignUpView(CreateView):
    form_class = UserCreationForm  # 標準フォーム
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')  # 登録完了後ログインフォームへ
