# Generated by Django 4.2.2 on 2023-07-24 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_adminapp', '0007_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]