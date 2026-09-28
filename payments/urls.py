# from django.urls import path

# from .views import (
#     payment_add,
#     payment_history,
# )

# urlpatterns = [

#     path(
#         '',
#         payment_history,
#         name='payment_history'
#     ),

#     path(
#         'add/<int:invoice_id>/',
#         payment_add,
#         name='payment_add'
#     ),

# ]

from django.urls import path

from .views import (
    payment_history,
    add_payment,
)


urlpatterns = [

    path(
        '',
        payment_history,
        name='payment_history'
    ),

    path(
        'add/<int:invoice_id>/',
        add_payment,
        name='payment_add'
    ),

]