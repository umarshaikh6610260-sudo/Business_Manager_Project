from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone

from billing.models import Invoice, InvoiceItem
from payments.models import Payment
from expenses.models import Expense
from customers.models import Customer
from products.models import Product

from .models import UserProfile


@login_required(login_url='login')
def dashboard(request):

    # -----------------------------
    # TOTAL SALES
    # -----------------------------

    sales_expression = ExpressionWrapper(
        F('quantity') * F('price'),
        output_field=DecimalField(
            max_digits=12,
            decimal_places=2
        )
    )

    total_sales = (
        InvoiceItem.objects
        .aggregate(
            total=Sum(sales_expression)
        )['total']
        or 0
    )

    # -----------------------------
    # TOTAL EXPENSES
    # -----------------------------

    total_expenses = (
        Expense.objects
        .aggregate(
            total=Sum('amount')
        )['total']
        or 0
    )

    # -----------------------------
    # TOTAL PAYMENTS
    # -----------------------------

    total_payments = (
        Payment.objects
        .aggregate(
            total=Sum('amount')
        )['total']
        or 0
    )

    # -----------------------------
    # BASIC COUNTS
    # -----------------------------

    total_customers = Customer.objects.count()

    total_products = Product.objects.count()

    total_invoices = Invoice.objects.count()

    # -----------------------------
    # PENDING PAYMENTS
    # -----------------------------

    pending_payments = total_sales - total_payments

    # -----------------------------
    # NET PROFIT
    # -----------------------------

    net_profit = total_sales - total_expenses

    # -----------------------------
    # LOW STOCK PRODUCTS
    # -----------------------------

    low_stock_products = Product.objects.filter(
        stock__lte=F('minimum_stock')
    ).count()

    # -----------------------------
    # FOLLOW-UPS
    # -----------------------------

    today = timezone.now().date()

    followups = Customer.objects.filter(
        follow_up_date__isnull=False,
        follow_up_date__gte=today
    ).order_by(
        'follow_up_date'
    )[:10]

    # -----------------------------
    # CONTEXT
    # -----------------------------

    context = {

        'total_sales': total_sales,

        'total_expenses': total_expenses,

        'total_payments': total_payments,

        'pending_payments': pending_payments,

        'net_profit': net_profit,

        'total_customers': total_customers,

        'total_products': total_products,

        'total_invoices': total_invoices,

        'low_stock_products': low_stock_products,

        'followups': followups,

    }

    return render(
        request,
        'dashboard.html',
        context
    )


# ---------------------------------
# REGISTER
# ---------------------------------

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password validation
        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        # Username validation
        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create profile
        UserProfile.objects.create(
            user=user,
            role='staff'
        )

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# ---------------------------------
# LOGIN
# ---------------------------------

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'login.html'
    )


# ---------------------------------
# LOGOUT
# ---------------------------------

def logout_view(request):

    logout(request)

    return redirect('login')