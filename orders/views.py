from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart
from users.models import Address

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart:cart_detail')
    
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        
        if not address_id:
            messages.error(request, 'Please select a delivery address!')
            return redirect('orders:checkout')
        
        address = get_object_or_404(Address, id=address_id, user=request.user)
        
        order = Order.objects.create(
            user=request.user,
            shipping_address=address,
            total_amount=cart.total_price,
            status='pending',
            payment_status='pending'
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                quantity=item.quantity,
                price=item.product.price
            )
        
        request.session['pending_order_id'] = order.order_id
        cart.items.all().delete()
        
        return redirect('orders:order_detail', order_id=order.order_id)
    
    context = {
        'cart': cart,
        'addresses': addresses,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    if request.GET.get("payment") == "success":
     order.payment_status = 'paid'
     order.status = 'confirmed'
     order.save()

    return render(request, 'orders/order_detail.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)
