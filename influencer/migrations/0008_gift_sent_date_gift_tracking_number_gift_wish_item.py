# influencer/migrations/0008_gift_sent_date_gift_tracking_number_gift_wish_item.py

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0007_alter_shippingaddress_city_and_more'),
    ]

    operations = [
        # ① wish_item の追加（既存レコードはNULL許容）
        migrations.AddField(
            model_name='gift',
            name='wish_item',
            field=models.ForeignKey(
                to='influencer.WishItem',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='gifts',
                verbose_name='対象WishItem',
                null=True,
                blank=True,
            ),
        ),
        # ② tracking_number の追加
        migrations.AddField(
            model_name='gift',
            name='tracking_number',
            field=models.CharField(
                default='',
                max_length=100,
                verbose_name='追跡番号',
            ),
            preserve_default=False,
        ),
        # ③ sent_date の追加
        migrations.AddField(
            model_name='gift',
            name='sent_date',
            field=models.DateField(
                verbose_name='送付日',
                null=True,
                blank=True,
            ),
        ),
    ]
