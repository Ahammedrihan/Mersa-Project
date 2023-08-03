# Generated by Django 4.2.2 on 2023-07-20 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0009_coupon_usercoupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon_is_applied',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cartapp.coupon'),
            preserve_default=False,
        ),
    ]
