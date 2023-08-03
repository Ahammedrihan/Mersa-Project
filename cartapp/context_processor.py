from .models import Cart, CartItem
from  .views import _cart_id

def counter(request):
    cart_count =0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user= request.user)
            cart_count = cart_items.count()
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart)
            cart_count = cart_items.count()
            
    except Cart.DoesNotExist:
        cart_count=0
    return ({'cart_count':cart_count})

      
