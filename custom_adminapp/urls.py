from django.urls import path 
from .import views

urlpatterns = [
    path('admin-login',views.admin_login,name="adminlogin"),
    path('admin-signout',views.admin_signout,name="adminsignout"),
    path('admin-home',views.admin_home,name="adminhome"),
    path('users-details',views.users_details,name="userdetails"),
    path('user-block/<id>',views.user_block,name="userblock"),
    path('users-unblock/<id>',views.user_un_block,name="user_unblock"),
    path('brand-list',views.brandlist,name="brand"),
    path('category-list',views.categorylist,name="category"),
    path('product-list',views.productlist,name="product"),
    path('add-category', views.add_category, name='add_category'),
    path('add-product', views.add_product, name='add_product'),
    path('add-brand', views.add_brand, name='add_brand'),
    path('edit-product/<int:product_id>', views.edit_product, name='edit_product'),
    path('edit-brand/<int:brand_id>', views.edit_brand, name='edit_brand'),
    path('edit-category/<int:category_id>', views.edit_category, name='edit_category'),

    path('product/<int:product_id>/add-variant/', views.AddVariant.as_view(), name='add_variant'),
    path('product/<int:product_id>/all-variants/', views.ListVariants.as_view(), name='all_variant'),


    path('shopby-category/<int:category_id>', views.shop_category, name='shop_by_category'),
    path('shopby-product/<int:product_id>,<int:variant_id>', views.shop_product, name='shop_by_product'),
    
    path('get-variant-details', views.get_variant_details, name='get-variant-details'),
    path('Orders', views.orders, name='orders'),
    path('change-order-status', views.change_order_status, name='change_order_status'),
    path('coupon-list', views.coupon_list, name='coupon_list'),
    path('add-coupon', views.add_coupon, name='add_coupon'),
    path('edit-coupon/<int:coupon_id>', views.edit_coupon, name='edit_coupon'),
    path('view-order/<int:order_id>', views.view_order, name='view_order'),
    path('update-order-status/<int:item_id>/<str:status>/', views.update_order_status, name='update_order_status'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),






]

