from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Transaction, Invoice, BankAccount, AccountCategory, Customer, Budget
from .forms import AccountCategoryForm

# Create your views here.

@login_required
def transaction_list(request):
    """Finans işlemlerini listeler"""
    transactions = Transaction.objects.all().order_by('-transaction_date')
    return render(request, 'finans/transaction_list.html', {
        'transactions': transactions
    })

@login_required
def invoice_list(request):
    """Faturaları listeler"""
    invoices = Invoice.objects.all().order_by('-invoice_date')
    return render(request, 'finans/invoice_list.html', {
        'invoices': invoices
    })

@login_required
def invoice_create(request):
    """Yeni fatura oluşturur"""
    if request.method == 'POST':
        # Form işleme mantığı burada olacak
        messages.success(request, 'Fatura başarıyla oluşturuldu.')
        return redirect('finans:invoice_list')
    return render(request, 'finans/invoice_form.html', {
        'title': 'Yeni Fatura Oluştur'
    })

@login_required
def bank_account_list(request):
    """Banka hesaplarını listeler"""
    bank_accounts = BankAccount.objects.all().order_by('bank_name')
    return render(request, 'finans/bank_account_list.html', {
        'bank_accounts': bank_accounts
    })

@login_required
def account_category_list(request):
    """Hesap kategorilerini listeler"""
    categories = AccountCategory.objects.all()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'finans/account_category_list.html', {'categories': page_obj, 'is_paginated': True})

@login_required
def account_category_create(request):
    if request.method == 'POST':
        form = AccountCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hesap kategorisi başarıyla oluşturuldu.')
            return redirect('finans:account_category_list')
    else:
        form = AccountCategoryForm()
    return render(request, 'finans/account_category_form.html', {'form': form})

@login_required
def account_category_update(request, pk):
    category = get_object_or_404(AccountCategory, pk=pk)
    if request.method == 'POST':
        form = AccountCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hesap kategorisi başarıyla güncellendi.')
            return redirect('finans:account_category_list')
    else:
        form = AccountCategoryForm(instance=category)
    return render(request, 'finans/account_category_form.html', {'form': form})

@login_required
def account_category_delete(request, pk):
    category = get_object_or_404(AccountCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Hesap kategorisi başarıyla silindi.')
        return redirect('finans:account_category_list')
    return render(request, 'finans/account_category_confirm_delete.html', {'category': category})

@login_required
def customer_list(request):
    """Müşterileri listeler"""
    customers = Customer.objects.all().order_by('name')
    return render(request, 'finans/customer_list.html', {
        'customers': customers
    })

@login_required
def budget_list(request):
    """Bütçe planlarını listeler"""
    budgets = Budget.objects.all().order_by('-year', '-month')
    return render(request, 'finans/budget_list.html', {
        'budgets': budgets
    })
