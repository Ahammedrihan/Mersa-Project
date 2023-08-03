from django.db import models
from decimal import Decimal







class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    brand_status = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_image = models.ImageField(upload_to='category_images/', default=None, blank=True, null=True)
    category_status = models.BooleanField(default=True)




  

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    product_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_description = models.TextField(max_length=2000, blank=True)
    product_status = models.BooleanField(default=True)
    product_image = models.ImageField(upload_to='product_images/')


    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.product_name

class Variant(models.Model):
    variant_name = models.CharField(max_length=100, unique=True)
    mrp = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    variant_description = models.TextField(max_length=2000, blank=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    variant_status = models.BooleanField(default=True)
    variant_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.variant_name

class VariantImage(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='images')
    image1 = models.ImageField(upload_to='variant_images/', null=False, blank=False)
    image2 = models.ImageField(upload_to='variant_images/' ,null= False, blank= False)
    image3 = models.ImageField(upload_to='variant_images/',null= False, blank= False)

    def __str__(self):
        return str(self.id)




