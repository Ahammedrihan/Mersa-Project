# Generated by Django 4.2.2 on 2023-07-02 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50, unique=True)),
                ('brand_status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('category_image', models.ImageField(blank=True, default=None, null=True, upload_to='category_images/')),
                ('category_status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('product_description', models.TextField(blank=True, max_length=2000)),
                ('product_status', models.BooleanField(default=True)),
                ('product_image', models.ImageField(blank=True, upload_to='product_images/')),
                ('product_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='custom_adminapp.brand')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='custom_adminapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(max_length=100, unique=True)),
                ('mrp', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('offer_price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('variant_description', models.TextField(blank=True, max_length=2000)),
                ('variant_status', models.BooleanField(default=True)),
                ('variant_stock', models.IntegerField(default=0)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_adminapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='VariantImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(default='default_image.png', upload_to='variant_images/')),
                ('image2', models.ImageField(upload_to='variant_images/')),
                ('image3', models.ImageField(upload_to='variant_images/')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='custom_adminapp.variant')),
            ],
        ),
    ]