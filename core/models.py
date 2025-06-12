# core/models.py
from django.db import models

class WarehouseInfo(models.Model):
    name = models.CharField('倉庫名', max_length=100, default='Giftyo 倉庫')
    postal_code = models.CharField('郵便番号', max_length=10)
    pref = models.CharField('都道府県', max_length=50)
    city = models.CharField('市区町村', max_length=100)
    address_line = models.CharField('番地以下', max_length=200)
    notes = models.TextField('備考', blank=True)

    def __str__(self):
        return self.name
