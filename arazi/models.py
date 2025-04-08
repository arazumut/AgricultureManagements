# Author: Umut Araz
# Date: 2025-04-08

from django.db import models
from django.contrib.auth.models import User

class Land(models.Model):
    """Model for land/field owned by farmers"""
    name = models.CharField(max_length=100, verbose_name="Arazi Adı")
    total_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toplam Alan (Dönüm)")
    location = models.CharField(max_length=255, verbose_name="Lokasyon")
    address = models.TextField(verbose_name="Adres", blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Enlem", blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Boylam", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lands", verbose_name="Sahibi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Arazi"
        verbose_name_plural = "Araziler"
        ordering = ['-created_at']
        
class Parcel(models.Model):
    """Model for parcels/subdivisions within a land"""
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="parcels", verbose_name="Arazi")
    parcel_no = models.CharField(max_length=50, verbose_name="Parsel No")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Alan (Dönüm)")
    soil_type = models.CharField(max_length=100, verbose_name="Toprak Türü", blank=True, null=True)
    has_irrigation = models.BooleanField(default=False, verbose_name="Sulama Durumu")
    coordinates = models.TextField(verbose_name="Koordinatlar (GeoJSON)", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.land.name} - Parsel {self.parcel_no}"
    
    class Meta:
        verbose_name = "Parsel"
        verbose_name_plural = "Parseller"
        ordering = ['land', 'parcel_no']
        
class SoilAnalysis(models.Model):
    """Model for soil analysis results for parcels"""
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name="soil_analyses", verbose_name="Parsel")
    analysis_date = models.DateField(verbose_name="Analiz Tarihi")
    ph_value = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="pH Değeri", blank=True, null=True)
    organic_matter = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Organik Madde (%)", blank=True, null=True)
    phosphorus = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Fosfor (P) (ppm)", blank=True, null=True)
    potassium = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Potasyum (K) (ppm)", blank=True, null=True)
    calcium = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Kalsiyum (Ca) (ppm)", blank=True, null=True)
    magnesium = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Magnezyum (Mg) (ppm)", blank=True, null=True)
    iron = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Demir (Fe) (ppm)", blank=True, null=True)
    zinc = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Çinko (Zn) (ppm)", blank=True, null=True)
    report_file = models.FileField(upload_to='soil_analyses/', verbose_name="Rapor Dosyası", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.parcel} - {self.analysis_date}"
    
    class Meta:
        verbose_name = "Toprak Analizi"
        verbose_name_plural = "Toprak Analizleri"
        ordering = ['-analysis_date']
        
class IrrigationRecord(models.Model):
    """Model for irrigation records for parcels"""
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name="irrigation_records", verbose_name="Parsel")
    irrigation_date = models.DateField(verbose_name="Sulama Tarihi")
    irrigation_duration = models.DurationField(verbose_name="Sulama Süresi", blank=True, null=True)
    water_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Su Miktarı (m³)", blank=True, null=True)
    irrigation_method = models.CharField(max_length=100, verbose_name="Sulama Yöntemi", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.parcel} - {self.irrigation_date}"
    
    class Meta:
        verbose_name = "Sulama Kaydı"
        verbose_name_plural = "Sulama Kayıtları"
        ordering = ['-irrigation_date']
