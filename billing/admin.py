from django.contrib import admin

# # Register your models here.

# from .models import Invoice

from .models import (
    Invoice,
    InvoiceItem,
    Quotation,
    QuotationItem,
)




@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):

    list_display = (
        'quotation_number',
        'customer',
        'quotation_date',
        'valid_until',
        'status',
        'discount',
    )

    list_filter = (
        'status',
        'quotation_date',
    )

    search_fields = (
        'quotation_number',
        'customer__name',
    )