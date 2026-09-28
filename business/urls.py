from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [

    # =====================================================
    # PUBLIC WEBSITE
    # =====================================================

    path('', views.home, name='home'),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'services/',
        views.services,
        name='services'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),


    # =====================================================
    # ADMIN
    # =====================================================

    path(
        'admin/',
        admin.site.urls
    ),


    # =====================================================
    # ACCOUNTS
    # =====================================================

    path(
        'account/',
        include('accounts.urls')
    ),


    # =====================================================
    # BUSINESS MODULES
    # =====================================================

    path(
        'customers/',
        include('customers.urls')
    ),

    path(
        'products/manage/',
        include('products.urls')
    ),

    path(
        'billing/',
        include('billing.urls')
    ),

    path(
        'payments/',
        include('payments.urls')
    ),

    path(
        'expenses/',
        include('expenses.urls')
    ),

    path(
        'reports/',
        include('reports.urls')
    ),
]