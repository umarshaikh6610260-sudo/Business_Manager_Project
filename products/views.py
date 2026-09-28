# from django.shortcuts import render

# # Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product


def product_list(request):

    search = request.GET.get('search', '')

    products = Product.objects.all().order_by('-created_at')

    if search:

        products = products.filter(
            name__icontains=search
        ) | products.filter(
            sku__icontains=search
        ) | products.filter(
            category__icontains=search
        )

    context = {
        'products': products,
        'search': search,
    }

    return render(
        request,
        'products/product_list.html',
        context
    )


def add_product(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        category = request.POST.get('category')
        sku = request.POST.get('sku')
        purchase_price = request.POST.get('purchase_price')
        selling_price = request.POST.get('selling_price')
        stock = request.POST.get('stock')
        minimum_stock = request.POST.get('minimum_stock')
        description = request.POST.get('description')

        Product.objects.create(

            name=name,

            category=category,

            sku=sku,

            purchase_price=purchase_price,

            selling_price=selling_price,

            stock=stock,

            minimum_stock=minimum_stock,

            description=description,

        )

        return redirect('product_list')

    return render(
        request,
        'products/add_product.html'
    )


def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        product.name = request.POST.get('name')

        product.category = request.POST.get('category')

        product.sku = request.POST.get('sku')

        product.purchase_price = request.POST.get(
            'purchase_price'
        )

        product.selling_price = request.POST.get(
            'selling_price'
        )

        product.stock = request.POST.get(
            'stock'
        )

        product.minimum_stock = request.POST.get(
            'minimum_stock'
        )

        product.description = request.POST.get(
            'description'
        )

        product.save()

        return redirect('product_list')

    return render(
        request,
        'products/edit_product.html',
        {
            'product': product
        }
    )


def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        product.delete()

        return redirect('product_list')

    return render(
        request,
        'products/delete_product.html',
        {
            'product': product
        }
    )