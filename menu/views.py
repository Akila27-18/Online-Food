from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import stripe

from .models import Item, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

# ----------------- MENU -----------------
def menu(request):
    items = Item.objects.filter(available=True)
    return render(request, 'menu/menu.html', {'items': items})

# ----------------- CART -----------------
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for item_id, quantity in cart.items():
        item = get_object_or_404(Item, id=item_id)
        items.append({'item': item, 'quantity': quantity, 'subtotal': item.price * quantity})
        total += item.price * quantity
    return render(request, 'menu/cart.html', {'items': items, 'total': total})

# ----------------- CHECKOUT -----------------
@login_required
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('menu')
        order = Order.objects.create(user=request.user)
        total = 0
        for item_id, quantity in cart.items():
            item = get_object_or_404(Item, id=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=quantity)
            total += item.price * quantity
        order.total_price = total
        order.save()
        request.session['cart'] = {}
        return render(request, 'menu/checkout.html', {'success': True})
    return render(request, 'menu/checkout.html')

# ----------------- USER REGISTRATION -----------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu')
    else:
        form = UserCreationForm()
    return render(request, 'menu/register.html', {'form': form})

# ----------------- ORDER HISTORY -----------------
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'menu/order_history.html', {'orders': orders})

# ----------------- STRIPE CHECKOUT -----------------
@csrf_exempt
def create_checkout_session(request):
    cart = request.session.get('cart', {})
    line_items = []
    for item_id, quantity in cart.items():
        item = get_object_or_404(Item, id=item_id)
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item.name},
                'unit_amount': int(item.price * 100),
            },
            'quantity': quantity,
        })
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/checkout/'),
        cancel_url=request.build_absolute_uri('/cart/'),
    )
    return JsonResponse({'id': session.id})

# ----------------- ADMIN DASHBOARD -----------------
@staff_member_required
def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    items = Item.objects.all()
    return render(request, 'menu/dashboard.html', {'orders': orders, 'items': items})

@staff_member_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        return redirect('dashboard')
from django.contrib.auth.views import LogoutView

class MyLogoutView(LogoutView):
    allow_get = True
