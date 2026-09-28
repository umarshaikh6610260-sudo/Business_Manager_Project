from django.urls import path

from .views import (
    product_list,
    add_product,
    edit_product,
    delete_product,
)


urlpatterns = [

    path(
        '',
        product_list,
        name='product_list'
    ),

    path(
        'add/',
        add_product,
        name='add_product'
    ),

    path(
        'edit/<int:product_id>/',
        edit_product,
        name='edit_product'
    ),

    path(
        'delete/<int:product_id>/',
        delete_product,
        name='delete_product'
    ),

]