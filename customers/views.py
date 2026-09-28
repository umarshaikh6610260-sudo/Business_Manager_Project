# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from billing.models import Invoice

# from django.utils import timezone
# from django.db.models import Q

# from .models import Customer

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.db.models import Q

from .models import Customer
from billing.models import Invoice

def customer_list(request):

    search = request.GET.get('search', '')

    customers = Customer.objects.all().order_by('-created_at')

    if search:
        customers = customers.filter(
            name__icontains=search
        ) | customers.filter(
            phone__icontains=search
        ) | customers.filter(
            email__icontains=search
        )

    context = {
        'customers': customers,
        'search': search,
    }

    return render(
        request,
        'customers/customer_list.html',
        context
    )


def add_customer(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        notes = request.POST.get('notes')
        follow_up_date = request.POST.get('follow_up_date')

        Customer.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            notes=notes,
            follow_up_date=follow_up_date or None,
        )

        return redirect('customer_list')

    return render(
        request,
        'customers/add_customer.html'
    )


def edit_customer(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == 'POST':

        customer.name = request.POST.get('name')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')
        customer.notes = request.POST.get('notes')

        follow_up_date = request.POST.get(
            'follow_up_date'
        )

        customer.follow_up_date = (
            follow_up_date or None
        )

        customer.save()

        return redirect('customer_list')

    context = {
        'customer': customer
    }

    return render(
        request,
        'customers/edit_customer.html',
        context
    )


def delete_customer(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == 'POST':

        customer.delete()

        return redirect('customer_list')

    return render(
        request,
        'customers/delete_customer.html',
        {'customer': customer}
    )

@login_required
def customer_detail(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    invoices = Invoice.objects.filter(
        customer=customer
    ).order_by(
        '-invoice_date',
        '-id'
    )

    total_purchase = sum(
        invoice.grand_total
        for invoice in invoices
    )

    total_paid = sum(
        invoice.paid_amount
        for invoice in invoices
    )

    pending_amount = total_purchase - total_paid

    return render(
        request,
        'customers/customer_detail.html',
        {
            'customer': customer,
            'invoices': invoices,
            'total_purchase': total_purchase,
            'total_paid': total_paid,
            'pending_amount': pending_amount,
        }
    )

@login_required
def follow_up_list(request):

    today = timezone.localdate()

    customers = Customer.objects.filter(
        follow_up_date__isnull=False
    ).order_by(
        'follow_up_date'
    )

    overdue = customers.filter(
        follow_up_date__lt=today
    )

    today_followups = customers.filter(
        follow_up_date=today
    )

    upcoming = customers.filter(
        follow_up_date__gt=today
    )

    return render(
        request,
        'customers/follow_up_list.html',
        {
            'overdue': overdue,
            'today_followups': today_followups,
            'upcoming': upcoming,
            'today': today,
        }
    )