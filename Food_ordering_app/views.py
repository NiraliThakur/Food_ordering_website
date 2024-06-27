from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from Food_ordering_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Food_ordering_app.forms import ShippingForm


# Create your views here
def index(request):
    pizzas = MenuItem.objects.all()

    query = request.GET.get('q')
    if query:
        pizzas = pizzas.filter(category__icontains=query)
    else:
        print('Not Found')
    return render(request, 'index.html', {'pizzas': pizzas})


@login_required 
def add_item(request, pizza_id):
    menuitem = get_object_or_404(MenuItem, id=pizza_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menuitem=menuitem)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        toppings_ids = request.POST.getlist('toppings')

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menuitem=menuitem
        )
        if not created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity = quantity

        cart_item.toppings.clear()
        for topping_id in toppings_ids:
            topping = get_object_or_404(PizzaTopping, id=topping_id)
            cart_item.toppings.add(topping)


        cart_item.save()
        messages.success(request, f'{menuitem.pizza_name} added to cart!')
        return redirect('Food_ordering_app:cart')

    toppings = PizzaTopping.objects.all()
    return render(request, 'add_item.html', {'menuitem': menuitem, 'toppings': toppings})


def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    
    cart_total = 0

    for item in cart_items:
        item_total = item.menuitem.price * item.quantity
        toppings_total = sum(topping.price for topping in item.toppings.all()) * item.quantity
        item.total_price = item_total + toppings_total  
        cart_total += item.total_price
        
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})


def update_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = get_object_or_404(CartItem, id=item_id, cart=cart)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        if new_quantity.isdigit() and int(new_quantity) > 0:
            cart_items.quantity = int(new_quantity)
            cart_items.save()
            messages.success(request, 'Cart item updated successfully!')

            return redirect('Food_ordering_app:cart')
        else:
            messages.error(request, 'Invalid quantity. Please enter a positive number.')
    return render(request, 'cart.html', {'cart_items': cart_items})


@login_required
def remove_cart_item(request, item_id):
    cart_items = get_object_or_404(CartItem, id=item_id)
    cart_items.delete()
    messages.success(request,'Item removed from cart')
    return redirect('Food_ordering_app:cart')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cart_items.all() 

    total_price = sum(
        (item.menuitem.price * item.quantity) + 
        sum(topping.price for topping in item.toppings.all()) * item.quantity 
        for item in cart_items
    )

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)

        if shipping_form.is_valid() :
            shipping_info = shipping_form.save(commit=False)
            shipping_info.user = request.user
            shipping_info.save()

            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                placed=True  
            )

            for item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    menuitem=item.menuitem,
                    quantity=item.quantity,
                    price=item.menuitem.price,  
                )
                order_item.toppings.set(item.toppings.all())
                order_item.save()

            # Clear the cart
            cart.cart_items.all().delete()
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('Food_ordering_app:order_details', order_id=order.id)

    else:
        shipping_form = ShippingForm()

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price, 'shipping_form': shipping_form})


def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.order_items.all()
    return render(request, 'order_details.html', {'order': order, 'order_items': order_items})



































# @login_required
# def checkout(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     cart_items = cart.cart_items.all()

#     cart_total = 0

#     for item in cart_items:
#         item_total = item.menuitem.price * item.quantity
#         toppings_total = sum(topping.price for topping in item.toppings.all()) * item.quantity
#         item.total_price = item_total + toppings_total
#         cart_total += item.total_price

#     if request.method == 'POST':
#         # Place the order
#         order = Order.objects.create(
#             user=request.user,
#             total_price=cart_total,
#             placed=True,
#             in_cart=False,
#             completed=False
#         )

#         # Create OrderItems from CartItems
#         for item in cart_items:
#             order_item = OrderItem.objects.create(
#                 order=order,
#                 category=item.menuitem.category.category_name,
#                 menuitem=item.menuitem,
#                 quantity=item.quantity,
#                 price=item.menuitem.price
#             )
#             order_item.toppings.set(item.toppings.all())
#             order_item.save()

#         # Clear the cart
#         cart.cart_items.all().delete()

#         return redirect('Food_ordering_app:order_details', order_id=order.id)

#     return render(request, 'checkout.html', {'cart_items': cart_items, 'cart_total': cart_total})

