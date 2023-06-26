from django.shortcuts import render, redirect
from .models import Item, Order, OrderItem
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.


def home_page(request):

    products = Item.objects.filter(status=1).order_by('-created_on')
    return render(request, 'index.html', {'products': products})


def product_detail(request, pk):
    products = Item.objects.filter(status=1).order_by('-created_on')
    product = get_object_or_404(Item, pk=pk)
    return render(request, 'product.html', {'product': product,
                                            'products':products})

@login_required
def cart_page(request):
    order = []
    order_items = []
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    products = Item.objects.filter(status=1).order_by('-created_on')

    if order_qs.exists():
        order = order_qs[0]
        order_items = order.items.filter(ordered=False)

    return render(request, 'shopping-cart.html', {'order': order,
                                                  'order_items': order_items,
                                                  'products': products})

@login_required
def add_to_cart(request, pk):

    if (request.user.is_authenticated):
        item = get_object_or_404(Item, pk=pk)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Added Quantity Item")
                return redirect("market:cart")
            
            else:
                order.items.add(order_item)
                messages.info(request, "Added Item to Cart")
                return redirect("market:cart")
            
        else:
            order = Order.objects.create(
                user=request.user,
                ordered=False
            )

            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("market:cart")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False)[0]
            order_item.delete()

            messages.info(request, "Item Removed From Cart")
            return redirect("market:cart")
        
        else:
            messages.info(request, "Item not in cart")
            return redirect("market:cart")
        
    
    else:
        messages.info(request, "You do not have an order")
        return redirect("market:cart")
        
        
def register(request):

    if (request.method == "POST"):

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('market:home')
        
    else:
        form = UserCreationForm()

    
    return render(request, 'registration/register.html', {'form': form})

