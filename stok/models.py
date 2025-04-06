from django.db import models
from django.contrib.auth.models import User
from uretim.models import Product
from hayvan.models import AnimalType

class Category(models.Model):
    """Category model for inventory items"""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name="subcategories", verbose_name="Üst Kategori")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']

class Supplier(models.Model):
    """Supplier model for inventory items"""
    name = models.CharField(max_length=200, verbose_name="Tedarikçi Adı")
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name="İlgili Kişi")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True, verbose_name="E-posta")
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    website = models.URLField(blank=True, null=True, verbose_name="Web Sitesi")
    tax_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Vergi No")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tedarikçi"
        verbose_name_plural = "Tedarikçiler"
        ordering = ['name']

class UnitOfMeasure(models.Model):
    """Unit of measure for inventory items"""
    name = models.CharField(max_length=50, verbose_name="Birim Adı")
    abbreviation = models.CharField(max_length=10, verbose_name="Kısaltma")
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
    
    class Meta:
        verbose_name = "Ölçü Birimi"
        verbose_name_plural = "Ölçü Birimleri"
        ordering = ['name']

class InventoryItem(models.Model):
    """Base model for all inventory items"""
    ITEM_TYPES = [
        ('seed', 'Tohum'),
        ('fertilizer', 'Gübre'),
        ('pesticide', 'Zirai İlaç'),
        ('animal_feed', 'Hayvan Yemi'),
        ('medicine', 'İlaç/Aşı'),
        ('equipment', 'Ekipman'),
        ('spare_part', 'Yedek Parça'),
        ('fuel', 'Yakıt'),
        ('product', 'Ürün'),
        ('other', 'Diğer'),
    ]

    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, verbose_name="Ürün Tipi")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name="inventory_items", verbose_name="Kategori")
    sku = models.CharField(max_length=50, blank=True, null=True, verbose_name="Stok Kodu")
    barcode = models.CharField(max_length=50, blank=True, null=True, verbose_name="Barkod")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT, 
                             related_name="inventory_items", verbose_name="Birim")
    min_stock_level = models.DecimalField(max_digits=10, decimal_places=2, default=0, 
                                         verbose_name="Minimum Stok Seviyesi")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name="inventory_items", verbose_name="Tedarikçi")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                        verbose_name="Alış Fiyatı")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                    verbose_name="Satış Fiyatı")
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18, 
                                  verbose_name="KDV Oranı (%)")
    image = models.ImageField(upload_to='inventory/', blank=True, null=True, verbose_name="Resim")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory_items", 
                             verbose_name="Sahip")
    
    # For seeds
    related_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="inventory_items", verbose_name="İlişkili Ürün")
    
    # For animal feed
    related_animal_type = models.ForeignKey(AnimalType, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name="inventory_items", verbose_name="İlişkili Hayvan Türü")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Stok Kalemi"
        verbose_name_plural = "Stok Kalemleri"
        ordering = ['name']

class StockTransaction(models.Model):
    """Records all stock transactions (in/out)"""
    TRANSACTION_TYPES = [
        ('purchase', 'Satın Alma'),
        ('sale', 'Satış'),
        ('consumption', 'Tüketim'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Stok Düzeltme'),
        ('return_in', 'İade (Giriş)'),
        ('return_out', 'İade (Çıkış)'),
        ('initial', 'Başlangıç Girişi'),
    ]
    
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, 
                            related_name="transactions", verbose_name="Ürün")
    transaction_date = models.DateTimeField(verbose_name="İşlem Tarihi")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="İşlem Tipi")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Miktar")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                    verbose_name="Birim Fiyat")
    reference_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Referans No")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name="transactions", verbose_name="Tedarikçi")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name="stock_transactions", verbose_name="Oluşturan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.item.name} - {self.get_transaction_type_display()} - {self.quantity} {self.item.unit.abbreviation}"
    
    class Meta:
        verbose_name = "Stok Hareketi"
        verbose_name_plural = "Stok Hareketleri"
        ordering = ['-transaction_date']

class Warehouse(models.Model):
    """Storage locations model"""
    name = models.CharField(max_length=100, verbose_name="Depo Adı")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Konum")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="warehouses", 
                             verbose_name="Sahip")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Depo"
        verbose_name_plural = "Depolar"
        ordering = ['name']

class InventoryLocation(models.Model):
    """Records current stock level at each location"""
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, 
                           related_name="inventory_locations", verbose_name="Ürün")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, 
                                related_name="inventory_items", verbose_name="Depo")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, 
                                  verbose_name="Stok Miktarı")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")
    
    def __str__(self):
        return f"{self.item.name} - {self.warehouse.name}: {self.quantity} {self.item.unit.abbreviation}"
    
    class Meta:
        verbose_name = "Stok Konumu"
        verbose_name_plural = "Stok Konumları"
        unique_together = ['item', 'warehouse']
        ordering = ['warehouse', 'item']
