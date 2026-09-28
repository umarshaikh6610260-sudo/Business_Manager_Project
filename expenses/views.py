# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required

# from .models import Expense

# from accounts.decorators import role_required


# @login_required
# def expense_list(request):

#     expenses = Expense.objects.order_by(
#         '-expense_date',
#         '-id'
#     )

#     return render(
#         request,
#         'expenses/expense_list.html',
#         {
#             'expenses': expenses
#         }
#     )


# @login_required
# @role_required('owner', 'accountant')
# def add_expense(request):

#     if request.method == 'POST':

#         title = request.POST.get('title')
#         category = request.POST.get('category')
#         amount = request.POST.get('amount')
#         expense_date = request.POST.get('expense_date')
#         description = request.POST.get('description')

#         Expense.objects.create(
#             title=title,
#             category=category,
#             amount=amount,
#             expense_date=expense_date,
#             description=description,
#         )

#         messages.success(
#             request,
#             'Expense added successfully.'
#         )

#         return redirect('expense_list')

#     return render(
#         request,
#         'expenses/add_expense.html'
#     )


# @login_required
# @role_required('owner', 'accountant')
# def edit_expense(request, expense_id):

#     expense = get_object_or_404(
#         Expense,
#         id=expense_id
#     )

#     if request.method == 'POST':

#         expense.title = request.POST.get('title')
#         expense.category = request.POST.get('category')
#         expense.amount = request.POST.get('amount')
#         expense.expense_date = request.POST.get('expense_date')
#         expense.description = request.POST.get('description')

#         expense.save()

#         messages.success(
#             request,
#             'Expense updated successfully.'
#         )

#         return redirect('expense_list')

#     return render(
#         request,
#         'expenses/edit_expense.html',
#         {
#             'expense': expense
#         }
#     )


# @login_required
# @role_required('owner', 'accountant')
# def delete_expense(request, expense_id):

#     expense = get_object_or_404(
#         Expense,
#         id=expense_id
#     )

#     if request.method == 'POST':

#         expense.delete()

#         messages.success(
#             request,
#             'Expense deleted successfully.'
#         )

#         return redirect('expense_list')

#     return render(
#         request,
#         'expenses/delete_expense.html',
#         {
#             'expense': expense
#         }
#     )

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Expense


@login_required
def expense_list(request):

    expenses = Expense.objects.order_by(
        '-expense_date',
        '-id'
    )

    return render(
        request,
        'expenses/expense_list.html',
        {
            'expenses': expenses
        }
    )


@login_required
def add_expense(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        expense_date = request.POST.get('expense_date')
        description = request.POST.get('description')

        Expense.objects.create(
            title=title,
            category=category,
            amount=amount,
            expense_date=expense_date,
            description=description
        )

        messages.success(
            request,
            'Expense added successfully.'
        )

        return redirect('expense_list')

    return render(
        request,
        'expenses/add_expense.html'
    )


@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    if request.method == 'POST':

        expense.title = request.POST.get('title')
        expense.category = request.POST.get('category')
        expense.amount = request.POST.get('amount')
        expense.expense_date = request.POST.get('expense_date')
        expense.description = request.POST.get('description')

        expense.save()

        messages.success(
            request,
            'Expense updated successfully.'
        )

        return redirect('expense_list')

    return render(
        request,
        'expenses/edit_expense.html',
        {
            'expense': expense
        }
    )


@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    if request.method == 'POST':

        expense.delete()

        messages.success(
            request,
            'Expense deleted successfully.'
        )

        return redirect('expense_list')

    return render(
        request,
        'expenses/delete_expense.html',
        {
            'expense': expense
        }
    )