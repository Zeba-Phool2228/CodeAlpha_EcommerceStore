from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# ======================================================
# CATEGORY MODEL
# ======================================================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        default="bi-tag",
        help_text="Bootstrap Icons class name, e.g. bi-laptop, bi-phone"
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ======================================================
# PRODUCT MODEL
# ======================================================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    brand = models.CharField(
        max_length=100,
        help_text="Example: Apple, Samsung, Sony"
    )

    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique Product Code"
    )

    description = models.TextField()

    specifications = models.TextField(
        blank=True,
        default=""
    )

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    discount = models.PositiveIntegerField(
        default=0,
        help_text="Discount Percentage"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    available = models.BooleanField(
        default=True
    )

    featured = models.BooleanField(
        default=False,
        help_text="Show product in Best Sellers section"
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    weight = models.CharField(
        max_length=50,
        blank=True
    )

    warranty = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ======================================================
# CART MODELS
# ======================================================

class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity
    # ======================================================
# ORDER MODELS
# ======================================================

class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    full_name = models.CharField(
        max_length=200
    )

    address = models.CharField(
        max_length=300
    )

    city = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    paid = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    def get_total_cost(self):
        return sum(
            item.get_cost()
            for item in self.items.all()
        )

    @property
    def can_be_cancelled(self):
        return self.status in ["Pending", "Processing"]


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"
