from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# ==========================
# CATEGORY ADMIN
# ==========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "icon",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ==========================
# PRODUCT ADMIN
# ==========================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "image_preview",
        "name",
        "brand",
        "sku",
        "category",
        "price",
        "old_price",
        "discount",
        "stock",
        "available",
        "featured",
        "created_at",
    )

    list_filter = (
        "category",
        "brand",
        "available",
        "featured",
        "created_at",
    )

    search_fields = (
        "name",
        "brand",
        "sku",
        "description",
    )

    list_editable = (
        "price",
        "discount",
        "stock",
        "available",
        "featured",
    )

    ordering = (
        "-created_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="55" height="55" style="border-radius:8px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Image"
    # ==========================
# CART ADMIN
# ==========================


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
    )


# ==========================
# CART ITEM ADMIN
# ==========================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
    )

    list_filter = (
        "product",
    )

    search_fields = (
        "product__name",
        "cart__user__username",
    )


# ==========================
# ORDER INLINE
# ==========================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ==========================
# ORDER ADMIN
# ==========================

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

    list_filter = (
        "paid",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "user__username",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        OrderItemInline,
    ]
