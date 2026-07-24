from django.contrib import admin
from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock",
        "available",
        "featured",
        "created_at",
    )
    list_filter = (
        "available",
        "featured",
        "category",
    )
    search_fields = ("name",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__username",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
    )
    list_filter = ("product",)
    search_fields = (
        "product__name",
        "cart__user__username",
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "city",
        "phone",
        "paid",
        "created_at",
    )
    list_filter = ("paid", "created_at")
    search_fields = (
        "full_name",
        "phone",
        "user__username",
    )
    inlines = [OrderItemInline]
