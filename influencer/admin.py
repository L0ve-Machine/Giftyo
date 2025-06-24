# influencer/manage.py
from django.contrib import admin
from .models import Influencer, WishItem, Gift

@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'user', 'is_public', 'created_at')
    prepopulated_fields = {'slug': ('display_name',)}

@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'influencer', 'brand', 'desired_price', 'is_visible', 'created_at')
    list_filter = ('influencer', 'is_visible')
    search_fields = ('product_name', 'brand', 'note')

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'to_profile', 'is_read', 'created_at')
    list_filter = ('is_read',)