# core/manage.py
from django.contrib import admin
from .models import WarehouseInfo

@admin.register(WarehouseInfo)
class WarehouseInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'postal_code', 'pref', 'city')
    search_fields = ('name', 'city')

