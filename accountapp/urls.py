from django.urls import path 
from .import views

urlpatterns = [
    path('',views.user_welcome,name='welcome_page'),
    path('user-registration', views.user_registration, name='registration'),
    path('user-login', views.user_login, name='userlogin'),
    path('user-logout', views.user_logout, name='userlogout'),
    path('user-home', views.home_page, name='home'),
    path('user-shop', views.shop_page, name='shop'),
    path('verify-otp', views.verify_otp, name='verify_otp'),
    path('user-profile', views.user_profile, name='user_profile'),
    path('delete-address', views.delete_address, name='delete_address'),
    path('edit-address', views.edit_address, name='edit_address'),
    path('add-address', views.add_address, name='add_address'),
    path('user-profile-order-page-view/<int:order_id>/', views.user_profile_order_page_view, name='user_profile_order_page_view'),
    path('user-profile-orders', views.user_profile_orders, name='user_profile_orders'),
    path('get_order_details/<int:order_id>/', views.get_order_details, name='get_order_details'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('return_order/<int:order_id>/', views.return_order, name='return_order'),
    path('cancel_product/<int:order_id>/', views.cancel_product, name='cancel_product'),
    path('return_product/<int:order_id>/', views.return_product, name='return_product'),
    path('search', views.search, name='search'),
    path('reset-password', views.reset_password, name='reset_password'),
    path('reset-password-page', views.reset_password_page, name='reset_password_page'),

   

    








    
    
    
]
    # path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name ='activate'),