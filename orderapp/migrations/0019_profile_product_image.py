# Generated by Django 4.2.2 on 2023-07-27 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0018_rename_order_status_orderproduct_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
