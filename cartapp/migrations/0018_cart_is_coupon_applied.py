# Generated by Django 4.2.2 on 2023-08-02 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0017_alter_coupon_max_amount_alter_coupon_min_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_coupon_applied',
            field=models.BooleanField(default=False),
        ),
    ]
