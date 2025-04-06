from django.db import models
from django.contrib.auth.models import User
from uretim.models import Product, Planting, Harvest
from hayvan.models import Animal, AnimalType
from arazi.models import Land, Parcel

class Dashboard(models.Model):
    """Model for customizable user dashboards"""
    name = models.CharField(max_length=100, verbose_name="Dashboard Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    layout = models.JSONField(blank=True, null=True, verbose_name="Yerleşim")
    is_default = models.BooleanField(default=False, verbose_name="Varsayılan mı?")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dashboards", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.name} - {self.owner.username}"
    
    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboards"
        ordering = ['owner', 'name']

class Report(models.Model):
    """Model for saved reports"""
    REPORT_TYPES = [
        ('yield', 'Verim Raporu'),
        ('profit_loss', 'Kar/Zarar Raporu'),
        ('inventory', 'Envanter Raporu'),
        ('animal_performance', 'Hayvan Performans Raporu'),
        ('cost_analysis', 'Maliyet Analizi'),
        ('weather', 'Hava Durumu Raporu'),
        ('task', 'Görev Raporu'),
        ('custom', 'Özel Rapor'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Rapor Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, verbose_name="Rapor Tipi")
    query_parameters = models.JSONField(blank=True, null=True, verbose_name="Sorgu Parametreleri")
    chart_settings = models.JSONField(blank=True, null=True, verbose_name="Grafik Ayarları")
    visualization_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Görselleştirme Tipi")
    is_scheduled = models.BooleanField(default=False, verbose_name="Zamanlanmış mı?")
    schedule = models.JSONField(blank=True, null=True, verbose_name="Zamanlama")
    recipients = models.JSONField(blank=True, null=True, verbose_name="Alıcılar")
    last_run = models.DateTimeField(blank=True, null=True, verbose_name="Son Çalıştırma")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"
    
    class Meta:
        verbose_name = "Rapor"
        verbose_name_plural = "Raporlar"
        ordering = ['owner', 'name']

class ReportResult(models.Model):
    """Model for stored report results"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="results", verbose_name="Rapor")
    run_date = models.DateTimeField(auto_now_add=True, verbose_name="Çalıştırma Tarihi")
    data = models.JSONField(verbose_name="Veri")
    summary = models.TextField(blank=True, null=True, verbose_name="Özet")
    status = models.CharField(max_length=20, verbose_name="Durum")
    file_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dosya Yolu")
    
    def __str__(self):
        return f"{self.report.name} - {self.run_date}"
    
    class Meta:
        verbose_name = "Rapor Sonucu"
        verbose_name_plural = "Rapor Sonuçları"
        ordering = ['-run_date']

class ProductPerformanceMetric(models.Model):
    """Model for tracking product performance metrics"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="performance_metrics", verbose_name="Ürün")
    year = models.PositiveIntegerField(verbose_name="Yıl")
    season = models.CharField(max_length=20, blank=True, null=True, verbose_name="Sezon")
    total_planted_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Toplam Ekim Alanı (Dönüm)")
    total_harvested_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Toplam Hasat Miktarı (kg/ton)")
    average_yield = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Ortalama Verim (kg/dönüm)")
    min_yield = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Minimum Verim (kg/dönüm)")
    max_yield = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Maksimum Verim (kg/dönüm)")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Toplam Maliyet")
    average_cost_per_dunum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Dönüm Başına Ortalama Maliyet")
    average_cost_per_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Kg Başına Ortalama Maliyet")
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Toplam Gelir")
    average_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Ortalama Satış Fiyatı")
    total_profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Toplam Kar")
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Kar Marjı (%)")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    
    def __str__(self):
        return f"{self.product.name} - {self.year}{' - ' + self.season if self.season else ''}"
    
    class Meta:
        verbose_name = "Ürün Performans Metriği"
        verbose_name_plural = "Ürün Performans Metrikleri"
        ordering = ['-year', 'product__name']
        unique_together = ['product', 'year', 'season']

class AnimalPerformanceMetric(models.Model):
    """Model for tracking animal performance metrics"""
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name="performance_metrics", verbose_name="Hayvan Türü")
    year = models.PositiveIntegerField(verbose_name="Yıl")
    period = models.CharField(max_length=20, blank=True, null=True, verbose_name="Dönem")
    average_daily_gain = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Ortalama Günlük Kilo Artışı (kg)")
    feed_conversion_ratio = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Yem Dönüşüm Oranı")
    mortality_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Ölüm Oranı (%)")
    birth_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Doğum Oranı (%)")
    avg_offspring_per_female = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Dişi Başına Ortalama Yavru Sayısı")
    avg_productive_lifespan = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Ortalama Verimli Yaşam Süresi")
    avg_production = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Ortalama Üretim (Süt/Yumurta vb.)")
    production_unit = models.CharField(max_length=20, blank=True, null=True, verbose_name="Üretim Birimi")
    avg_cost_per_animal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Hayvan Başına Ortalama Maliyet")
    avg_revenue_per_animal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Hayvan Başına Ortalama Gelir")
    profit_per_animal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Hayvan Başına Kar")
    total_animals = models.PositiveIntegerField(blank=True, null=True, verbose_name="Toplam Hayvan Sayısı")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    
    def __str__(self):
        return f"{self.animal_type.name} - {self.year}{' - ' + self.period if self.period else ''}"
    
    class Meta:
        verbose_name = "Hayvan Performans Metriği"
        verbose_name_plural = "Hayvan Performans Metrikleri"
        ordering = ['-year', 'animal_type__name']
        unique_together = ['animal_type', 'year', 'period']

class LandProductivityMetric(models.Model):
    """Model for tracking land productivity metrics"""
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="productivity_metrics", verbose_name="Arazi")
    parcel = models.ForeignKey(Parcel, on_delete=models.SET_NULL, null=True, blank=True, related_name="productivity_metrics", verbose_name="Parsel")
    year = models.PositiveIntegerField(verbose_name="Yıl")
    season = models.CharField(max_length=20, blank=True, null=True, verbose_name="Sezon")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="land_metrics", verbose_name="Ürün")
    area_used = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kullanılan Alan (Dönüm)")
    total_harvest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Toplam Hasat (kg/ton)")
    yield_per_dunum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Dönüm Başına Verim")
    revenue_per_dunum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Dönüm Başına Gelir")
    cost_per_dunum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Dönüm Başına Maliyet")
    profit_per_dunum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Dönüm Başına Kar")
    water_usage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Su Kullanımı (m³)")
    fertilizer_usage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Gübre Kullanımı (kg)")
    pesticide_usage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="İlaç Kullanımı")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    
    def __str__(self):
        return f"{self.land.name}{' - ' + self.parcel.parcel_no if self.parcel else ''} - {self.year}{' - ' + self.season if self.season else ''}"
    
    class Meta:
        verbose_name = "Arazi Verimlilik Metriği"
        verbose_name_plural = "Arazi Verimlilik Metrikleri"
        ordering = ['-year', 'land__name']
        
class Benchmark(models.Model):
    """Model for industry benchmarks for comparison"""
    name = models.CharField(max_length=100, verbose_name="Kıyaslama Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    metric_type = models.CharField(max_length=50, verbose_name="Metrik Tipi")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="benchmarks", verbose_name="Ürün")
    animal_type = models.ForeignKey(AnimalType, on_delete=models.SET_NULL, null=True, blank=True, related_name="benchmarks", verbose_name="Hayvan Türü")
    region = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bölge")
    year = models.PositiveIntegerField(verbose_name="Yıl")
    season = models.CharField(max_length=20, blank=True, null=True, verbose_name="Sezon")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Değer")
    unit = models.CharField(max_length=50, verbose_name="Birim")
    source = models.CharField(max_length=200, blank=True, null=True, verbose_name="Kaynak")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    
    def __str__(self):
        return f"{self.name} - {self.year}"
    
    class Meta:
        verbose_name = "Kıyaslama"
        verbose_name_plural = "Kıyaslamalar"
        ordering = ['-year', 'name']
