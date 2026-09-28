# from django.db import models

# from billing.models import Invoice


# class Payment(models.Model):

#     PAYMENT_METHODS = [
#         ('cash', 'Cash'),
#         ('upi', 'UPI'),
#         ('bank', 'Bank Transfer'),
#         ('card', 'Card'),
#         ('other', 'Other'),
#     ]

#     invoice = models.ForeignKey(
#         Invoice,
#         on_delete=models.CASCADE,
#         related_name='payments'
#     )

#     amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     payment_method = models.CharField(
#         max_length=20,
#         choices=PAYMENT_METHODS,
#         default='cash'
#     )

#     payment_date = models.DateField()

#     notes = models.TextField(
#         blank=True
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     def __str__(self):
#         return f"{self.invoice.invoice_number} - ₹{self.amount}"

from django.db import models
from billing.models import Invoice


class Payment(models.Model):

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer'),
        ('card', 'Card'),
        ('other', 'Other'),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='cash'
    )

    payment_date = models.DateField()

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.invoice.invoice_number} - ₹{self.amount}"