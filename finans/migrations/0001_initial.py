# Generated by Django 5.2 on 2025-04-06 13:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hayvan', '0001_initial'),
        ('stok', '0001_initial'),
        ('uretim', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Kategori Adı')),
                ('is_income', models.BooleanField(verbose_name='Gelir mi?')),
                ('is_expense', models.BooleanField(verbose_name='Gider mi?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
            ],
            options={
                'verbose_name': 'Hesap Kategorisi',
                'verbose_name_plural': 'Hesap Kategorileri',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Hesap Adı')),
                ('account_type', models.CharField(choices=[('checking', 'Vadesiz Hesap'), ('savings', 'Vadeli Hesap'), ('credit_card', 'Kredi Kartı'), ('loan', 'Kredi'), ('cash', 'Nakit'), ('other', 'Diğer')], max_length=20, verbose_name='Hesap Tipi')),
                ('account_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Hesap Numarası')),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Banka Adı')),
                ('branch_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Şube Adı')),
                ('iban', models.CharField(blank=True, max_length=50, null=True, verbose_name='IBAN')),
                ('currency', models.CharField(default='TRY', max_length=3, verbose_name='Para Birimi')),
                ('opening_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Açılış Bakiyesi')),
                ('current_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Güncel Bakiye')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to=settings.AUTH_USER_MODEL, verbose_name='Sahibi')),
            ],
            options={
                'verbose_name': 'Banka Hesabı',
                'verbose_name_plural': 'Banka Hesapları',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Bütçe Adı')),
                ('start_date', models.DateField(verbose_name='Başlangıç Tarihi')),
                ('end_date', models.DateField(verbose_name='Bitiş Tarihi')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL, verbose_name='Sahibi')),
            ],
            options={
                'verbose_name': 'Bütçe',
                'verbose_name_plural': 'Bütçeler',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='BudgetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('income', 'Gelir'), ('expense', 'Gider')], max_length=10, verbose_name='Kalem Tipi')),
                ('name', models.CharField(max_length=100, verbose_name='Kalem Adı')),
                ('planned_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Planlanan Tutar')),
                ('actual_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Gerçekleşen Tutar')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notlar')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='finans.budget', verbose_name='Bütçe')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget_items', to='finans.accountcategory', verbose_name='Kategori')),
            ],
            options={
                'verbose_name': 'Bütçe Kalemi',
                'verbose_name_plural': 'Bütçe Kalemleri',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Müşteri Adı')),
                ('contact_person', models.CharField(blank=True, max_length=100, null=True, verbose_name='İlgili Kişi')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefon')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-posta')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adres')),
                ('tax_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Vergi No')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notlar')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL, verbose_name='Sahibi')),
            ],
            options={
                'verbose_name': 'Müşteri',
                'verbose_name_plural': 'Müşteriler',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=50, verbose_name='Fatura Numarası')),
                ('invoice_date', models.DateField(verbose_name='Fatura Tarihi')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Son Ödeme Tarihi')),
                ('invoice_type', models.CharField(choices=[('sale', 'Satış Faturası'), ('purchase', 'Alış Faturası')], max_length=10, verbose_name='Fatura Tipi')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Ara Toplam')),
                ('tax_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Vergi Tutarı')),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='İndirim Tutarı')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Toplam Tutar')),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Ödenen Tutar')),
                ('balance_due', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Kalan Tutar')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notlar')),
                ('status', models.CharField(choices=[('draft', 'Taslak'), ('sent', 'Gönderildi'), ('paid', 'Ödendi'), ('partially_paid', 'Kısmen Ödendi'), ('overdue', 'Gecikmiş'), ('cancelled', 'İptal Edildi')], default='draft', max_length=15, verbose_name='Durum')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('bank_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='finans.bankaccount', verbose_name='Hesap')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='finans.accountcategory', verbose_name='Kategori')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='finans.customer', verbose_name='Müşteri')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to=settings.AUTH_USER_MODEL, verbose_name='Sahibi')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='stok.supplier', verbose_name='Tedarikçi')),
            ],
            options={
                'verbose_name': 'Fatura',
                'verbose_name_plural': 'Faturalar',
                'ordering': ['-invoice_date'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Açıklama')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Miktar')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Birim Fiyat')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=18, max_digits=5, verbose_name='Vergi Oranı (%)')),
                ('tax_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Vergi Tutarı')),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='İndirim Tutarı')),
                ('line_total', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Satır Toplamı')),
                ('animal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_items', to='hayvan.animal', verbose_name='Hayvan')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='finans.invoice', verbose_name='Fatura')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_items', to='stok.inventoryitem', verbose_name='Ürün')),
            ],
            options={
                'verbose_name': 'Fatura Kalemi',
                'verbose_name_plural': 'Fatura Kalemleri',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(verbose_name='İşlem Tarihi')),
                ('transaction_type', models.CharField(choices=[('income', 'Gelir'), ('expense', 'Gider'), ('transfer', 'Transfer'), ('initial', 'Açılış Bakiyesi')], max_length=10, verbose_name='İşlem Tipi')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Tutar')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('payment_method', models.CharField(blank=True, choices=[('cash', 'Nakit'), ('bank_transfer', 'Havale/EFT'), ('credit_card', 'Kredi Kartı'), ('check', 'Çek'), ('other', 'Diğer')], max_length=20, null=True, verbose_name='Ödeme Yöntemi')),
                ('reference_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Referans No')),
                ('status', models.CharField(choices=[('pending', 'Bekliyor'), ('completed', 'Tamamlandı'), ('cancelled', 'İptal Edildi')], default='completed', max_length=10, verbose_name='Durum')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='finans.bankaccount', verbose_name='Hesap')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='finans.accountcategory', verbose_name='Kategori')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan')),
                ('related_animal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='hayvan.animal', verbose_name='İlgili Hayvan')),
                ('related_harvest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='uretim.harvest', verbose_name='İlgili Hasat')),
                ('related_invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='finans.invoice', verbose_name='İlgili Fatura')),
                ('related_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='finance_transactions', to='stok.inventoryitem', verbose_name='İlgili Ürün')),
            ],
            options={
                'verbose_name': 'İşlem',
                'verbose_name_plural': 'İşlemler',
                'ordering': ['-transaction_date', '-created_at'],
            },
        ),
    ]
