from django.db import models
from custom_adminapp.models import Product, Variant ,Category
from accountapp.models import CustomUser

from django.db import models
from django.utils import timezone


# Create your models here.
#The _cart_id function is used to retrieve or create this cart ID from the user's session. 

class Wishlist(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)


    def __str__(self):
        return self.product
    


class Coupon(models.Model):

    DISCOUNT_TYPES = (
    ('percentage', 'Percentage'),
    ('amount', 'Amount'),
)
    APPLICABLE_TYPES = (
    ('all', 'Category All'),
    ('category', 'Category'), 
)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount = models.DecimalField(max_digits=10, decimal_places=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    applicable_type = models.CharField(max_length=10, choices=APPLICABLE_TYPES)
    category = models.ForeignKey( Category, on_delete=models.SET_NULL,default= None, null=True, blank=True)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)
    max_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)

    def is_valid(self):
        current_time = timezone.now()
        return self.is_active and self.start_date <= current_time and self.end_date >= current_time

    def is_applicable_to_order(self, order_amount, order_category):
        if not self.is_valid():
            return False

        if self.applicable_type == 'all':
            return True
        elif self.applicable_type == 'category' and self.category == order_category:
            return True
        
        return False

    
    def __str__(self):
        return self.name



class UserCoupon(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    coupon_applied = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    is_applied = models.BooleanField(default=True)

    



class Cart(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    cart_id = models.CharField(max_length=250, blank=True, default='default_value')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon_is_applied = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    is_coupon_applied = models.BooleanField(default=False)

    def get_total_mrp(self):
        return sum(item.get_subtotal_mrp_price() for item in self.cart_items.all())
    
    def get_total_offer_price(self):
        return sum(item.get_subtotal_offer_price() for item in self.cart_items.all())
    
    def get_total_quantity(self):
        return sum(item.cart_quantity for item in self.cart_items.all())

    def get_total_discount_price(self):
        return sum(item.get_subtotal_discount_price() for item in self.cart_items.all())
    
    def get_shipping_charge(self):
        total_amount = self.get_total_mrp()
        if total_amount > 10000:
            return 0
        else:
            return 50
    def calculate_discount(self):
        try:
            if self.coupon_is_applied and self.coupon_is_applied.is_valid() :
                if self.coupon_is_applied.discount_type == 'percentage':
                    if self.coupon_is_applied.max_amount <= ((self.coupon_is_applied.discount / 100) * self.get_total_offer_price()):
                        return self.coupon_is_applied.max_amount
                    else:
                        return (self.coupon_is_applied.discount / 100) * self.get_total_offer_price() 
                elif self.coupon_is_applied.discount_type == 'amount':
                    return self.coupon_is_applied.discount
                else:
                   return 0
                
            else:
                return 0
        except:
            return 0
        
        
    def get_total_count(self):
        return sum(item.get_sub_count() for item in self.cart_items.all() )


   
    def get_total(self):
        if self.coupon_is_applied and self.coupon_is_applied.min_purchase < self.get_total_offer_price():
           return self.get_total_offer_price() + self.get_shipping_charge() -  self.calculate_discount()
        else:
            return self.get_total_offer_price() + self.get_shipping_charge() 
    


    def __str__(self):
        return str(self.cart_id)
    
    
class CartItem(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items',null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    cart_quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default= True)

    def get_subtotal_mrp_price(self):
        return self.variant.mrp * self.cart_quantity
    
    
    def get_subtotal_offer_price(self):
        return self.variant.offer_price * self.cart_quantity
    
    def get_subtotal_discount_price(self):
        return self.variant.discount * self.cart_quantity
    
    def __str__(self):
        return str(self.product)
    def get_sub_count(self):
        return self.cart_quantity
        



    




