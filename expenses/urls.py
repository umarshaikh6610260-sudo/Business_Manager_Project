# from django.urls import path

# from .views import (
#     expense_list,
#     add_expense,
#     edit_expense,
#     delete_expense,
# )

# urlpatterns = [

#     path(
#         '',
#         expense_list,
#         name='expense_list'
#     ),

#     path(
#         'add/',
#         add_expense,
#         name='add_expense'
#     ),

#     path(
#         'edit/<int:expense_id>/',
#         edit_expense,
#         name='edit_expense'
#     ),

#     path(
#         'delete/<int:expense_id>/',
#         delete_expense,
#         name='delete_expense'
#     ),

# ]

from django.urls import path

from .views import (
    expense_list,
    add_expense,
    edit_expense,
    delete_expense,
)


urlpatterns = [

    path(
        '',
        expense_list,
        name='expense_list'
    ),

    path(
        'add/',
        add_expense,
        name='add_expense'
    ),

    path(
        'edit/<int:expense_id>/',
        edit_expense,
        name='edit_expense'
    ),

    path(
        'delete/<int:expense_id>/',
        delete_expense,
        name='delete_expense'
    ),

]