import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, ShippingInfo, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import ShippingInfoForm, ProductForm
from datetime import datetime


# Create your views here.
def home(request):
    categories = Category.objects.all()
    popularItems = Product.objects.order_by('countInStock')[:4]
    recentItems = Product.objects.order_by('createdAt').reverse()[:4]
    context = {'popularItems': popularItems, 'recentItems': recentItems, 'categories': categories}
    return render(request, "home.html", context)


def productScreen(request, pk):
    if request.method == 'POST':
        carts = Cart.objects.filter(user=request.user).order_by('createdAt').reverse()[:1]
        cart = carts[0]
        product = Product.objects.get(id=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        if not quantity:
            quantity = 1
        cartItem = CartItem(cart=cart, product=product, quantity=quantity)
        cartItem.save()
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, "productScreen.html", context)


def categoryScreen(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, "categoryScreen.html", context)


def loginScreen(request):
    context = {'invalidUser': False, 'invalidPassword': False}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context.update({'invalidUser': False, 'invalidPassword': 'Погрешна лозинка'})
        except:
            context.update({'invalidUser': 'Невалиден корисник', 'invalidPassword': False})
    return render(request, "login.html", context)


def registerScreen(request):
    form = UserCreationForm()
    context = {'form': form, 'error': False}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            cart = Cart(user=user)
            cart.save()
            return redirect('home')
        else:
            context.update({
                'error': "Лозинката мора да содржи барем 8 знаци. Лознката мора да биде комбинација од букви и бројки"})

    return render(request, "register.html", context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def cartScreen(request):
    # cart = Cart.objects.get(user=request.user,)
    carts = Cart.objects.filter(user=request.user).order_by('createdAt').reverse()[:1]
    cart = carts[0]
    cartItems = CartItem.objects.filter(cart=cart)
    totalPrice = 0
    for item in cartItems:
        totalPrice = totalPrice + (item.product.price * item.quantity)
    context = {'cartItems': cartItems, 'totalPrice': totalPrice}
    return render(request, "cartScreen.html", context)


def shippingScreen(request):
    try:
        shipping = ShippingInfo.objects.get(user=request.user)
        form = ShippingInfoForm(instance=shipping)
        if request.method == 'POST':
            form = ShippingInfoForm(request.POST, instance=shipping)
            if form.is_valid():
                form.save()
                return redirect('paymentScreen')
        context = {'form': form}
        return render(request, "shippingScreen.html", context)
    except:
        if request.method == 'POST':
            form_data = ShippingInfoForm(data=request.POST)
            if form_data.is_valid():
                shippingInfo = form_data.save(commit=False)
                shippingInfo.user = request.user
                shippingInfo.save()
                return redirect('paymentScreen')
        context = {'form': ShippingInfoForm}
        return render(request, "shippingScreen.html", context)


def paymentScreen(request):
    context = {'invalidCardHolder': False, 'invalidCardNumber': False, 'invalidCVV': False}
    carts = Cart.objects.filter(user=request.user).order_by('createdAt').reverse()[:1]
    cart = carts[0]
    cartItems = CartItem.objects.filter(cart=cart)
    itemsPrice = 0
    shippingPrice = 150
    for item in cartItems:
        itemsPrice = itemsPrice + (item.product.price * item.quantity)
    if itemsPrice >= 1500:
        shippingPrice = 0
    totalPrice = itemsPrice + shippingPrice
    if request.method == 'POST':
        cardHolder = request.POST.get('cardHolder')
        cardNumber = request.POST.get('cardNumber')
        CVV = request.POST.get("CVV")
        parts = cardHolder.split()
        cardHolder = ''.join(parts)
        print(cardHolder)
        if not cardHolder.isalpha():
            context.update({'invalidCardHolder': 'Невалидно име и презиме'})
        if not cardNumber.isdigit() or not len(cardNumber) == 16:
            context.update({'invalidCardNumber': 'Невалиден број на картичка'})
        if not CVV.isdigit():
            context.update({'invalidCVV': 'Невалиден CVV2/CVC2'})
        if context.get('invalidCardHolder') == False and context.get('invalidCardNumber') == False and context.get(
                'invalidCVV') == False:
            order = Order(user=request.user, cart=cart, itemsPrice=itemsPrice, shippingPrice=shippingPrice,
                          totalPrice=totalPrice)
            order.save()
            cart = Cart(user=request.user)
            cart.save()
            return redirect('orderScreen', order.id)
    return render(request, "paymentScreen.html", context)


def removeCartItem(request, pk):
    cartItem = CartItem.objects.get(id=pk)
    cartItem.delete()
    return redirect('cartScreen')


def orderScreen(request, pk):
    order = Order.objects.get(id=pk)
    cartItems = CartItem.objects.filter(cart=order.cart)
    shippingInfo = ShippingInfo.objects.get(user=order.user)
    context = {'order': order, 'shippingInfo': shippingInfo, 'cartItems': cartItems}
    return render(request, "orderScreen.html", context)


def orderHistoryScreen(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, "orderHistoryScreen.html", context)


def addProductScreen(request):
    context = {'form': ProductForm}
    if request.method == 'POST':
        form_data = ProductForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            product = form_data.save(commit=False)
            product.image = form_data.cleaned_data['image']
            product.save()
            return redirect('addProductScreen')
    return render(request, "addProductScreen.html", context)


def ordersScreen(request):
    orders = Order.objects.order_by('createdAt').reverse().all()
    context = {'orders': orders}
    return render(request, "ordersScreen.html", context)


def manageOrderScreen(request, pk):
    order = Order.objects.get(id=pk)
    cart = order.cart
    cartItems = CartItem.objects.filter(cart=cart)
    shippingInfo = ShippingInfo.objects.get(user=order.user)
    context = {'order': order, 'cartItems': cartItems, 'shippingInfo': shippingInfo}
    return render(request, "manageOrderScreen.html", context)


def actionOrderSent(request, pk):
    order = Order.objects.get(id=pk)
    order.isShipped = True
    order.shippedAt = datetime.now()
    order.save()
    return redirect('manageOrderScreen', pk)


def actionOrderArrived(request, pk):
    order = Order.objects.get(id=pk)
    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()
    return redirect('manageOrderScreen', pk)

def productsScreen(request):
    products = Product.objects.order_by('createdAt').all()
    context = {'products': products}
    return render(request, "productsScreen.html", context)

def productEditScreen(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('productEditScreen', pk)
    context = {'product': product, 'form': form}
    return render(request, "productEditScreen.html", context)
