from django.shortcuts import render


# =========================================================
# PUBLIC WEBSITE
# =========================================================

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def products(request):
    return render(request, 'products.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')