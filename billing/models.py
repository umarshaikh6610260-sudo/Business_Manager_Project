from django.db import models

from customers.models import Customer
from products.models import Product


class Invoice(models.Model):

    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    invoice_number = models.CharField(
        max_length=30,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    invoice_date = models.DateField()

    due_date = models.DateField(
        blank=True,
        null=True
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unpaid'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number

    @property
    def subtotal(self):
        return sum(
            item.total
            for item in self.items.all()
        )

    @property
    def grand_total(self):
        return self.subtotal - self.discount

    @property
    def paid_amount(self):
        return sum(
            payment.amount
            for payment in self.payments.all()
        )

    @property
    def pending_amount(self):
        return self.grand_total - self.paid_amount


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Quotation(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    quotation_number = models.CharField(
        max_length=30,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='quotations'
    )

    quotation_date = models.DateField()

    valid_until = models.DateField(
        blank=True,
        null=True
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.quotation_number

    @property
    def subtotal(self):

        return sum(
            item.total
            for item in self.items.all()
        )

    @property
    def grand_total(self):

        return self.subtotal - self.discount


class QuotationItem(models.Model):

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total(self):

        return self.quantity * self.price

    def __str__(self):

        return (
            f"{self.product.name} - "
            f"{self.quantity}"
        )
    