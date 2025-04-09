# Author: Umut Araz
# Date: 2025-04-08

from django.db import models
from django.contrib.auth.models import User
from stok.models import InventoryItem
from hayvan.models import Animal
from uretim.models import Harvest
from django.utils import timezone

class AccountCategory(models.Model):
    """Model for account/transaction categories"""
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Gelir'),
        ('expense', 'Gider'),
        ('other', 'Diğer'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES, default='expense', verbose_name="Kategori Tipi")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Güncellenme Tarihi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Hesap Kategorisi"
        verbose_name_plural = "Hesap Kategorileri"
        ordering = ['name']

class Customer(models.Model):
    """Model for customers (buyers of farm products)"""
    name = models.CharField(max_length=200, verbose_name="Müşteri Adı")
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name="İlgili Kişi")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True, verbose_name="E-posta")
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    tax_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Vergi No")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customers", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"
        ordering = ['name']

class BankAccount(models.Model):
    """Model for bank accounts"""
    ACCOUNT_TYPES = [
        ('checking', 'Vadesiz Hesap'),
        ('savings', 'Vadeli Hesap'),
        ('credit_card', 'Kredi Kartı'),
        ('loan', 'Kredi'),
        ('cash', 'Nakit'),
        ('other', 'Diğer'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Hesap Adı")
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, verbose_name="Hesap Tipi")
    account_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Hesap Numarası")
    bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Banka Adı")
    branch_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Şube Adı")
    iban = models.CharField(max_length=50, blank=True, null=True, verbose_name="IBAN")
    currency = models.CharField(max_length=3, default="TRY", verbose_name="Para Birimi")
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Açılış Bakiyesi")
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Güncel Bakiye")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank_accounts", verbose_name="Sahibi")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"
    
    class Meta:
        verbose_name = "Banka Hesabı"
        verbose_name_plural = "Banka Hesapları"
        ordering = ['name']

class Transaction(models.Model):
    """Model for financial transactions"""
    TRANSACTION_TYPES = [
        ('income', 'Gelir'),
        ('expense', 'Gider'),
        ('transfer', 'Transfer'),
        ('initial', 'Açılış Bakiyesi'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Nakit'),
        ('bank_transfer', 'Havale/EFT'),
        ('credit_card', 'Kredi Kartı'),
        ('check', 'Çek'),
        ('other', 'Diğer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Bekliyor'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    transaction_date = models.DateField(verbose_name="İşlem Tarihi")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="İşlem Tipi")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tutar")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    category = models.ForeignKey(AccountCategory, on_delete=models.SET_NULL, null=True, 
                               related_name="transactions", verbose_name="Kategori")
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, 
                                   related_name="transactions", verbose_name="Hesap")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, 
                                    verbose_name="Ödeme Yöntemi", blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Referans No")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, 
                            default='completed', verbose_name="Durum")
    related_invoice = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name="transactions", verbose_name="İlgili Fatura")
    related_product = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name="finance_transactions", verbose_name="İlgili Ürün")
    related_animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name="transactions", verbose_name="İlgili Hayvan")
    related_harvest = models.ForeignKey(Harvest, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name="transactions", verbose_name="İlgili Hasat")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name="transactions", verbose_name="Oluşturan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} {self.bank_account.currency} ({self.transaction_date})"
    
    class Meta:
        verbose_name = "İşlem"
        verbose_name_plural = "İşlemler"
        ordering = ['-transaction_date', '-created_at']

class Invoice(models.Model):
    """Model for invoices (both sales and purchases)"""
    INVOICE_TYPES = [
        ('sale', 'Satış Faturası'),
        ('purchase', 'Alış Faturası'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Taslak'),
        ('sent', 'Gönderildi'),
        ('paid', 'Ödendi'),
        ('partially_paid', 'Kısmen Ödendi'),
        ('overdue', 'Gecikmiş'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    invoice_number = models.CharField(max_length=50, verbose_name="Fatura Numarası")
    invoice_date = models.DateField(verbose_name="Fatura Tarihi")
    due_date = models.DateField(verbose_name="Son Ödeme Tarihi", blank=True, null=True)
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES, verbose_name="Fatura Tipi")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name="invoices", verbose_name="Müşteri")
    supplier = models.ForeignKey('stok.Supplier', on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name="invoices", verbose_name="Tedarikçi")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Ara Toplam")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Vergi Tutarı")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="İndirim Tutarı")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Toplam Tutar")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Ödenen Tutar")
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Kalan Tutar")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft', verbose_name="Durum")
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name="invoices", verbose_name="Hesap")
    category = models.ForeignKey(AccountCategory, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name="invoices", verbose_name="Kategori")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.invoice_number} - {self.get_invoice_type_display()} ({self.invoice_date})"
    
    class Meta:
        verbose_name = "Fatura"
        verbose_name_plural = "Faturalar"
        ordering = ['-invoice_date']
        
    def save(self, *args, **kwargs):
        self.balance_due = self.total_amount - self.paid_amount
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    """Model for individual line items in an invoice"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items", verbose_name="Fatura")
    description = models.CharField(max_length=255, verbose_name="Açıklama")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Miktar")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Birim Fiyat")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18, verbose_name="Vergi Oranı (%)")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Vergi Tutarı")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="İndirim Tutarı")
    line_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Satır Toplamı")
    product = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name="invoice_items", verbose_name="Ürün")
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name="invoice_items", verbose_name="Hayvan")
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description}"
    
    class Meta:
        verbose_name = "Fatura Kalemi"
        verbose_name_plural = "Fatura Kalemleri"
        
    def save(self, *args, **kwargs):
        self.tax_amount = (self.quantity * self.unit_price) * (self.tax_rate / 100)
        self.line_total = (self.quantity * self.unit_price) + self.tax_amount - self.discount_amount
        super().save(*args, **kwargs)

class Budget(models.Model):
    """Model for budgeting and planning"""
    name = models.CharField(max_length=100, verbose_name="Bütçe Adı")
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(verbose_name="Bitiş Tarihi")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"
    
    class Meta:
        verbose_name = "Bütçe"
        verbose_name_plural = "Bütçeler"
        ordering = ['-start_date']

class BudgetItem(models.Model):
    """Model for individual budget items"""
    ITEM_TYPES = [
        ('income', 'Gelir'),
        ('expense', 'Gider'),
    ]
    
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="items", verbose_name="Bütçe")
    category = models.ForeignKey(AccountCategory, on_delete=models.CASCADE, related_name="budget_items", verbose_name="Kategori")
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES, verbose_name="Kalem Tipi")
    name = models.CharField(max_length=100, verbose_name="Kalem Adı")
    planned_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Planlanan Tutar")
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Gerçekleşen Tutar")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    
    def __str__(self):
        return f"{self.budget.name} - {self.name}"
    
    class Meta:
        verbose_name = "Bütçe Kalemi"
        verbose_name_plural = "Bütçe Kalemleri"
