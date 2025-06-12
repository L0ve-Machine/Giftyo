# influencer/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



class Influencer(models.Model):
    """
    インフルエンサーの公開プロフィール用モデル。
    user: 1対1で Django の User と紐づけ
    display_name: あとでスラッグにも使う公開名
    bio: 自己紹介文（コメント）
    profile_image: プロフィール画像（任意）
    instagram_url, twitter_url, tiktok_url: SNSリンク（任意）
    is_public: 公開設定フラグ
    created_at, updated_at: 自動作成・更新日時
    slug: URL 用スラッグ
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    display_name = models.CharField('表示名', max_length=50, unique=True)
    bio = models.TextField('自己紹介', blank=True)
    profile_image = models.ImageField('プロフィール画像', upload_to='influencer_profiles/', blank=True, null=True)

    instagram_url = models.URLField('Instagram URL', blank=True)
    twitter_url = models.URLField('Twitter（X）URL', blank=True)
    tiktok_url = models.URLField('TikTok URL', blank=True)
    free_url1 = models.URLField('フリーURL1', blank=True)
    free_url2 = models.URLField('フリーURL2', blank=True)

    is_public = models.BooleanField('公開設定', default=False)

    slug = models.SlugField('URLスラッグ', max_length=50, unique=True, blank=True)

    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # slug が未設定なら display_name から自動生成
        if not self.slug:
            self.slug = slugify(self.display_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name


class WishItem(models.Model):
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE, related_name='wish_items')
    product_name = models.CharField('商品名', max_length=200)
    brand = models.CharField('ブランド名', max_length=100, blank=True)  # 追加
    product_url = models.URLField('商品URL')
    image_url = models.URLField('画像URL', blank=True)
    image_file = models.ImageField('商品画像（アップロード）', upload_to='wish_items/%Y/%m/', blank=True, null=True)  # 追加
    desired_price = models.DecimalField('希望価格', max_digits=10, decimal_places=0, null=True, blank=True)
    note = models.TextField('備考', blank=True)  # TextField に変更
    order = models.PositiveIntegerField('並び順', default=0)  # 追加
    is_visible = models.BooleanField('公開設定', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.product_name} ({self.influencer.display_name})"



class Gift(models.Model):
    """インフルエンサー宛のギフト通知モデル"""
    sender_name = models.CharField(
        '送信者名',
        max_length=100,
        help_text='ギフトを送った方のお名前を入力してください'
    )
    to_profile = models.ForeignKey(
        'Influencer',
        on_delete=models.CASCADE,
        related_name='received_gifts',
        verbose_name='受信インフルエンサー'
    )
    message = models.TextField('メッセージ', blank=True)
    is_read = models.BooleanField('既読フラグ', default=False)
    created_at = models.DateTimeField('送信日時', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender_name} → {self.to_profile.display_name} @ {self.created_at:%Y-%m-%d %H:%M}"



# influencer/models.py
class ShippingAddress(models.Model):
    influencer = models.OneToOneField(
        Influencer,
        on_delete=models.CASCADE,
        related_name='shipping_address',
        verbose_name='インフルエンサー'
    )
    recipient_name = models.CharField(
        '宛名',
        max_length=100
        # blank=False がデフォルトなので必須
    )
    postal_code = models.CharField(
        '郵便番号',
        max_length=10
        # blank=False がデフォルトなので必須
    )
    prefecture = models.CharField(
        '都道府県',
        max_length=100
        # blank=False がデフォルトなので必須
    )
    city = models.CharField(
        '市区町村',
        max_length=100
        # blank=False がデフォルトなので必須
    )
    building = models.CharField(
        '建物名・部屋番号',
        max_length=200,
        blank=True  # 建物名のみ任意
    )
    updated_at = models.DateTimeField(
        '更新日時',
        auto_now=True
    )

    def __str__(self):
        return f"{self.influencer.display_name} の送信先"
