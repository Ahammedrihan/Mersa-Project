# Generated by Django 4.2.2 on 2023-07-04 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_adminapp', '0005_remove_variantimage_image2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantimage',
            name='image2',
            field=models.ImageField(default=1, upload_to='variant_images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variantimage',
            name='image3',
            field=models.ImageField(default=1, upload_to='variant_images/'),
            preserve_default=False,
        ),
    ]