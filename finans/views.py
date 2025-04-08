from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction, Invoice, BankAccount, AccountCategory, Customer, Budget

# Create your views here.

@login_required
def transaction_list(request):
    """Finans işlemlerini listeler"""
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'finans/transaction_list.html', {
        'transactions': transactions
    })

@login_required
def invoice_list(request):
    """Faturaları listeler"""
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'finans/invoice_list.html', {
        'invoices': invoices
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
    account_categories = AccountCategory.objects.all().order_by('name')
    return render(request, 'finans/account_category_list.html', {
        'account_categories': account_categories
    })

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
