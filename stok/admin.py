from django.contrib import admin

from .models import (Category, Supplier, UnitOfMeasure, InventoryItem, StockTransaction, Warehouse, InventoryLocation)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'contact_person', 'phone', 'email', 'address', 'tax_number']
    fieldsets = [
        ('Temel Bilgiler', {'fields': ['name', 'contact_person', 'is_active']}),
        ('İletişim Bilgileri', {'fields': ['phone', 'email', 'address', 'website']}),
        ('Mali Bilgiler', {'fields': ['tax_number']}),
        ('Diğer', {'fields': ['notes']}),
    ]

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']
    search_fields = ['name', 'abbreviation']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'category', 'unit', 'purchase_price', 'sale_price', 'is_active']
    list_filter = ['item_type', 'category', 'is_active', 'supplier']
    search_fields = ['name', 'sku', 'barcode', 'description']
    fieldsets = [
        ('Temel Bilgiler', {'fields': ['name', 'item_type', 'category', 'is_active', 'unit', 'owner']}),
        ('Stok Bilgileri', {'fields': ['sku', 'barcode', 'min_stock_level']}),
        ('Fiyat Bilgileri', {'fields': ['purchase_price', 'sale_price', 'vat_rate']}),
        ('Tedarik Bilgileri', {'fields': ['supplier']}),
        ('Ürün İlişkileri', {'fields': ['related_product', 'related_animal_type']}),
        ('Diğer', {'fields': ['description', 'notes', 'image']}),
    ]

class InventoryLocationInline(admin.TabularInline):
    model = InventoryLocation
    extra = 1

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['item', 'transaction_date', 'transaction_type', 'quantity', 'unit_price', 'supplier']
    list_filter = ['transaction_type', 'transaction_date', 'supplier']
    search_fields = ['item__name', 'reference_no', 'notes']
    date_hierarchy = 'transaction_date'
    fieldsets = [
        ('İşlem Bilgileri', {'fields': ['item', 'transaction_date', 'transaction_type', 'quantity', 'unit_price']}),
        ('Tedarik Bilgileri', {'fields': ['supplier', 'reference_no']}),
        ('Diğer', {'fields': ['notes', 'created_by']}),
    ]

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'location', 'description']
    inlines = [InventoryLocationInline]
    fieldsets = [
        ('Temel Bilgiler', {'fields': ['name', 'location', 'is_active', 'owner']}),
        ('Diğer', {'fields': ['description']}),
    ]

@admin.register(InventoryLocation)
class InventoryLocationAdmin(admin.ModelAdmin):
    list_display = ['item', 'warehouse', 'quantity', 'last_updated']
    list_filter = ['warehouse', 'item__category']
    search_fields = ['item__name', 'warehouse__name']
