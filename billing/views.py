# from django.shortcuts import render, redirect, get_object_or_404

# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.shortcuts import get_object_or_404
# from django.db import transaction

# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.db import transaction

# from .models import (
#     Invoice,
#     InvoiceItem,
#     Quotation,
#     QuotationItem,
# )

# from customers.models import Customer
# from products.models import Product

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import (
    Invoice,
    InvoiceItem,
    Quotation,
    QuotationItem,
)

from customers.models import Customer
from products.models import Product

@login_required
def create_invoice(request):

    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':

        customer_id = request.POST.get('customer')
        invoice_number = request.POST.get('invoice_number')
        invoice_date = request.POST.get('invoice_date')
        due_date = request.POST.get('due_date')
        discount = request.POST.get('discount') or 0

        product_ids = request.POST.getlist(
            'product[]'
        )

        quantities = request.POST.getlist(
            'quantity[]'
        )

        if not customer_id:
            messages.error(
                request,
                'Please select a customer.'
            )
            return redirect('create_invoice')

        if not invoice_number:
            messages.error(
                request,
                'Invoice number is required.'
            )
            return redirect('create_invoice')

        if Invoice.objects.filter(
            invoice_number=invoice_number
        ).exists():

            messages.error(
                request,
                'Invoice number already exists.'
            )

            return redirect('create_invoice')

        if not product_ids:

            messages.error(
                request,
                'Please add at least one product.'
            )

            return redirect('create_invoice')

        try:

            with transaction.atomic():

                invoice = Invoice.objects.create(
                    invoice_number=invoice_number,
                    customer_id=customer_id,
                    invoice_date=invoice_date,
                    due_date=due_date or None,
                    discount=discount,
                )

                for product_id, quantity in zip(
                    product_ids,
                    quantities
                ):

                    product = Product.objects.select_for_update().get(
                        id=product_id
                    )

                    quantity = int(quantity)

                    if quantity <= 0:

                        raise ValueError(
                            'Quantity must be greater than 0.'
                        )

                    if quantity > product.stock:

                        raise ValueError(
                            f'Not enough stock for '
                            f'{product.name}. '
                            f'Available stock: '
                            f'{product.stock}'
                        )

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        price=product.selling_price,
                    )

                    product.stock -= quantity

                    product.save(
                        update_fields=['stock']
                    )

            messages.success(
                request,
                'Invoice created and stock updated successfully.'
            )

            return redirect(
                'invoice_detail',
                invoice_id=invoice.id
            )

        except ValueError as error:

            messages.error(
                request,
                str(error)
            )

            return redirect(
                'create_invoice'
            )

        except Product.DoesNotExist:

            messages.error(
                request,
                'Selected product does not exist.'
            )

            return redirect(
                'create_invoice'
            )

    return render(
        request,
        'billing/create_invoice.html',
        {
            'customers': customers,
            'products': products,
        }
    )

@login_required
def create_quotation(request):

    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':

        customer_id = request.POST.get(
            'customer'
        )

        quotation_number = request.POST.get(
            'quotation_number'
        )

        quotation_date = request.POST.get(
            'quotation_date'
        )

        valid_until = request.POST.get(
            'valid_until'
        )

        discount = request.POST.get(
            'discount'
        ) or 0

        notes = request.POST.get(
            'notes'
        )

        if not quotation_number:

            messages.error(
                request,
                'Quotation number is required.'
            )

            return redirect(
                'create_quotation'
            )

        if Quotation.objects.filter(
            quotation_number=quotation_number
        ).exists():

            messages.error(
                request,
                'Quotation number already exists.'
            )

            return redirect(
                'create_quotation'
            )

        product_ids = request.POST.getlist(
            'product[]'
        )

        quantities = request.POST.getlist(
            'quantity[]'
        )

        prices = request.POST.getlist(
            'price[]'
        )

        if not product_ids:

            messages.error(
                request,
                'Please add at least one product.'
            )

            return redirect(
                'create_quotation'
            )

        with transaction.atomic():

            quotation = Quotation.objects.create(

                quotation_number=quotation_number,

                customer_id=customer_id,

                quotation_date=quotation_date,

                valid_until=valid_until or None,

                discount=discount,

                notes=notes,

            )

            for product_id, quantity, price in zip(
                product_ids,
                quantities,
                prices
            ):

                product = get_object_or_404(
                    Product,
                    id=product_id
                )

                QuotationItem.objects.create(

                    quotation=quotation,

                    product=product,

                    quantity=quantity,

                    price=price,

                )

        messages.success(
            request,
            'Quotation created successfully.'
        )

        return redirect(
            'quotation_detail',
            quotation_id=quotation.id
        )

    return render(
        request,
        'billing/create_quotation.html',
        {
            'customers': customers,
            'products': products,
        }
    )

@login_required
def quotation_list(request):

    quotations = Quotation.objects.select_related(
        'customer'
    ).order_by(
        '-quotation_date',
        '-id'
    )

    return render(
        request,
        'billing/quotation_list.html',
        {
            'quotations': quotations
        }
    )

@login_required
def quotation_detail(
    request,
    quotation_id
):

    quotation = get_object_or_404(
        Quotation.objects.select_related(
            'customer'
        ),
        id=quotation_id
    )

    items = quotation.items.select_related(
        'product'
    )

    return render(
        request,
        'billing/quotation_detail.html',
        {
            'quotation': quotation,
            'items': items,
        }
    )

@login_required
def invoice_list(request):

    invoices = Invoice.objects.select_related(
        'customer'
    ).order_by(
        '-invoice_date',
        '-id'
    )

    search = request.GET.get('search', '')

    if search:
        invoices = invoices.filter(
            invoice_number__icontains=search
        ) | invoices.filter(
            customer__name__icontains=search
        )

    return render(
        request,
        'billing/invoice_list.html',
        {
            'invoices': invoices,
            'search': search,
        }
    )


@login_required
def invoice_detail(request, invoice_id):

    invoice = get_object_or_404(
        Invoice.objects.select_related('customer'),
        id=invoice_id
    )

    items = invoice.items.select_related(
        'product'
    ).all()

    return render(
        request,
        'billing/invoice_detail.html',
        {
            'invoice': invoice,
            'items': items,
        }
    )


@login_required
def invoice_print(request, invoice_id):

    invoice = get_object_or_404(
        Invoice.objects.select_related('customer'),
        id=invoice_id
    )

    items = invoice.items.select_related(
        'product'
    ).all()

    return render(
        request,
        'billing/invoice_print.html',
        {
            'invoice': invoice,
            'items': items,
        }
    )