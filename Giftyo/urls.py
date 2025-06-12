# Giftyo/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 管理サイト
    path('admin/', admin.site.urls),

    # 認証（ログイン・ログアウトなど）
    path('accounts/', include('django.contrib.auth.urls')),

    # インフルエンサー用機能（プロフィール／ダッシュボード／WishItem CRUD）
    path('influencer/', include('influencer.urls', namespace='influencer')),

    # ファン側の URL はすべて fan/urls.py に任せる
    path('', include('fan.urls', namespace='fan')),

    # ※ /u/<slug>/ は fan/urls.py で定義しているので、ここでは書かない
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

