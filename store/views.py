from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import SignUpForm, OrderForm


def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, "store/product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect("cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "store/cart_detail.html", {"cart": cart})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("product_list")
    else:
        form = SignUpForm()
    return render(request, "store/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("product_list")
    else:
        form = AuthenticationForm()
    return render(request, "store/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("product_list")


@login_required(login_url="login")
def checkout_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["product"].price,
                    quantity=item["quantity"],
                )

            cart.clear()
            messages.success(
                request, "Your order has been placed successfully!")
            return redirect("order_success", order_id=order.id)
    else:
        form = OrderForm()

    return render(request, "store/checkout.html", {"cart": cart, "form": form})


@login_required(login_url="login")
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "store/order_success.html", {"order": order})


@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "store/my_orders.html", {"orders": orders})
