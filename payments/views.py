# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.db import transaction
# from django.utils import timezone

# from .models import Payment
# from billing.models import Invoice


# @login_required
# def payment_add(request, invoice_id):

#     invoice = get_object_or_404(
#         Invoice,
#         id=invoice_id
#     )

#     if request.method == 'POST':

#         amount = request.POST.get('amount')
#         payment_method = request.POST.get('payment_method')
#         payment_date = request.POST.get('payment_date')
#         notes = request.POST.get('notes')

#         try:

#             amount = float(amount)

#             if amount <= 0:
#                 raise ValueError(
#                     'Payment amount must be greater than 0.'
#                 )

#             if amount > float(invoice.pending_amount):
#                 raise ValueError(
#                     f'Payment cannot be greater than pending amount '
#                     f'₹{invoice.pending_amount}.'
#                 )

#             with transaction.atomic():

#                 Payment.objects.create(
#                     invoice=invoice,
#                     amount=amount,
#                     payment_method=payment_method,
#                     payment_date=payment_date,
#                     notes=notes,
#                 )

#                 total_paid = invoice.paid_amount + amount

#                 if total_paid >= invoice.grand_total:
#                     invoice.status = 'paid'

#                 elif total_paid > 0:
#                     invoice.status = 'partial'

#                 else:
#                     invoice.status = 'unpaid'

#                 invoice.save(update_fields=['status'])

#             messages.success(
#                 request,
#                 'Payment added successfully.'
#             )

#             return redirect(
#                 'invoice_detail',
#                 invoice_id=invoice.id
#             )

#         except ValueError as error:

#             messages.error(
#                 request,
#                 str(error)
#             )

#     return render(
#         request,
#         'payments/payment_add.html',
#         {
#             'invoice': invoice,
#             'today': timezone.now().date(),
#         }
#     )


# @login_required
# def payment_history(request):

#     payments = Payment.objects.select_related(
#         'invoice',
#         'invoice__customer'
#     ).order_by(
#         '-payment_date',
#         '-id'
#     )

#     return render(
#         request,
#         'payments/payment_history.html',
#         {
#             'payments': payments
#         }
#     )

from decimal import Decimal

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Payment
from billing.models import Invoice


@login_required
def payment_history(request):

    payments = Payment.objects.select_related(
        'invoice',
        'invoice__customer'
    ).order_by(
        '-payment_date',
        '-id'
    )

    return render(
        request,
        'payments/payment_history.html',
        {
            'payments': payments
        }
    )


@login_required
def add_payment(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    if request.method == 'POST':

        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        payment_date = request.POST.get('payment_date')
        notes = request.POST.get('notes', '')

        try:

            amount = Decimal(amount)

        except Exception:

            messages.error(
                request,
                'Please enter a valid payment amount.'
            )

            return redirect(
                'payment_add',
                invoice_id=invoice.id
            )

        if amount <= 0:

            messages.error(
                request,
                'Payment amount must be greater than 0.'
            )

            return redirect(
                'payment_add',
                invoice_id=invoice.id
            )

        pending_amount = invoice.pending_amount

        if amount > pending_amount:

            messages.error(
                request,
                f'Payment cannot be greater than '
                f'pending amount ₹{pending_amount}.'
            )

            return redirect(
                'payment_add',
                invoice_id=invoice.id
            )

        Payment.objects.create(
            invoice=invoice,
            amount=amount,
            payment_method=payment_method,
            payment_date=payment_date,
            notes=notes
        )

        total_paid = invoice.paid_amount

        if total_paid >= invoice.grand_total:

            invoice.status = 'paid'

        elif total_paid > 0:

            invoice.status = 'partial'

        else:

            invoice.status = 'unpaid'

        invoice.save(
            update_fields=['status']
        )

        messages.success(
            request,
            'Payment added successfully.'
        )

        return redirect(
            'invoice_detail',
            invoice_id=invoice.id
        )

    return render(
        request,
        'payments/payment_add.html',
        {
            'invoice': invoice,
            'today': timezone.now().date()
        }
    )