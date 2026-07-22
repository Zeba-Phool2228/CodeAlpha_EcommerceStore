from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/",
         views.cart_remove, name="cart_remove"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("order/success/<int:order_id>/",
         views.order_success, name="order_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
