from django.db import models
from arazi.models import Parcel

class Product(models.Model):
    """Model for products grown/produced on the farm"""
    name = models.CharField(max_length=100, verbose_name="Ürün Adı")
    type = models.CharField(max_length=100, verbose_name="Tür", blank=True, null=True)
    variety = models.CharField(max_length=100, verbose_name="Çeşit", blank=True, null=True)
    growing_time = models.PositiveIntegerField(verbose_name="Yetişme Süresi (Gün)", blank=True, null=True)
    planting_interval = models.CharField(max_length=200, verbose_name="Ekim Aralığı", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    image = models.ImageField(upload_to='products/', verbose_name="Fotoğraf", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ['name']

class Seed(models.Model):
    """Model for seeds used on the farm"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="seeds", verbose_name="Ürün")
    brand = models.CharField(max_length=100, verbose_name="Marka", blank=True, null=True)
    certificate_no = models.CharField(max_length=100, verbose_name="Sertifika No", blank=True, null=True)
    lot_no = models.CharField(max_length=100, verbose_name="Lot No", blank=True, null=True)
    supplier = models.CharField(max_length=200, verbose_name="Tedarikçi", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.product.name} - {self.brand}" if self.brand else self.product.name
    
    class Meta:
        verbose_name = "Tohum"
        verbose_name_plural = "Tohumlar"
        ordering = ['product__name', 'brand']

class PlantingPlan(models.Model):
    """Model for planned planting activities"""
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name="planting_plans", verbose_name="Parsel")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="planting_plans", verbose_name="Ürün")
    planned_planting_date = models.DateField(verbose_name="Planlanan Ekim Tarihi")
    planned_harvest_date = models.DateField(verbose_name="Planlanan Hasat Tarihi", blank=True, null=True)
    planned_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Planlanan Tohum Miktarı (kg)", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    is_completed = models.BooleanField(default=False, verbose_name="Tamamlandı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.parcel} - {self.product} ({self.planned_planting_date})"
    
    class Meta:
        verbose_name = "Ekim Planı"
        verbose_name_plural = "Ekim Planları"
        ordering = ['planned_planting_date']

class Planting(models.Model):
    """Model for actual planting activities"""
    planting_plan = models.OneToOneField(PlantingPlan, on_delete=models.SET_NULL, related_name="planting", verbose_name="Ekim Planı", blank=True, null=True)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name="plantings", verbose_name="Parsel")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="plantings", verbose_name="Ürün")
    seed = models.ForeignKey(Seed, on_delete=models.SET_NULL, related_name="plantings", verbose_name="Tohum", blank=True, null=True)
    planting_date = models.DateField(verbose_name="Ekim Tarihi")
    planting_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ekim Alanı (Dönüm)", blank=True, null=True)
    seed_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tohum Miktarı (kg)", blank=True, null=True)
    planting_method = models.CharField(max_length=100, verbose_name="Ekim Yöntemi", blank=True, null=True)
    planting_depth = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Ekim Derinliği (cm)", blank=True, null=True)
    row_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Sıra Arası Mesafe (cm)", blank=True, null=True)
    estimated_harvest_date = models.DateField(verbose_name="Tahmini Hasat Tarihi", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.parcel} - {self.product} ({self.planting_date})"
    
    class Meta:
        verbose_name = "Ekim"
        verbose_name_plural = "Ekimler"
        ordering = ['-planting_date']

class FertilizationRecord(models.Model):
    """Model for fertilization activities"""
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE, related_name="fertilization_records", verbose_name="Ekim")
    fertilization_date = models.DateField(verbose_name="Gübreleme Tarihi")
    fertilizer_name = models.CharField(max_length=100, verbose_name="Gübre Adı")
    fertilizer_type = models.CharField(max_length=100, verbose_name="Gübre Türü", blank=True, null=True)
    application_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Uygulama Miktarı (kg/dönüm)", blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toplam Miktar (kg)", blank=True, null=True)
    application_method = models.CharField(max_length=100, verbose_name="Uygulama Yöntemi", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.planting} - {self.fertilizer_name} ({self.fertilization_date})"
    
    class Meta:
        verbose_name = "Gübreleme Kaydı"
        verbose_name_plural = "Gübreleme Kayıtları"
        ordering = ['-fertilization_date']

class PesticideApplication(models.Model):
    """Model for pesticide application activities"""
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE, related_name="pesticide_applications", verbose_name="Ekim")
    application_date = models.DateField(verbose_name="İlaçlama Tarihi")
    pesticide_name = models.CharField(max_length=100, verbose_name="İlaç Adı")
    pesticide_type = models.CharField(max_length=100, verbose_name="İlaç Türü", blank=True, null=True)
    active_ingredient = models.CharField(max_length=100, verbose_name="Etken Madde", blank=True, null=True)
    application_dose = models.CharField(max_length=100, verbose_name="Uygulama Dozu", blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toplam Miktar", blank=True, null=True)
    application_method = models.CharField(max_length=100, verbose_name="Uygulama Yöntemi", blank=True, null=True)
    waiting_period = models.PositiveIntegerField(verbose_name="Bekleme Süresi (Gün)", blank=True, null=True)
    target_pest = models.CharField(max_length=200, verbose_name="Hedef Zararlı", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.planting} - {self.pesticide_name} ({self.application_date})"
    
    class Meta:
        verbose_name = "İlaçlama Kaydı"
        verbose_name_plural = "İlaçlama Kayıtları"
        ordering = ['-application_date']

class Harvest(models.Model):
    """Model for harvest activities"""
    planting = models.OneToOneField(Planting, on_delete=models.CASCADE, related_name="harvest", verbose_name="Ekim")
    harvest_date = models.DateField(verbose_name="Hasat Tarihi")
    harvest_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Hasat Miktarı (kg/ton)")
    yield_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Verim (kg/dönüm)", blank=True, null=True)
    moisture_content = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Nem Oranı (%)", blank=True, null=True)
    quality_class = models.CharField(max_length=50, verbose_name="Kalite Sınıfı", blank=True, null=True)
    harvest_method = models.CharField(max_length=100, verbose_name="Hasat Yöntemi", blank=True, null=True)
    stored_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Depolanan Miktar (kg/ton)", blank=True, null=True)
    sold_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Satılan Miktar (kg/ton)", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.planting.product} - {self.harvest_date}"
    
    class Meta:
        verbose_name = "Hasat"
        verbose_name_plural = "Hasatlar"
        ordering = ['-harvest_date']
        
    def save(self, *args, **kwargs):
        if self.harvest_amount and self.planting.planting_area and self.planting.planting_area > 0:
            self.yield_rate = self.harvest_amount / self.planting.planting_area
        super().save(*args, **kwargs)

class MaintenanceRecord(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
        ('sulama', 'Sulama'),
        ('gubreleme', 'Gübreleme'),
        ('ilaclama', 'İlaçlama'),
        ('yabancı_ot', 'Yabancı Ot Temizliği'),
        ('toprak_hazirligi', 'Toprak Hazırlığı'),
        ('diger', 'Diğer'),
    ]

    planting = models.ForeignKey(Planting, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPE_CHOICES)
    maintenance_date = models.DateField()
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text='Bakım yapılan alan (dekar)')
    weather_condition = models.CharField(max_length=100, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fertilizer = models.CharField(max_length=100, blank=True)
    pesticide = models.CharField(max_length=100, blank=True)
    water_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Su miktarı (m³)')
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    material_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    equipment_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-maintenance_date']
        verbose_name = 'Bakım Kaydı'
        verbose_name_plural = 'Bakım Kayıtları'

    def __str__(self):
        return f"{self.get_maintenance_type_display()} - {self.maintenance_date}"

    def save(self, *args, **kwargs):
        self.total_cost = self.labor_cost + self.material_cost + self.equipment_cost
        super().save(*args, **kwargs)
