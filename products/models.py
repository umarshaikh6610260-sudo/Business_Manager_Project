from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=150)

    category = models.CharField(
        max_length=100,
        blank=True
    )

    sku = models.CharField(
        max_length=50,
        unique=True
    )

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    minimum_stock = models.PositiveIntegerField(
        default=5
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"{self.name} ({self.sku})"


    @property
    def is_low_stock(self):
        return self.stock <= self.minimum_stock