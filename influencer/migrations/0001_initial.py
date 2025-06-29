# Generated by Django 5.1.4 on 2025-06-04 15:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Influencer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=50, unique=True, verbose_name='表示名')),
                ('bio', models.TextField(blank=True, verbose_name='自己紹介')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='influencer_profiles/', verbose_name='プロフィール画像')),
                ('instagram_url', models.URLField(blank=True, verbose_name='Instagram URL')),
                ('twitter_url', models.URLField(blank=True, verbose_name='Twitter（X）URL')),
                ('tiktok_url', models.URLField(blank=True, verbose_name='TikTok URL')),
                ('is_public', models.BooleanField(default=False, verbose_name='公開設定')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='URLスラッグ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='influencer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WishItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, verbose_name='商品名')),
                ('product_url', models.URLField(verbose_name='商品URL')),
                ('image_url', models.URLField(blank=True, verbose_name='画像URL')),
                ('desired_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='希望価格')),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='備考')),
                ('is_visible', models.BooleanField(default=True, verbose_name='公開設定')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_items', to='influencer.influencer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
