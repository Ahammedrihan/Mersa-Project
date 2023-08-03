from django.db import models
from accountapp.models import CustomUser
from custom_adminapp.models import Product,Variant,Brand,Category
# Create your models here.



    
class Order(models.Model):
    STATUS =(

        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled','Cancelled'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=20)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    order_note = models.TextField(blank=True,null=True)

    order_total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    order_created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    payment_mode = models.CharField(max_length=100,null=True)
    payment_id = models.CharField(max_length=250,null=True)

   


    def __str__(self):
        return  f"Order of {self.user.first_name}"
   
    

class OrderProduct(models.Model):
    STATUS =(

        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled','Cancelled'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        
    )
    order_no = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orderproduct')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    varaiant = models.ForeignKey(Variant,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=False)
    amount = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    def __str__(self):
        return self.product.product_name
    

    
    

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='profile_images/',null=True,blank=True)

    
    def __str__(self) -> str:
        return self.user.first_name
    


class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet for {self.user.first_name}"
