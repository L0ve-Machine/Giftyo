# Generated by Django 5.2.2 on 2025-06-11 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0002_alter_wishitem_options_wishitem_brand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='free_url1',
            field=models.URLField(blank=True, verbose_name='フリーURL1'),
        ),
        migrations.AddField(
            model_name='influencer',
            name='free_url2',
            field=models.URLField(blank=True, verbose_name='フリーURL2'),
        ),
    ]
