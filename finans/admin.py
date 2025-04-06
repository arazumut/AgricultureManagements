from django.contrib import admin
from .models import (
    AccountCategory, Customer, BankAccount, Transaction, 
    Invoice, InvoiceItem, Budget, BudgetItem
)

@admin.register(AccountCategory)
class AccountCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_income', 'is_expense', 'is_active']
    list_filter = ['is_income', 'is_expense', 'is_active']
    search_fields = ['name', 'description']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'contact_person', 'phone', 'email', 'address', 'tax_number']
    fieldsets = [
        ('Temel Bilgiler', {'fields': ['name', 'contact_person', 'is_active', 'owner']}),
        ('İletişim Bilgileri', {'fields': ['phone', 'email', 'address']}),
        ('Mali Bilgiler', {'fields': ['tax_number']}),
        ('Diğer', {'fields': ['notes']}),
    ]

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_type', 'bank_name', 'current_balance', 'currency', 'is_active']
    list_filter = ['account_type', 'is_active', 'currency']
    search_fields = ['name', 'bank_name', 'account_number', 'iban']
    readonly_fields = ['current_balance', 'created_at', 'updated_at']
    fieldsets = [
        ('Temel Bilgiler', {'fields': ['name', 'account_type', 'is_active', 'currency', 'owner']}),
        ('Banka Bilgileri', {'fields': ['bank_name', 'branch_name', 'account_number', 'iban']}),
        ('Bakiye Bilgileri', {'fields': ['opening_balance', 'current_balance']}),
        ('Diğer', {'fields': ['description', 'created_at', 'updated_at']}),
    ]

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['description', 'quantity', 'unit_price', 'tax_rate', 'tax_amount', 'discount_amount', 'line_total', 'product', 'animal']
    readonly_fields = ['tax_amount', 'line_total']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'invoice_type', 'invoice_date', 'total_amount', 'paid_amount', 'balance_due', 'status']
    list_filter = ['invoice_type', 'status', 'invoice_date']
    search_fields = ['invoice_number', 'description']
    readonly_fields = ['balance_due', 'created_at', 'updated_at']
    inlines = [InvoiceItemInline]
    fieldsets = [
        ('Fatura Bilgileri', {'fields': ['invoice_number', 'invoice_type', 'invoice_date', 'due_date', 'status']}),
        ('İlişkili Kayıtlar', {'fields': ['customer', 'supplier', 'bank_account', 'category']}),
        ('Tutar Bilgileri', {'fields': ['subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'paid_amount', 'balance_due']}),
        ('Diğer', {'fields': ['notes', 'owner', 'created_at', 'updated_at']}),
    ]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_date', 'transaction_type', 'amount', 'bank_account', 'category', 'status']
    list_filter = ['transaction_type', 'status', 'transaction_date', 'payment_method']
    search_fields = ['description', 'reference_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('İşlem Bilgileri', {'fields': ['transaction_date', 'transaction_type', 'amount', 'status']}),
        ('Hesap Bilgileri', {'fields': ['bank_account', 'category', 'payment_method']}),
        ('İlişkili Kayıtlar', {'fields': ['related_invoice', 'related_product', 'related_animal', 'related_harvest']}),
        ('Diğer', {'fields': ['description', 'reference_number', 'created_by', 'created_at', 'updated_at']}),
    ]

class BudgetItemInline(admin.TabularInline):
    model = BudgetItem
    extra = 1

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BudgetItemInline]
    fieldsets = [
        ('Temel Bilgiler', {'fields': ['name', 'is_active', 'owner']}),
        ('Dönem Bilgileri', {'fields': ['start_date', 'end_date']}),
        ('Diğer', {'fields': ['description', 'created_at', 'updated_at']}),
    ]
