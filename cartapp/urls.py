
from django.urls import path 
from .import views

urlpatterns = [
    path('cart',views.cart, name="cart"),
    path('add-cart/<int:product_id>/',views.add_cart, name="add_cart"),
    path('remove-cart/<int:variant_id>/',views.remove_cart, name="remove_cart"),
    path('plus-cart/<int:variant_id>/',views.plus_cart, name="plus_cart"),
    path('remove-cart-button/<int:variant_id>/',views.remove_cart_button, name="remove_cart_button"),
    path('checkout/',views.checkout, name="checkout"),
    path('add-to-wishlist/',views.add_to_wishlist, name="add_to_wishlist"),
    path('wishlist-view/',views.wishlist_view, name="wishlist_view"),
    path('remove-wishlist/<int:product_id>/',views.remove_wishlist, name="remove_wishlist"),
    path('change-address', views.change_Address, name='change_Address'),
    path('apply-coupon', views.apply_coupon, name='apply_coupon'),



  
    



   
]

