from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import (
    Product,
    Category,
    Order,
    OrderItem,
    Cart,
    CartItem,
)

from .forms import SignUpForm, OrderForm


def product_list(request):
    category_slug = request.GET.get("category")
    sort = request.GET.get("sort")
    search = request.GET.get("search", "").strip()

    products = Product.objects.filter(available=True)

    # Category Filter
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Search Filter
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(category__name__icontains=search) |
            Q(brand__icontains=search) |
            Q(sku__icontains=search)
        ).distinct()

    # Sorting
    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "name_az":
        products = products.order_by("name")

    elif sort == "name_za":
        products = products.order_by("-name")

    elif sort == "newest":
        products = products.order_by("-created_at")

    categories = Category.objects.all()

    featured_products = Product.objects.filter(
        available=True,
        featured=True
    )[:3]

    return render(
        request,
        "store/product_list.html",
        {
            "products": products,
            "categories": categories,
            "featured_products": featured_products,
            "selected_category": category_slug,
            "search": search,
            "sort": sort,
        },
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
        },
    )


def cart_add(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first.")
        return redirect("login")

    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect("cart_detail")


def cart_remove(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login")

    cart = get_object_or_404(Cart, user=request.user)

    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        item.delete()
        messages.success(request, "Item removed from cart.")
    except CartItem.DoesNotExist:
        pass

    return redirect("cart_detail")


@login_required(login_url="login")
def cart_increase(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)

    item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=product_id,
    )

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()
    else:
        messages.warning(
            request,
            "No more stock available."
        )

    return redirect("cart_detail")


@login_required(login_url="login")
def cart_decrease(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)

    item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=product_id,
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart_detail")


def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(
        request,
        "store/cart_detail.html",
        {
            "cart": cart,
            "cart_items": cart.items.select_related("product"),
        },
    )


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)

            Cart.objects.get_or_create(user=user)

            messages.success(request, "Account created successfully.")
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

                Cart.objects.get_or_create(user=user)

                return redirect("product_list")

    else:
        form = AuthenticationForm()

    return render(request, "store/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("product_list")


@login_required(login_url="login")
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            order.user = request.user
            order.email = form.cleaned_data["email"]

            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )

            cart.items.all().delete()

            messages.success(request, "Order placed successfully.")

            return redirect("order_success", order_id=order.id)

    else:
        form = OrderForm()

    return render(
        request,
        "store/checkout.html",
        {
            "cart": cart,
            "cart_items": cart.items.select_related("product"),
            "form": form,
        },
    )


@login_required(login_url="login")
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "store/order_success.html",
        {
            "order": order,
        },
    )


@login_required(login_url="login")
def my_orders(request):
    orders = (
        Order.objects.filter(user=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "store/my_orders.html",
        {
            "orders": orders,
        },
    )


@login_required(login_url="login")
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "store/order_detail.html",
        {
            "order": order,
        },
    )


@login_required(login_url="login")
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    if order.can_be_cancelled:
        order.status = "Cancelled"
        order.save()

        messages.success(
            request,
            f"Order #{order.id} has been cancelled successfully."
        )

    else:
        messages.error(
            request,
            f"Order #{order.id} can no longer be cancelled."
        )

    return redirect("my_orders")


@login_required(login_url="login")
def profile_view(request):
    orders_count = Order.objects.filter(user=request.user).count()

    return render(
        request,
        "store/profile.html",
        {
            "orders_count": orders_count,
        },
    )


def contact_view(request):
    return render(request, "store/contact.html")