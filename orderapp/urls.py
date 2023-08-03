
from django.urls import path 
from .import views

urlpatterns = [
    path('place-order',views.place_order, name="place_order"),
    path('order_success',views.order_success, name="order_success"),
    path('my-orders',views.my_orders, name="my_orders"),
    path('razorpay_payment/', views.razorpay_payment, name='razorpay_payment')

   
   
   
]
