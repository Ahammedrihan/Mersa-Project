# Generated by Django 4.2.2 on 2023-07-03 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='product_images/'),
        ),
    ]
