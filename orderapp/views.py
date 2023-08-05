from django.shortcuts import render
from cartapp.models import Cart,CartItem
from django.shortcuts import render ,redirect
from .models import Order,OrderProduct,Wallet
from .models import Order
import datetime
from custom_adminapp.models import Product,Variant
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from accountapp.models import CustomUser
from orderapp.models import Profile
from django.http import JsonResponse
from mersa_project.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET
import razorpay 


@never_cache
@login_required(login_url='userlogin')
def place_order(request):
    current_user = request.user
    cart = Cart.objects.get(cart_id = current_user)
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    try:
        balance = Wallet.objects.get(user=current_user)
    except Wallet.DoesNotExist:
        balance = 0
    
    if cart_count <= 0:
        return redirect('shop')
    
    if request.method == "POST":
        wallet=request.POST.get('wallet_modal')
    
        
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.email = request.POST.get('email')
            userprofile.address_line1 = request.POST.get('address_line1')
            userprofile.address_line2 = request.POST.get('address_line2')
            userprofile.country = request.POST.get('country')
            userprofile.state = request.POST.get('state')
            userprofile.city = request.POST.get('city')
            userprofile.postcode = request.POST.get('postcode')
            userprofile.save()
        if wallet=='true':
            if balance.balance > cart.get_total_offer_price():
                payment_amount = 0
                balance.balance = (balance.balance - cart.get_total_offer_price())
                balance.save()
            else:
                payment_amount = cart.get_total() - balance.balance
                balance.balance = 0
                balance.save()
        else:
            payment_amount = cart.get_total_offer_price()

        

        data = Order()
        data.user = current_user
        data.first_name = request.POST.get('first_name')
        data.last_name = request.POST.get('last_name')
        data.phone = request.POST.get('phone')
        data.email = request.POST.get('email')
        data.address_line1 = request.POST.get('address_line1')
        data.address_line2 = request.POST.get('address_line2')
        data.country = request.POST.get('country')
        data.state = request.POST.get('state')
        data.city = request.POST.get('city')
        data.postcode = request.POST.get('postcode')
        data.order_note = request.POST.get('order_note')

        data.order_total_amount = payment_amount
        payment_mode =request.POST.get('payment_modal2')
        data.payment_mode = payment_mode 
        data.payment_id = request.POST.get('payment_id')
        data.save()
        

        # for generating order id
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        print(order_number)
        data.save()
        neworder_items = CartItem.objects.filter(user = request.user, is_active =True)

        for item in neworder_items:
            order_product = OrderProduct.objects.create(
                        order_no = data,
                        product = item.product,
                        varaiant = item.variant,
                        amount = item.get_subtotal_offer_price(),
                        quantity = item.cart_quantity
                )
            order_product.save()
            ordervariant = Variant.objects.filter(id=item.variant_id).first()
            ordervariant.variant_stock = ordervariant.variant_stock - item.cart_quantity
            ordervariant.save()

            # to clear users cart
        CartItem.objects.filter(user = request.user).delete()

        
    return redirect('order_success',order_number)




def order_details(request):#user side
      user=request.user
      order=Order.objects.filter(user=user)
      order_items=OrderProduct.objects.filter(order_no__in=order)
      contex={
      'user':user,     
      'order':order,
      'order_items':order_items,
      }
      return render(request,'user/order_details.html',contex)


# def cancelorderitem(request):
#     if request.method == 'POST':
#         item_id = int(request.POST.get('itemId'))
#         print(type(item_id),'0000000000000000000')
#         order_item = OrderProduct.objects.get(id=item_id)
#         if order_item:
#             order_item.order_status = 'Canceled'
#             order_item.save()
#             product_size = order_item.product_size
#             product_size.Quantity += order_item.quantity
#             product_size.save()
#             return JsonResponse({'message': 'Item canceled successfully'})
#         else:
#             return JsonResponse({'error': 'Item not found'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

    
        
    #     return redirect('order_success')
    # else:
    #     return redirect('checkout')

def order_success(request,order_number):
    print(order_number,"kjggggggggggggggggggggl")
    order_items = OrderProduct.objects.filter(order_no__order_number = order_number )
    order = Order.objects.get(order_number = order_number)
    total_mrp =0
    discount =0
    offer_price =0
    shipping =0
    for i in order_items:
        total_mrp += i.varaiant.mrp * i.quantity
        discount += i.varaiant.discount * i.quantity
        offer_price += i.varaiant.offer_price * i.quantity
    if total_mrp > 10000:
        shipping = 0
    else:
        shipping = 50
    
    context ={
         "order_items":order_items,
         "order": order,
         "total_mrp":total_mrp,
         "offer_price":offer_price,
         "discount":discount,
         "shipping":shipping,
         
     }
    return render (request,"user/user_order_success.html",context)



# def user_profile_order_page_view(request ,order_id):
#     print(order_id,"order_id")
#     order_items = OrderProduct.objects.filter(order_no__order_number = order_id )
    
#     order = Order.objects.get(order_number = order_id)
#     total_mrp =0
#     discount =0
#     offer_price =0
#     shipping =0

#     for i in order_items:
#         total_mrp += i.varaiant.mrp * i.quantity
#         discount += i.varaiant.discount * i.quantity
#         offer_price += i.varaiant.offer_price * i.quantity
#     if total_mrp > 10000:
#         shipping =0
#     else:
#         shipping =50


#     context ={
#         "order_items":order_items,
#         "order": order,
#         "total_mrp":total_mrp,
#         "offer_price":offer_price,
#         "discount":discount,
#         "shipping":shipping,

#     }
#     return render(request, "user/user_profile/user_order_page_view.html", context)


        
@login_required(login_url='userlogin')
def my_orders(request):
    orders =Order.objects.filter(user = request.user)

    return render(request,"user/user_my_orders.html",{"orders":orders})




def razorpay_payment(request):
    user=request.user
    if user is None:
         return render(request,'user/register.html')
    
    cart = Cart.objects.get(cart_id=user)
    payment_amount = cart.get_total()*100
    client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET)) 
    DATA = {
    "amount": float(payment_amount),
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
    }
    order = client.order.create(data=DATA)    
    cart = Cart.objects.get( user = user )
    res = {
        'success': True,
        'key_id': RAZOR_KEY_ID,
        'amount': float(payment_amount),
        'order_id': order['id'],
        'name': cart.user.first_name,
    
        'email': cart.user.email,
        'mobile': cart.user.phone_number,
    }
    return JsonResponse(res)