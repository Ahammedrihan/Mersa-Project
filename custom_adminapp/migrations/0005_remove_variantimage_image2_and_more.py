# Generated by Django 4.2.2 on 2023-07-04 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_adminapp', '0004_remove_product_product_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variantimage',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='variantimage',
            name='image3',
        ),
        migrations.AlterField(
            model_name='variantimage',
            name='image1',
            field=models.ImageField(upload_to='variant_images/'),
        ),
    ]