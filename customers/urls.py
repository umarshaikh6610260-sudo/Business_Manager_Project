from django.urls import path

from .views import (
    customer_list,
    add_customer,
    edit_customer,
    delete_customer,
    customer_detail,
    follow_up_list,
)


urlpatterns = [

    path(
        '',
        customer_list,
        name='customer_list'
    ),

    path(
        'add/',
        add_customer,
        name='add_customer'
    ),

    path(
        'edit/<int:customer_id>/',
        edit_customer,
        name='edit_customer'
    ),

    path(
        'delete/<int:customer_id>/',
        delete_customer,
        name='delete_customer'
    ),

    path(
        'follow-ups/',
        follow_up_list,
        name='follow_up_list'
    ),

    path(
    '<int:customer_id>/',
    customer_detail,
    name='customer_detail'
    ),

]