from django.contrib import admin
from .models import (
    AccountCategory, Customer, BankAccount, Transaction, 
    Invoice, InvoiceItem, Budget, BudgetItem
)

@admin.register(AccountCategory)
class AccountCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category_type', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_person', 'phone', 'email', 'address')
    ordering = ('name',)

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'bank_name', 'account_number', 'current_balance', 'currency', 'is_active')
    list_filter = ('account_type', 'currency', 'is_active')
    search_fields = ('name', 'bank_name', 'account_number', 'iban')
    ordering = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_date', 'transaction_type', 'amount', 'category', 'bank_account', 'status')
    list_filter = ('transaction_type', 'status', 'payment_method', 'category')
    search_fields = ('description', 'reference_number')
    date_hierarchy = 'transaction_date'
    ordering = ('-transaction_date',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'invoice_date', 'invoice_type', 'customer', 'total_amount', 'status')
    list_filter = ('invoice_type', 'status', 'category')
    search_fields = ('invoice_number', 'customer__name', 'notes')
    date_hierarchy = 'invoice_date'
    ordering = ('-invoice_date',)

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price', 'line_total')
    list_filter = ('invoice__invoice_type',)
    search_fields = ('description', 'invoice__invoice_number')
    ordering = ('-invoice__invoice_date',)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('budget', 'category', 'item_type', 'name', 'planned_amount', 'actual_amount')
    list_filter = ('item_type', 'category')
    search_fields = ('name', 'notes')
    ordering = ('budget', 'category')
