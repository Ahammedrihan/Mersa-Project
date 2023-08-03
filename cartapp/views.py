from django.shortcuts import render ,redirect , get_object_or_404
from custom_adminapp.models import Product,Variant
from .models import Cart,CartItem ,Wishlist ,Coupon ,UserCoupon 
from orderapp.models import Wallet
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from orderapp.models import Profile
from django.contrib import messages



def cart(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(cart_id = request.user, user = request.user)
            cart_items = CartItem.objects.filter(user = request.user, is_active =True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart =cart, is_active =True)
        for cart_item in cart_items:
            image1_url = cart_item.variant.images.first().image1.url 
            cart_item.variant_image_url = image1_url
        coupons = Coupon.objects.filter(is_active = True )
        context ={
        "cart_items":cart_items,
        "cart":cart,
        "coupons":coupons,
              }
    except ObjectDoesNotExist:
        pass
    return render(request,'user/user_cart.html',context)



def _cart_id(request):                   
    cart = request.session.session_key  
    if not cart:                           
        cart = request.session.create()  
    return cart



def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id = product_id)
    variant_number = request.POST.get('variant') 
    quantity = request.POST.get('quantity') 
    variant_id=Variant.objects.get(id=variant_number)

    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=current_user,user = current_user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=current_user,user =current_user)

        try:
            cart_item = CartItem.objects.get(product=product,user=current_user,variant_id=variant_id,cart = cart)
            cart_item.cart_quantity +=1 
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item =CartItem.objects.create(product =product,cart_quantity = quantity,user=current_user,variant=variant_id,cart = cart)
            cart_item.save()
        return redirect('cart')
    else:
       
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
        except Cart.DoesNotExist:
            cart = Cart.objects.create( cart_id = _cart_id(request))
        cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart = cart,variant_id=variant_id)
            cart_item.cart_quantity +=1 
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item =CartItem.objects.create(product =product,cart_quantity = quantity,cart =cart ,variant=variant_id)
            cart_item.save()
    return redirect('cart')



@never_cache
def remove_cart(request,variant_id):
    variant=get_object_or_404(Variant,id=variant_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(variant = variant,user = request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(variant = variant,cart= cart)
        if cart_item.cart_quantity > 1:
            cart_item.cart_quantity -= 1
            cart_item.save()
        elif cart_item.cart_quantity == 1:
            cart_item.delete()
    except:
        pass
    return redirect('cart')



def plus_cart(request,variant_id):
    variant=get_object_or_404(Variant,id=variant_id)
    try :
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(variant = variant,user = request.user)
            if cart_item.cart_quantity >= 1:
                cart_item.cart_quantity += 1
                cart_item.save()
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(variant = variant,cart= cart)
            if cart_item.cart_quantity >= 1:
                cart_item.cart_quantity += 1
                cart_item.save()
    except:
       pass
    return redirect('cart')


def remove_cart_button(request,variant_id):
    variant=get_object_or_404(Variant,id=variant_id)
    try :
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(variant = variant,user = request.user)
            cart_item.delete()
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(variant = variant,cart= cart)
            cart_item.delete()
    except:
        pass
    return redirect('cart')


@never_cache
@login_required(login_url='userlogin')
def checkout(request):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user_id = request.user)             
        for cart_item in cart_items:
            image1_url = cart_item.variant.images.first().image1.url 
            cart_item.variant_image_url = image1_url
    
    except:
       return redirect ('userlogin')
    
    addresses = Profile.objects.filter(user=request.user)
    cart = Cart.objects.get(cart_id =request.user)

    balance = Wallet.objects.get(user = request.user)
    cart_items = CartItem.objects.filter(user = request.user)
    context ={
    
        "cart_items":cart_items,
        "cart": cart,
        "addresses":addresses,
        "balance":balance,
        }

    return render(request,'user/user_checkout.html',context)



def change_Address(request):

    profiles = Profile.objects.all(user = request.user)
    data = []
    for profile in profiles:
        data.append({
            'id': profile.id,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone': profile.phone
        })
    return JsonResponse(data)





@login_required(login_url='userlogin')
def add_to_wishlist(request):
    if request.method == 'POST':
        variant_id = request.POST['variant_id']
        variant = Variant.objects.get(id=variant_id)
        product = variant.product 
        wishlist, created = Wishlist.objects.get_or_create(user = request.user ,product = product,variant =variant)
        if created:
            messages.success(request, 'Item added to wishlist successfully!')
    return redirect('wishlist_view')


@login_required(login_url='userlogin')
def wishlist_view(request):
    try:
        wishlists = Wishlist.objects.filter(user=request.user)
    except Wishlist.DoesNotExist:   
        wishlists = None

    context = {
        'wishlists': wishlists,
    }
    return render(request, 'user/user_wishlist.html', context)

def remove_wishlist(request,product_id):
    wishlist = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    wishlist.delete()
    return redirect('wishlist_view')






def apply_coupon(request):
  
        if request.method =="POST":
            coupon_code = request.POST.get('coupon-code')
            print(coupon_code)
            user = request.user
            try:
                coupon = Coupon.objects.get(code = coupon_code)
                print(coupon,"yryyyyyyyyyyyyyy")
            except ObjectDoesNotExist:
                messages.warning(request, "COUPON CODE DOES NOT EXIST")
                return redirect('cart')

            if not coupon.is_valid():
                messages.warning(request, "COUPON CODE IS NOT VALID")
                return redirect('cart')
        
        
            if UserCoupon.objects.filter(user = user, coupon_applied = coupon ).exists():
                messages.warning(request, "YOU HAVE ALREADY USED THIS COUPON")
                return redirect('cart')
            cart, _ = Cart.objects.get_or_create(cart_id=user)  
            if cart.get_total() <= coupon.min_purchase:
                messages.warning(request, "MINIMUM CART AMOUNT NOT MET")
                print(Cart.calculate_discount)
                return redirect('cart')
                
            
            applicable_type  = coupon.applicable_type
            if applicable_type == "all":
                cart.coupon_is_applied = coupon
                cart.is_coupon_applied = True
                cart.save()
                UserCoupon.objects.create(user=user,coupon_applied = coupon)
                messages.success(request, "COUPON APPLIED SUCCESSFULLY")
                print(Cart.calculate_discount)
                return redirect('cart')
            
            
            elif applicable_type =="category":
                category = coupon.category
                try:

                    if CartItem.objects.filter(cart=cart, product__category=category).exists():
                        cart.coupon_is_applied = coupon
                        UserCoupon.objects.create(user=user, coupon_applied=coupon)
                        messages.success(request, "COUPON APPLIED SUCCESSFULLY")

                        print(Cart.calculate_discount)
                        return redirect('cart')
                except:
                    messages.warning(request, "COUPON IS NOT APPLICABLE TO SELECTED CATEGORY")
                    return redirect('cart')

            else:
                messages.warning(request, "INVALID APPLICABLE TYPE")
                return redirect('cart')
        return redirect('cart')


        

