# Generated by Django 4.2.2 on 2023-07-11 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_adminapp', '0006_variantimage_image2_variantimage_image3'),
        ('orderapp', '0006_rename_phone_number_order_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='created_at',
            new_name='order_date',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_total',
            new_name='order_total_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_ordered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='prodcut',
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Out for Shipping', 'Out for Shipping'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='New', max_length=20),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_adminapp.product'),
        ),
    ]