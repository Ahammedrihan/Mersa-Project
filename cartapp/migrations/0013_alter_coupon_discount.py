# Generated by Django 4.2.2 on 2023-07-20 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0012_alter_coupon_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
