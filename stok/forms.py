from django import forms
from .models import Category, Supplier, UnitOfMeasure, Warehouse, InventoryItem, StockTransaction

class UnitForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['name', 'abbreviation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'abbreviation': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'name': 'Birim Adı',
            'abbreviation': 'Kısaltma',
        }

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'description', 'address', 'capacity', 'manager', 'phone', 'email', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Depo adı'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Depo açıklaması'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Depo adresi'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Depo kapasitesi (m²)'}),
            'manager': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Depo sorumlusu'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon numarası'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta adresi'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'name': 'Depo Adı',
            'description': 'Açıklama',
            'address': 'Adres',
            'capacity': 'Kapasite (m²)',
            'manager': 'Sorumlu',
            'phone': 'Telefon',
            'email': 'E-posta',
            'is_active': 'Aktif'
        }
        help_texts = {
            'capacity': 'Deponun toplam kullanılabilir alanı (metrekare cinsinden)',
            'is_active': 'Depo aktif olarak kullanılıyor mu?'
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'name', 'item_type', 'category', 'sku', 'barcode', 'description',
            'unit', 'min_stock_level', 'supplier', 'purchase_price', 'sale_price',
            'vat_rate', 'image', 'is_active', 'notes', 'related_product',
            'related_animal_type'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'item_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unit': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'min_stock_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'vat_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'related_product': forms.Select(attrs={'class': 'form-control'}),
            'related_animal_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Ürün Adı',
            'item_type': 'Ürün Tipi',
            'category': 'Kategori',
            'sku': 'Stok Kodu',
            'barcode': 'Barkod',
            'description': 'Açıklama',
            'unit': 'Birim',
            'min_stock_level': 'Minimum Stok Seviyesi',
            'supplier': 'Tedarikçi',
            'purchase_price': 'Alış Fiyatı',
            'sale_price': 'Satış Fiyatı',
            'vat_rate': 'KDV Oranı (%)',
            'image': 'Resim',
            'is_active': 'Aktif',
            'notes': 'Notlar',
            'related_product': 'İlişkili Ürün',
            'related_animal_type': 'İlişkili Hayvan Türü',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True)
        self.fields['unit'].queryset = UnitOfMeasure.objects.all()

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = [
            'item', 'transaction_date', 'transaction_type', 'quantity',
            'unit_price', 'reference_no', 'supplier', 'notes'
        ]
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'transaction_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'required': True,
                'type': 'datetime-local'
            }),
            'transaction_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'reference_no': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'item': 'Ürün',
            'transaction_date': 'İşlem Tarihi',
            'transaction_type': 'İşlem Tipi',
            'quantity': 'Miktar',
            'unit_price': 'Birim Fiyat',
            'reference_no': 'Referans No',
            'supplier': 'Tedarikçi',
            'notes': 'Notlar',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = InventoryItem.objects.filter(is_active=True)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True) 