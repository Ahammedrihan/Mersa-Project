# Generated by Django 4.2.2 on 2023-07-20 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0010_cart_coupon_is_applied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='applicable_type',
            field=models.CharField(choices=[('all', 'Category All'), ('category', 'Category')], max_length=10),
        ),
    ]
