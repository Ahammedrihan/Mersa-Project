from django.contrib import admin
from .models import Cart,CartItem,Wishlist,Coupon,UserCoupon

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(Coupon)
admin.site.register(UserCoupon)