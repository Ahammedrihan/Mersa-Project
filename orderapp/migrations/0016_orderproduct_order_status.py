# Generated by Django 4.2.2 on 2023-07-19 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0015_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Out for Shipping', 'Out for Shipping'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=20),
        ),
    ]