from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils import timezone,datetime_safe
from django.views.decorators.cache import never_cache
from custom_adminapp.models import Brand,Product,Category
from custom_adminapp.models import Variant
from cartapp.models import Cart, CartItem ,Product
from cartapp.views import _cart_id
from orderapp.models import Order,OrderProduct ,Profile
from cartapp.models import Wishlist 
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from orderapp.models import Wallet
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from decimal import Decimal
from django.db.models import Q


@never_cache
def user_registration(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        try:
            user = CustomUser.objects.get(email=email)
            messages.error(request, 'An account with this email already exists.')
            return redirect('registration')
        except CustomUser.DoesNotExist:
            pass
        
        if password1 != password2:
            messages.error(request, "Password mismatch.")
            return redirect('registration')

        otp = ''.join(random.choices('0123456789', k=6))
        user = CustomUser.objects.create_user(email=email, password=password1, first_name=first_name, phone_number=phone_number, otp=otp, is_active=False) 
            
        send_mail('Email Verification', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email], fail_silently=False)
        request.session['otp_created_at'] = timezone.now().isoformat()
        return redirect('verify_otp')
    return render(request, 'user/user_register.html')


@never_cache
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        
        try:
            user = CustomUser.objects.get( otp=otp)
            otp_created_at_str = request.session.get('otp_created_at')

            if otp_created_at_str is None:
                return redirect('verify_otp')
            otp_created_at = datetime_safe.datetime.fromisoformat(otp_created_at_str)
            current_time = timezone.now()
            if (current_time - otp_created_at).total_seconds() > 300:
                error_message = 'OTP has expired. Please request a new OTP.'
                return render(request, 'authentication/verify_otp.html', {'error_message': error_message})
            user.is_active = True
            user.save()
            customers = CustomUser.objects.all()
            wallet = Wallet.objects.create(user = user)
            wallet.save()
            request.session.pop('otp_created_at')
            return redirect('userlogin')
        except CustomUser.DoesNotExist:
            return redirect('verify_otp')
    
    return render(request, 'user/user_verify_otp.html')

@never_cache
def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id =_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            login(request, user)
            return redirect(home_page)
        messages.success(request, "Invalid email or password")
        return redirect('userlogin')

    return render(request, 'user/user_login.html')


@login_required
@never_cache
def user_logout(request):
    logout(request)
    return redirect(home_page)



def shop_page(request):
    category = Category.objects.filter(category_status=True).order_by('id')
    
    if request.method == "POST":
        selected_category = []
        if 'all_category' in request.POST:
            selected_category.extend([str(cat.id) for cat in category])
        for cat in category:
            if f'category_name_{cat.id}' in request.POST:
                selected_category.append(request.POST[f'category_name_{cat.id}'])
        
        sort_by = request.POST.get('sort_by')
        min_price = request.POST.get('minValue')
        max_price = request.POST.get('maxValue')

        min_price = float(min_price) if min_price is not None and min_price != '' else 0
        max_price = float(max_price) if max_price is not None and max_price != '' else Decimal('999999')

        products = Product.objects.filter(product_category__id__in=selected_category)
        variants = Variant.objects.filter(product__in=products, offer_price__gte=min_price, offer_price__lte=max_price)
        
        if sort_by == 'low_to_high':
            variants = variants.order_by('offer_price')
        elif sort_by == 'high_to_low':
            variants = variants.order_by('-offer_price')
        v_count = variants.count()

        paginator = Paginator(variants, 9)
        page = request.GET.get('page')
        paged_variants = paginator.get_page(page)

        context = {
            "variants": paged_variants,
            "category": category,
            "v_count":v_count,
        }
        return render(request, "user/user_shop.html", context)
    else:
        variants = Variant.objects.all().order_by('id')
        var_count = variants.count()
        paginator = Paginator(variants, 9)
        page = request.GET.get('page')
        paged_variants = paginator.get_page(page)

        context = {
            "variants": paged_variants,
            "var_count": var_count,
            "category": category,
        }

        return render(request, "user/user_shop.html", context)



# def shop_page(request):
#     variants = Variant.objects.all().order_by('id')
#     var_count =variants.count()
#     paginator = Paginator(variants,9)
#     page = request.GET.get('page')
#     paged_product = paginator.get_page(page)
#     categor = Category.objects.filter(category_status=True).order_by('id')

#     if request.method == "POST":
#         category = Category.objects.all
#         selected_category = []

#         if 'all_category' in request.POST:

#             selected_category.extend([str(cat.id) for cat in category])
#         for cat in category:
#             if f'category_name_{ cat.id }' in request.POST:
#                 selected_category.append(request.POST[f'category_name_{ cat.id }' ])

#         min_price = request.POST.get('minValue', None)
#         max_price = request.POST.get('maxValue', None)

#         products = Product.objects.filter(category__id__in=selected_category)
#         variants=[]
#         for p in products:
#             variants.extend( Variant.objects.filter(product = p, mrp__gte=min_price, mrp__lte=max_price))
#         context= {
#             "variants":variants,
#             "category":category,
#             "categor":categor,
#         }
#         return render(request,"user/user_shop.html",context)
#     return render(request,"user/user_shop.html")
    


@never_cache
def home_page(request):
    products = Product.objects.all()
    category = Category.objects.all()
    return render(request,"user/user_home.html",{"product":products ,"categories":category})
   
   


@never_cache
def user_welcome(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('adminhome')
    return render(request,"user/user_welcome.html") 

  
@login_required(login_url='userlogin')
@never_cache
def user_profile(request):
        if request.user.is_authenticated and not request.user.is_superuser :
           
            orders =  Order.objects.filter(user = request.user)
            order_products =[]
            for o in orders:
                order_products.extend(OrderProduct.objects.filter(order_no=o))  # Append to the list
            wishlist = Wishlist.objects.filter(user = request.user)
            profile_address = Profile.objects.filter(user = request.user)
            try:
                user_wallet = Wallet.objects.get(user =request.user)
            except :
                user_wallet = Wallet.objects.create(user =request.user)
            return render(request, 'user/user_profile/user_profile.html', {
                'orders': orders,
                'order_products': order_products,
                'wishlist': wishlist,
                "profile_address_all":profile_address,
                "user_wallet":user_wallet, 
            })
        else:
            return redirect('userlogin') 
       
    

        

# def add_address(request):
#     user = request.user
#     if request.method == 'POST':
#         print ('sdhgsvadhg')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         phone = request.POST.get('phone')
#         address_line1 = request.POST.get('address_line1')
#         address_line2 = request.POST.get('address_line2')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         country = request.POST.get('country')
#         postcode = request.POST.get('postcode')


#         profile_address = Profile(user=user)
#         profile_address.first_name=first_name
#         profile_address.last_name=last_name
#         profile_address.phone =phone
#         profile_address.address_line1=address_line1
#         profile_address.address_line2 = address_line2
#         profile_address.city = city
#         profile_address.state = state
#         profile_address.country = country
#         profile_address.postcode= postcode
#         profile_address.save()
#         return redirect('user_profile')

def add_address(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postcode = request.POST.get('postcode')
        profile_photo = request.POST.get('photo')
           

        profile_address = Profile(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email= email,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            country=country,
            postcode=postcode,
            profile_image = profile_photo,
        )
        profile_address.save()
        return redirect('user_profile')
    

from django.shortcuts import get_object_or_404

def edit_address(request):
    user = request.user
    address_id = request.POST.get('address.id')
    print(address_id)
    
    print(address_id)
    profile_address = get_object_or_404(Profile, user=user, id=address_id)
    if address_id:
        try:
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                address_line1 = request.POST.get('address_line1')
                address_line2 = request.POST.get('address_line2')
                city = request.POST.get('city')
                state = request.POST.get('state')
                country = request.POST.get('country')
                postcode = request.POST.get('postcode')

                profile_address.first_name = first_name
                profile_address.last_name = last_name
                profile_address.phone = phone
                profile_address.email = email
                profile_address.address_line1 = address_line1
                profile_address.address_line2 = address_line2
                profile_address.city = city
                profile_address.state = state
                profile_address.country = country
                profile_address.postcode = postcode
                profile_address.save()
        except (ValueError, Profile.DoesNotExist):
            pass


    return redirect('user_profile')


# def edit_address(request):
#     user = request.user
#     address_id = request.POST.get('address_id')
   
#     print(address_id)
#     profile_address = Profile(user=user,id=address_id)
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         address_line1 = request.POST.get('address_line1')
#         address_line2 = request.POST.get('address_line2')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         country = request.POST.get('country')
#         postcode = request.POST.get('postcode')


        
#         profile_address.first_name=first_name
#         profile_address.last_name=last_name
#         profile_address.phone =phone
#         profile_address.email =email
#         profile_address.address_line1=address_line1
#         profile_address.address_line2 = address_line2
#         profile_address.city = city
#         profile_address.state = state
#         profile_address.country = country
#         profile_address.postcode= postcode
#         profile_address.save()
#         return redirect('user_profile')



def delete_address(request):
    user = request.user
    address_id = request.POST.get('address_id')

    if address_id:
        try:
            address_id = int(address_id)
            profile_address = get_object_or_404(Profile, id=address_id, user=user)
            profile_address.delete()
        except (ValueError, Profile.DoesNotExist):
            pass

    return redirect('user_profile')



@login_required(login_url='userlogin')
@never_cache
def user_profile_orders(request):
        if request.user.is_authenticated and not request.user.is_superuser :
            orders =  Order.objects.filter(user = request.user).order_by('-order_created_date')
            wallet = Wallet.objects.get(user =request.user)
            order_items = OrderProduct.objects.all()
           
            order_products =[]
            for o in orders:
                order_products.extend(OrderProduct.objects.filter(order_no=o)) 
            return render(request, "user/user_profile/user_profile_order.html", {
                'orders': orders,
                'order_products': order_products,
                'order_items':order_items,
                
                
            })
        else:
            # Handle the case when the user is not authenticated or is a superuser
            return redirect('user_login')  

@never_cache
# def user_profile_orders(request):
#     if request.user.is_authenticated and not request.user.is_superuser:
#         orders = Order.objects.filter(user=request.user)
#         for order in orders:
#             order_products = order.orderproduct_set.all()

#         return render(request, "user/user_profile_order.html", {
#             'orders': orders,
#             'order_products': order_products,
#         })
#     else:
#         return redirect('user_login')



@login_required(login_url='userlogin')
def user_profile_order_page_view(request ,order_id):
    print(order_id,"order_id")
    order_items = OrderProduct.objects.filter(order_no__order_number = order_id )
    
    order = Order.objects.get(order_number = order_id)
    total_mrp =0
    discount =0
    offer_price =0
    shipping =0

    for i in order_items:
        total_mrp += i.varaiant.mrp * i.quantity
        discount += i.varaiant.discount * i.quantity
        offer_price += i.varaiant.offer_price * i.quantity
    if total_mrp > 10000:
        shipping =0
    else:
        shipping =50


    context ={
        "order_items":order_items,
        "order": order,
        "total_mrp":total_mrp,
        "offer_price":offer_price,
        "discount":discount,
        "shipping":shipping,

    }
    return render(request, "user/user_profile/user_order_page_view.html", context)



def wallet(request):
    if request.user.is_authenticated:
        try:
            wallet = Wallet.objects.filter(user= request.user)
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user = request.user)
        return redirect(request,"user_wallet.html",{"wallet":wallet})
    else:
        return redirect('user_login')    
    
        

@login_required(login_url='userlogin')
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(order_number=order_id)
        order_products = OrderProduct.objects.filter(order_no = order)
    
        if order.order_status == 'Pending':
            order.order_status = 'Cancelled'
            order.save()
    
            if order.order_status == 'Cancelled':
                for order_product in order_products:
                    order_product.product_status = "Cancelled"
                    order_product.save()

            if order.order_status =='Cancelled' and order.payment_mode == 'Razorpay':
                user = order.user
                try:
                   wallet_amount = Wallet.objects.get(user_id = user)
                except:
                    wallet_amount = Wallet.objects.create(user_id = user)
                wallet_amount.balance += order.order_total_amount
                wallet_amount.save()
            else:
                pass
            messages.success(request, 'Order has been cancelled successfully.')
        else:
            messages.warning(request, 'Order cannot be cancelled.')

    except Order.DoesNotExist:
        messages.error(request, 'Order does not exist.')

    return redirect('user_profile_orders')



def return_order(request, order_id):
    try:
        product = OrderProduct.filter(order_no = order_id)
        order = Order.objects.get(pk=order_id)
        if order.order_status == 'Delivered':
            order.order_status = 'Returned'
            order.save()
            messages.success(request, 'Order has been returned successfully.')
        

        
        else:
            messages.warning(request, 'Order cannot be returned.')
    except Order.DoesNotExist:
        messages.error(request, 'Order does not exist.')

    return redirect('user_profile_orders')



# @login_required(login_url='userlogin')
# def cancel_product(request,order_id):
#     print(order_id)
#     user = request.user

#     try:
#         order_product =OrderProduct.objects.get(id = order_id)
#         print(order_product,"THIS IS THE ORDER PRODUCT OF ORDER")
#         order = order_product.order_no
#         related_order_products = order.orderproduct.all()
#         order_products_count = order.orderproduct.count()


#         print(order,"ORDER DETAILS")
#         order_products = OrderProduct.objects.filter( order_no = order_id )
#         print(order_products,"TO GET THE TOATOL PRODUCT IN A ORDET")
#         if order_product.product_status == "Pending":
#             if order_product.order_no.orderproduct_set.count()==1:
#                 print("hello00000000000000000000000000000000000000000000000000000")
#                 order.order_status = "Cancelled"
#                 order.save()
#             else:
#                 for order_product in order.orderproduct_set.all():
#                     print(order_product,"EACH PRODUCT IN ORDER PRODUCTS")
#                     if order_product.product_status != "Cancelled":
#                         order.order_status = "Pending"
#                         order.save()
#                         break
#                     else:
#                         order.order_status = "Cancelled"
#                         order.save()


#                         order.save()
#                         print(order.order_status,"THIS IS ORDER STATUS AFTER CONDITION CHECKIMG")

#             order_product.product_status = "Cancelled"
#             order_product.save()
#             messages.success(request, 'Product has been cancelled successfully.')

#             if order_product.product_status =='Cancelled' and order_product.order_no.payment_mode == 'Razorpay':
#                 try:
#                     wallet_amount = Wallet.objects.get(user_id = user)
#                 except:
#                     wallet_amount = Wallet.objects.create(user_id = user)
#                 order_product_amount_decimal = Decimal(str(order_product.amount))
#                 wallet_amount.balance = (wallet_amount.balance + order_product_amount_decimal)
#                 wallet_amount.save()
#         else:
#             messages.warning(request, 'Product cannot be cancelled.')
#     except OrderProduct.DoesNotExist:
#         messages.error(request, 'Product does not exist.')
#     return redirect('user_profile_orders')


@login_required(login_url='userlogin')
def cancel_product(request, order_id):
    print(order_id)
    user = request.user

    try:
        order_product = OrderProduct.objects.get(id=order_id)
        print(order_product, "THIS IS THE ORDER PRODUCT OF ORDER")
        order = order_product.order_no
      
       

        print(order, "ORDER DETAILS")
        order_products = OrderProduct.objects.filter(order_no=order_id)
        print(order_products, "TO GET THE TOTAL PRODUCT IN AN ORDER")

        if order_product.product_status == "Pending":
            if order.orderproduct.count() == 1:
                print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
                order.order_status = "Cancelled"
            else:
                print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
                for order_product in order.orderproduct.all():
                    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
                    print(order_product, "EACH PRODUCT IN ORDER PRODUCTS")
                    if order_product.product_status != "Cancelled":
                        print(order_product.product_status,"eeeeeeeeeeeeee")
                        order.order_status = "Pending"
                        break
                    else:
                        order.order_status = "Cancelled"

                order.save()
                print(order.order_status)

            order_product.product_status = "Cancelled"
            order_product.save()
            messages.success(request, 'Product has been cancelled successfully.')

            if order_product.product_status == 'Cancelled' and order_product.order_no.payment_mode == 'Razorpay':
                try:
                    wallet_amount = Wallet.objects.get(user_id=user)
                except Wallet.DoesNotExist:
                    wallet_amount = Wallet.objects.create(user_id=user)

                order_product_amount_decimal = Decimal(str(order_product.amount))
                wallet_amount.balance = (wallet_amount.balance + order_product_amount_decimal)
                wallet_amount.save()
        else:
            messages.warning(request, 'Product cannot be cancelled.')
    except OrderProduct.DoesNotExist:
        messages.error(request, 'Product does not exist.')
    return redirect('user_profile_orders')



def return_product(request,order_id):
    user = request.user
    try:
        order_product = OrderProduct.objects.get(id = order_id)
        if order_product.product_status == "Delivered":
            order_product.product_status = "Returned"
            order_product.save()
            if order_product.product_status =="Returned" and order_product.order_no.payment_mode =="Razorpay":
                try:
                    wallet_amount = Wallet.objects.get(user_id = user)
                except:
                    wallet_amount = Wallet.objects.create(user_id = user)
                wallet_amount.balance = (wallet_amount.balance + order_product.amount)
                wallet_amount.save()
            messages.success(request, 'Product has been Returned successfully.')
        else:
            messages.warning(request, 'Product cannot be Returned.')
    except OrderProduct.DoesNotExist:
        messages.error(request, 'Product does not exist.')

    return redirect('user_profile_orders')








def get_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order_no=order)

    order_details = {
        'order_id': order_id,
        'order_number': order.order_number,
        'user_first_name': order.user.first_name, 
        'user_last_name': order.user.last_name,   
        'user_phone': order.phone,
        'user_email': order.email,
        'address_line1': order.address_line1,
        'address_line2': order.address_line2,
        'country': order.country,
        'state': order.state,
        'city': order.city,
        'postcode': order.postcode,
        'order_note': order.order_note,
        'order_total_amount': str(order.order_total_amount),  
        'order_status': order.get_order_status_display(),     
        'order_created_date': order.order_created_date.strftime('%Y-%m-%d %H:%M:%S'),  
        'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S'),  
        'payment_mode': order.payment_mode,
        'payment_id': order.payment_id,
        'order_products': [{
            'product_id': product.product.id,
            'product_name': product.product.product_name,
            'variant_id': product.varaiant.id,
            'variant_name': product.varaiant.variant_name,
            'quantity': product.quantity,
            'amount': str(product.amount),  # Convert FloatField to string
            'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the datetime as string
            'updated_at': product.updated_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the datetime as string
        } for product in order_products],
    }
    return JsonResponse(order_details)



def search(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        variant = Variant.objects.order_by('id').filter(
            Q(variant_description__icontains=keyword) | Q(variant_name=keyword)
        )
        paginator = Paginator(variant, 6)
        page_number = request.GET.get('page')
        variants = paginator.get_page(page_number)

        context = {
            "variants": variants,
            "keyword": keyword,
        }
        return render(request, "user/user_shop.html", context)
    return render(shop_page)


def reset_password_page(request):
    if request.user.is_authenticated and not request.user.is_superuser :
        return render(request,"user/user_reset_pass.html")


def reset_password(request):
    if request.user.is_authenticated and not request.user.is_superuser :
        if request.method == "POST":
            old_pass = request.POST.get('old_password')
            new_pass = request.POST.get('new_password')
            user = authenticate(email = request.user.email, password = old_pass)
            if user is not None:
                user.set_password(new_pass)
                user.save()
                messages.success(request, 'Your password has been changed successfully.')
            else:
                messages.error(request, "Password Mismatch.")
        return render(request,"user/user_reset_pass.html")
    else:
        return render(request,"user/user_reset_pass.html")

        
        


  


    

        
    
            

      
    




            










        
        
    
        
      





