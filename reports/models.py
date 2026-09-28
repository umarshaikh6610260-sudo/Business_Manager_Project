from django.shortcuts import render

from django.db.models import Sum

from billing.models import Invoice
from payments.models import Payment
from expenses.models import Expense
from customers.models import Customer
from products.models import Product


def reports_dashboard(request):

    total_sales = (
        Invoice.objects.aggregate(
            total=Sum('discount')
        )['total'] or 0
    )

    total_expenses = (
        Expense.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )

    total_customers = Customer.objects.count()

    total_products = Product.objects.count()

    total_payments = (
        Payment.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )

    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_payments': total_payments,
    }

    return render(
        request,
        'reports/reports_dashboard.html',
        context
    )