# from django.contrib import admin

# # Register your models here.
from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'sku',
        'category',
        'purchase_price',
        'selling_price',
        'stock',
        'minimum_stock',
        'low_stock_status',
    )

    search_fields = (
        'name',
        'sku',
        'category',
    )

    list_filter = (
        'category',
    )


    @admin.display(
        boolean=True,
        description='Low Stock'
    )
    def low_stock_status(self, obj):
        return obj.is_low_stock
