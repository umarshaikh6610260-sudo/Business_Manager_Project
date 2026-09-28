# from django.shortcuts import render

# # Create your views here.

# from django.contrib.auth.decorators import login_required
# from accounts.decorators import role_required

# @login_required
# @role_required('owner', 'accountant')
# def reports_dashboard(request):
#     reports = reports.objects.order_by(
#             '-expense_date',
#             '-id'
#         )
    
#     return render(
#             request,
#             'expenses/expense_list.html',
#             {
#                 'expenses': reports
#             }
#         )

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import (
    Sum,
    F,
    DecimalField,
    ExpressionWrapper
)

from django.db.models.functions import (
    TruncMonth
)

from billing.models import Invoice, InvoiceItem
from payments.models import Payment
from expenses.models import Expense
from customers.models import Customer
from products.models import Product


@login_required
def reports_dashboard(request):

    # --------------------------------
    # TOTAL SALES
    # --------------------------------

    item_total_expression = ExpressionWrapper(
        F('quantity') * F('price'),
        output_field=DecimalField(
            max_digits=12,
            decimal_places=2
        )
    )

    items_sales = InvoiceItem.objects.aggregate(
        total=Sum(item_total_expression)
    )['total'] or 0

    total_discount = Invoice.objects.aggregate(
        total=Sum('discount')
    )['total'] or 0

    total_sales = items_sales - total_discount


    # --------------------------------
    # TOTAL EXPENSES
    # --------------------------------

    total_expenses = Expense.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0


    # --------------------------------
    # TOTAL PAYMENTS
    # --------------------------------

    total_payments = Payment.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0


    # --------------------------------
    # PENDING PAYMENTS
    # --------------------------------

    pending_payments = total_sales - total_payments


    # --------------------------------
    # PROFIT
    # --------------------------------

    total_profit = total_sales - total_expenses


    # --------------------------------
    # COUNTS
    # --------------------------------

    total_customers = Customer.objects.count()

    total_products = Product.objects.count()

    total_invoices = Invoice.objects.count()


    # --------------------------------
    # MONTHLY SALES
    # --------------------------------

    monthly_sales = (
        InvoiceItem.objects
        .annotate(
            month=TruncMonth(
                'invoice__invoice_date'
            ),
            item_total=item_total_expression
        )
        .values('month')
        .annotate(
            total=Sum('item_total')
        )
        .order_by('month')
    )


    # --------------------------------
    # MONTHLY EXPENSES
    # --------------------------------

    monthly_expenses = (
        Expense.objects
        .annotate(
            month=TruncMonth(
                'expense_date'
            )
        )
        .values('month')
        .annotate(
            total=Sum('amount')
        )
        .order_by('month')
    )


    context = {

        'total_sales': total_sales,

        'total_expenses': total_expenses,

        'total_profit': total_profit,

        'total_payments': total_payments,

        'pending_payments': pending_payments,

        'total_customers': total_customers,

        'total_products': total_products,

        'total_invoices': total_invoices,

        'monthly_sales': monthly_sales,

        'monthly_expenses': monthly_expenses,

    }


    return render(
        request,
        'reports/reports_dashboard.html',
        context
    )