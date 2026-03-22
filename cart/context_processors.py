def cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        from .models import Cart
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        session_key = request.session.session_key
        if session_key:
            from .models import Cart
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_count = cart.total_items
            except Cart.DoesNotExist:
                cart_count = 0
    
    return {'cart_count': cart_count}
