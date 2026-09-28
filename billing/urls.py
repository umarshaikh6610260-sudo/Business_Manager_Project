# from django.urls import path

# from .views import (
#     create_invoice,
#     invoice_list,
#     invoice_detail,
#     invoice_print,
# )

# urlpatterns = [

#     path(
#         '',
#         invoice_list,
#         name='invoice_list'
#     ),

#     path(
#         'create/',
#         create_invoice,
#         name='create_invoice'
#     ),

#     path(
#         '<int:invoice_id>/',
#         invoice_detail,
#         name='invoice_detail'
#     ),

#     path(
#         '<int:invoice_id>/print/',
#         invoice_print,
#         name='invoice_print'
#     ),
# ]

from django.urls import path

from .views import (
    create_invoice,
    create_quotation,
    quotation_list,
    quotation_detail,
    invoice_list,
    invoice_detail,
    invoice_print,
)



urlpatterns = [

    path(
        '',
        invoice_list,
        name='invoice_list'
    ),

    path(
        'create/',
        create_invoice,
        name='create_invoice'
    ),

    path(
    'quotations/',
    quotation_list,
    name='quotation_list'
),

path(
    'quotations/create/',
    create_quotation,
    name='create_quotation'
),

path(
    'quotations/<int:quotation_id>/',
    quotation_detail,
    name='quotation_detail'
),

    path(
        '<int:invoice_id>/',
        invoice_detail,
        name='invoice_detail'
    ),

    path(
        '<int:invoice_id>/print/',
        invoice_print,
        name='invoice_print'
    ),

]