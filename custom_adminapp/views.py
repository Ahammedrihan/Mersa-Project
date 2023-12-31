from django.shortcuts import render ,redirect ,get_object_or_404
from django.shortcuts import render ,redirect
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accountapp.models import CustomUser
from custom_adminapp.models import Brand,Product,Category
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from cartapp.models import Cart ,CartItem , Coupon ,UserCoupon
from cartapp.views import _cart_id
from orderapp.models import Order,OrderProduct
from django.urls import reverse_lazy
from custom_adminapp.forms import VariantForm
from custom_adminapp.models import Variant ,VariantImage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import functions
from django.db.models import Count
from datetime import datetime, timedelta
from orderapp.models import Order
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Variant
from django.db.models import Sum


@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('adminhome')
    if request.method == 'POST':
        email= request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('adminhome')
            else:
                return redirect('adminlogin')
        else:
            return redirect('adminlogin')
    return render(request,"admin/admin_login.html")


@never_cache
def admin_signout(request):
    if request.user.is_superuser:
        logout(request)
        return redirect('adminlogin')
    
    
    
@login_required(login_url='adminlogin')
@never_cache
def admin_home(request):
    if request.user.is_superuser:
        return render(request,'admin/admin_home.html')
    else:
        return redirect('adminlogin')
    

@login_required(login_url='adminlogin')
@never_cache
def users_details(request):
    if request.user.is_superuser:
        data = CustomUser.objects.all().order_by('-id')
        user_count = data.count()
        paginator = Paginator(data,10)
        page = request.GET.get('page')
        paged_order = paginator.get_page(page)
        context ={"data":paged_order}
        return render(request,"admin/user_details.html",context)
    else:
        return redirect('adminlogin')


@login_required(login_url='adminlogin')
@never_cache
def user_block(request,id):
    if request.user.is_superuser:
        if request.method=='POST':
            user =CustomUser.objects.get(pk=id)
            user.is_active = False
            user.save()
            return redirect('userdetails')
    else:
        return redirect('adminlogin')
    

@login_required(login_url='adminlogin')
@never_cache
def user_un_block(request,id):
    if request.user.is_superuser:
        if request.method=='POST':
            user =CustomUser.objects.get(pk=id)
            user.is_active = True
            user.save()
            return redirect('userdetails')
    else:
        return redirect('adminlogin')
    

@login_required(login_url='adminlogin')
@never_cache
def brandlist(request):
    if request.user.is_superuser:
        brand = Brand.objects.all().order_by('id')
        return render(request,"admin/brand.html",{"brand":brand})
    else:
        return redirect('adminlogin')
    
    
@login_required(login_url='adminlogin')
@never_cache
def categorylist(request):
    if request.user.is_superuser:
        category = Category.objects.all().order_by('id')
        return render(request,"admin/category.html",{"category":category})
    else:
        return redirect('adminlogin')
    

 
@login_required(login_url='adminlogin')
@never_cache
def productlist(request):
    if request.user.is_superuser:
        product = Product.objects.all().order_by('id')
        brands = Brand.objects.all()
        category = Category.objects.all()
        return render(request,"admin/product.html",{"product":product,'brands':brands,"categorys":category })
    else:
        return redirect('adminlogin')


@login_required(login_url='adminlogin')
@never_cache
def add_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            category_name = request.POST.get('category_name')
            category_image = request.FILES.get('category_image')
            category_status = request.POST.get('category_status')
            status = bool(category_status)
            category = Category(category_name=category_name,category_status=status,category_image=category_image)
            category.save()
            return redirect('category')
        return render(request, 'admin/category.html')
    else:
        return redirect('adminlogin')

@login_required(login_url='adminlogin')
@never_cache
def add_brand( request):
    if request.user.is_superuser:
        if request.method =='POST':
            new_brand = request.POST.get('brand_name')
            brand_status = request.POST.get('brand_status')
            status = bool(brand_status)
            brand = Brand(brand_name =new_brand, brand_status= status)
            brand.save()
            return redirect('brand')
        return render(request, 'admin/brand.html')
    else:
        return redirect('adminlogin')

 
@login_required(login_url='adminlogin')
@never_cache 
def add_product(request):
    if request.user.is_superuser:
        if request.method =='POST':
            product_name = request.POST.get('product_name')
            category = request.POST.get('product_category')
            brand= request.POST.get('product_brand')
            product_description = request.POST.get('product_description')
            product_image = request.FILES.get('product_image')
            product_status = request.POST.get('product_status', False) == 'true'
            product_brand = Brand.objects.get(id=brand)
            product_category =Category.objects.get(id =category)
            product = Product(product_name = product_name,product_category=product_category,product_brand=product_brand,
                    product_description=product_description,product_image =product_image
                    ,product_status=product_status)
            product.save()
            return redirect('product')
        return render(request,'admin/product.html')
    else:
        return redirect('adminlogin')
    
 
@login_required(login_url='adminlogin')
@never_cache
def edit_product(request,product_id):
    if request.user.is_superuser:
        if request.method=='POST':
            edited_product_name = request.POST.get('product_name')
            sub_edited_category =request.POST.get('product_category')
            sub_edited_brand =request.POST.get('product_brand')
            edited_product_description =request.POST.get('product_description')
            edited_product_image =request.FILES.get('product_image')
            edited_category =Category.objects.get(id=sub_edited_category)
            edited_brand = Brand.objects.get(id=sub_edited_brand)
            edit = Product.objects.get(id=product_id)
            edit.product_name = edited_product_name
            edit.product_image = edited_product_image
            edit.product_brand =edited_brand
            edit.product_category = edited_category
            edit.product_description = edited_product_description
            edit.save()
            return redirect('product')
        return render(request,"admin/product.html")
    else:
        return redirect('adminlogin')

 
@login_required(login_url='adminlogin')
@never_cache
def edit_brand(request,brand_id):
    if request.user.is_superuser:
        if request.method=="POST":
            edit_brand_name = request.POST.get('editbrand_name')
            edit_brand_status = request.POST.get('editbrand_status')
            edit = Brand.objects.get(id=brand_id)
            edit.brand_name = edit_brand_name
            edit.brand_status = True if edit_brand_status == 'on' else False
            edit.save()
            return redirect('brand')
        return render(request,'admin/brand.html')
    else:
        return redirect('adminlogin')


@login_required(login_url='adminlogin')
@never_cache
def edit_category(request,category_id):
    if request.user.is_superuser:
        if request.method=="POST":
            edit_category_name = request.POST.get('editcategory_name')
            edit_category_image = request.FILES.get('editcategory_image')
            edit_category_status = request.POST.get('editcategory_status')
            edit = Category.objects.get(id=category_id)
            edit.category_name = edit_category_name
            edit.category_image =edit_category_image
            edit.category_status = True if edit_category_status == 'on' else False
            edit.save()
            return redirect('category')
        return render(request,'admin/category.html')
    else:
        return redirect('adminlogin')


class AddVariant(FormView):
    model = Variant ,VariantImage
    form_class = VariantForm
    template_name = 'admin/add-variant.html'
    success_url = reverse_lazy('product') #The form submission is considered valid, and the user is redirected to the success URL.



    def form_valid(self, form):    # When the form is submitted, form_valid() is called.
        obj = form.save()          # The form.save() method saves the form data to the database and returns the created Variant object.
        obj.product_id = self.kwargs.get('product_id') #self.kwargs.get('product_id') is used to retrieve the value of the product_id parameter from the URL. The self.kwargs is a dictionary-like object that contains all the captured URL parameters.
        #So, when the form is submitted, the product_id value from the URL is retrieved using self.kwargs.get('product_id'). Then, this value is assigned to the product_id field of the Variant object (obj) before saving it to the database.
        obj.save()  #The obj.save() method is called to update the product_id value in the database.
        image1 = self.request.FILES.get('image1')
        image2 = self.request.FILES.get('image2')
        image3 = self.request.FILES.get('image3')

        VariantImage.objects.create(variant=obj, image1=image1, image2=image2, image3=image3)

        return super().form_valid(form)
   

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(id=self.kwargs.get('product_id'))
        context['product'] = product
        return context

# from django.urls import reverse
# def edit_variant(request, variant_id):
#     variant = Variant.objects.get(id=variant_id)
#     product_id = variant.product.id  

#     if request.method == 'POST':
#         variant.variant_name = request.POST.get('name')
#         variant.mrp = request.POST.get('mrp')
#         variant.discount = request.POST.get('discount')
#         variant.offer_price = request.POST.get('offer_price')
#         variant.variant_status = request.POST.get('variant_status')
#         variant.variant_stock = request.POST.get('variant_stock')
#         variant.save()
#         image1 = request.FILES.get('image1')
#         image2 = request.FILES.get('image2')
#         image3 = request.FILES.get('image3')
#         variant_image, created = VariantImage.objects.get_or_create(variant=variant)
#         variant_image.image1 = image1 or variant_image.image1
#         variant_image.image2 = image2 or variant_image.image2
#         variant_image.image3 = image3 or variant_image.image3
#         variant_image.save()

#         return redirect(reverse('product', args=[product_id]))

#     else:
#         context = {'variant': variant}
#         return render(request, 'admin/edit-variant.html', context)




class ListVariants(ListView):
    model = Variant ,VariantImage
    template_name = 'admin/all-variants.html'
    context_object_name = 'variants'

    def get_queryset(self):
        queryset = Variant.objects.filter(product_id=self.kwargs.get('product_id')).order_by('id')
        return queryset
    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['product_id'] = self.kwargs.get('product_id')
        product = Product.objects.get(id=self.kwargs.get('product_id'))
        context['product'] = product
        return context










def shop_product(request, product_id, variant_id):
    product = Product.objects.get(id=product_id)
    variant = Variant.objects.get(id=variant_id)
    variants = Variant.objects.filter(product=product).order_by('mrp')
    variant_images = VariantImage.objects.filter(variant=variant)
    try :
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(user = request.user,variant =variant)
        else:
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), variant=variant).exists()
    except:
        pass

    context = {
        'product': product,
        'variant': variant,
        'variant_images': variant_images,
        'variants': variants,
        'in_cart': in_cart,
    }
    return render(request, 'user/user_shopby_product.html', context)

  



@require_GET
def get_variant_details(request):
    
    variant_id = request.GET.get('variantId')
    try:
        variant = Variant.objects.select_related('product').prefetch_related('images').get(id=variant_id)
        variant_data = {
            'product_image': variant.images.first().image1.url,
            'product_price': variant.offer_price,
            'product_name': variant.product.product_name,
            'variant_description': variant.variant_description,
            'variant_name': variant.variant_name,
            'variant_stock': variant.variant_stock,
            'variant_status': variant.variant_status,
            # Include other variant details as needed
        }
        return JsonResponse(variant_data)
    except Variant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)









def orders(request):
    orders = Order.objects.all().order_by('-order_created_date')
    order_count = orders.count()
    paginator = Paginator(orders,6)
    page = request.GET.get('page')
    paged_order = paginator.get_page(page)
    order_items = OrderProduct.objects.filter()
    order_status = OrderProduct.STATUS
    return render(request,"admin/admin_orders.html",{"orders":paged_order,"order_items":order_items,"choices":order_status,"order_count":order_count})




@login_required(login_url='adminlogin')
def change_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_item_id')
        order_status_update = request.POST.get('order_status')
        order = Order.objects.get(id = order_id ) 
        order.order_status = order_status_update
        order.save()
        return redirect('orders')    
    else:   
       return render(request,"admin/admin_orders.html")



def shop_category(request,category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(product_category=category)
    product_count = products.count()
    products_variants={}

    try:
        for product in products:
            variants = Variant.objects.filter(product = product).order_by('mrp')
            products_variants[product]=variants[0]
        for product,variant in products_variants.items():
            print(product,variant) 
       
        context ={
        'products_variants': products_variants,
        'product_count':product_count,
        }
        return render(request, 'user/user_shopby_category.html',context)
    except:
        messages.error(request, 'Product currently unavailable does not exist.')
        return render(request, 'user/user_shopby_category.html')

        
     

   


@login_required(login_url='adminlogin')
def coupon_list(request):
    coupons = Coupon.objects.all()
    coupon_DISCOUNT_TYPES = Coupon.DISCOUNT_TYPES
    category = Category.objects.all()
    context={
        "coupons": coupons,
        "discount_types": coupon_DISCOUNT_TYPES,
        "category":category,
    }
    return render(request,"admin/admin_coupon_manage.html",context)



@login_required(login_url='adminlogin')
def add_coupon(request):
    if request.method == "POST":
        
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')

        coupon_description = request.POST.get('coupon_description')
        coupon_discount_type = request.POST.get('coupon_discount_type')
        coupon_discount = request.POST.get('discount')
        coupon_start_date = request.POST.get('start_date')
        coupon_end_date = request.POST.get('end_date')
        coupon_is_active = request.POST.get('is_active')
        coupon_applicable_type = request.POST.get('applicable_type')
        coupon_category_id = request.POST.get('category')
        coupon_min_amount = request.POST.get('min_amount')
        coupon_max_amount = request.POST.get('max_amount')

        
        coupon = Coupon(
            name=coupon_name,
            code =  coupon_code,
            description=coupon_description,
            discount_type=coupon_discount_type,
            discount=coupon_discount,
            start_date=coupon_start_date,
            end_date=coupon_end_date,
            is_active=bool(coupon_is_active),  # Convert 'true'/'false' to boolean. in  Django's bool() function can be used to convert the string 'true' to the boolean value True and the string 'false' to the boolean value False.
            applicable_type=coupon_applicable_type,
            category_id=coupon_category_id,  # Assign the category ID to the foreign key
            min_purchase=coupon_min_amount,
            max_amount =coupon_max_amount
        )
        coupon.save()
        return redirect('coupon_list')
    return render(request, "admin/admin_coupon_manage.html")

@login_required(login_url='adminlogin')
def edit_coupon(request, coupon_id):
    if request.method == "POST":
        edit_coupon_name = request.POST.get('coupon_name')
        edit_coupon_code = request.POST.get('coupon_code')
        edit_coupon_description = request.POST.get('coupon_description')
        edit_coupon_discount_type = request.POST.get('coupon_discount_type')
        edit_coupon_discount = request.POST.get('discount')
        edit_coupon_start_date = request.POST.get('start_date')
        edit_coupon_end_date = request.POST.get('end_date')
        edit_coupon_is_active = request.POST.get('is_active')
        edit_coupon_applicable_type = request.POST.get('applicable_type')
        edit_coupon_category_id = request.POST.get('category')
        edit_coupon_min_amount = request.POST.get('min_amount')
        edit_coupon_max_amount = request.POST.get('max_amount')

        coupon = Coupon.objects.get(id=coupon_id)

        coupon.name = edit_coupon_name
        coupon.code = edit_coupon_code
        coupon.description = edit_coupon_description
        coupon.discount_type = edit_coupon_discount_type
        coupon.discount = edit_coupon_discount
        coupon.start_date = edit_coupon_start_date
        coupon.end_date = edit_coupon_end_date
        coupon.is_active = bool(edit_coupon_is_active)  # Convert 'true'/'false' to boolean.
        coupon.applicable_type = edit_coupon_applicable_type
        coupon.category_id = edit_coupon_category_id
        coupon.min_purchase = edit_coupon_min_amount
        coupon.max_amount = edit_coupon_max_amount
        coupon.save()
        return redirect('coupon_list')
    return render(request, "admin/admin_coupon_manage.html")


@login_required(login_url='adminlogin')
def view_coupon(request):
    coupon_view = Coupon.objects.all()
    return render(request, "admin/admin_coupon_manage.html")


@login_required(login_url='adminlogin')
def view_order(request,order_id):
    order = Order.objects.get(id = order_id) 
    order_items = OrderProduct.objects.filter(order_no = order)
    context ={
        "order":order,
        "order_items":order_items,
    }
    return render(request,"admin/admin_view_orders.html",context)


@login_required(login_url='adminlogin')
def update_order_status(request,item_id,status):
    order_item = OrderProduct.objects.get(id = item_id)
    if status =='Cancelled':
        variant = Variant.objects.get(id = order_item.varaiant.id)
        variant.variant_stock += 1
        order_item.product_status ="Cancelled"
        order_item.save()
    elif status =='Pending':
        order_item.product_status ='Confirmed'
        order_item.save()
    elif status =='Confirmed':
        order_item.product_status ='Out for Shipping'
        order_item.save()
    elif status =='Out for Shipping':
        order_item.product_status ='Out for Delivery'
        order_item.save()
    elif status =='Out for Delivery':
        order_item.product_status ='Delivered'
        order_item.save()
    else:
        pass
    return redirect('orders')



@login_required(login_url='adminlogin')
def admin_dashboard(request):
    
    daily_total_revenue = 0
    weekly_total_revenue = 0
    monthly_total_revenue = 0
    total_revenue = 0
    per_day_total_order_count=0
    per_day_total_product_count=0

    variants = Variant.objects.filter(variant_status=True)
    low_stock = [variant for variant in variants if variant.variant_stock <= 5]
    today_date = datetime.now()
    week_start_date = today_date - timedelta(days=today_date.weekday())
    week_end_date = week_start_date + timedelta(days=6)
    month_start_date = today_date.replace(day=1)
    month_end_date = month_start_date.replace(day=28) + timedelta(days=4)
    
    total_revenue = Order.objects.filter(order_created_date__date=today_date).aggregate(total_revenue=Sum('order_total_amount'))['total_revenue']
    per_day_total_order_count = Order.objects.filter(order_created_date__date=today_date).count()
    per_day_total_product_count = OrderProduct.objects.annotate(created_date_only=models.functions.Cast('created_at', models.DateField())).filter(created_date_only=today_date).count()
    if total_revenue is None:
        daily_total_revenue = 0
    else:
        daily_total_revenue = total_revenue

    week_revenue = Order.objects.filter(order_created_date__range=(week_start_date,week_end_date )).aggregate(total_revenue=Sum('order_total_amount'))['total_revenue']
    weekly_total_order_count = Order.objects.filter(order_created_date__range=(week_start_date,week_end_date )).count()
    weekly_total__product_count = OrderProduct.objects.annotate(created_date_only=models.functions.Cast('created_at', models.DateField())).filter( created_date_only__range=(week_start_date,week_end_date )).count()
    if week_revenue is None:
        weekly_total_revenue = 0
    else:
        weekly_total_revenue = week_revenue

    daily_sales_per_day = Order.objects.filter(order_created_date__date__range=(week_start_date, week_end_date)) \
        .values('order_created_date__date').annotate(daily_sales_count=Count('id'), total_daily_sales=Sum('order_total_amount'))
    
    # [{'order_created_date__date': datetime.date(2023, 7, 27), 'daily_sales_count': 5, 'total_daily_sales': Decimal('49100.00')},
    daily_sales_labels = [day['order_created_date__date'].strftime('%a') for day in daily_sales_per_day] 
    # ['Thu', 'Fri']  finding the particular days from it 
    daily_sales_data = [day['total_daily_sales'] for day in daily_sales_per_day]#
    #[Decimal('49100.00'), Decimal('22400.00')] take the corresponding sale with dat
    total_weekly_sales = sum(daily_sales_data)
    daily_sales_counts = [day['daily_sales_count'] for day in daily_sales_per_day]


    user_payment_counts = Order.objects.filter(order_created_date__date__range=(week_start_date, week_end_date)).values('payment_mode')\
    .annotate(payment_count = Count('id'))
    payment_label = [payment['payment_mode'] for payment in user_payment_counts]
    payment_data = [payment['payment_count'] for payment in user_payment_counts]
  

    weekly_sales = Order.objects.filter(order_created_date__range=(week_start_date, today_date))
    weekly_sales_count = weekly_sales.count()
    total_weekly_sales = weekly_sales.aggregate(total_amount = Sum('order_total_amount'))['total_amount']
    weekday_names =['mon','tue','wen','thur','fri','sat','sun']

    daily_brand_sales = OrderProduct.objects.values('product__product_brand__brand_name', 'created_at').annotate(total_quantity=Sum('quantity'))

    brand_sales_per_day = {}
    for sale in daily_brand_sales:
        brand_name = sale['product__product_brand__brand_name']
        order_date = sale['created_at'].date()
        total_quantity = sale['total_quantity']

        if brand_name not in brand_sales_per_day:
            brand_sales_per_day[brand_name] = {}

        brand_sales_per_day[brand_name][order_date] = total_quantity
    
    return render(request, 'admin/admin_dashboard.html', {
        "daily_total_revenue":daily_total_revenue,
        "weekly_total_revenue":weekly_total_revenue,
        "per_day_total_order_count":per_day_total_order_count,
        "per_day_total_product_count":per_day_total_product_count,
        "weekly_total_order_count":weekly_total_order_count,
        "weekly_total__product_count":weekly_total__product_count,
        "today_date":today_date,
        "week_start_date":week_start_date,
        "week_end_date":week_end_date,

        "daily_sales_labels":daily_sales_labels,
        "daily_sales_data":daily_sales_data,
        "total_weekly_sales":total_weekly_sales,
        "daily_sales_counts":daily_sales_counts,

        "payment_label":payment_label,
        "payment_data":payment_data,


        "show_low_stock_modal":low_stock,
        "weekly_sales_count":weekly_sales_count,
        "weekly_sales":total_weekly_sales,
        "weekday_names":weekday_names,
        "brand_sales_per_day":brand_sales_per_day,
     
    })



    



