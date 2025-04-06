from django.db import models
from django.contrib.auth.models import User
from arazi.models import Land, Parcel

class WeatherStation(models.Model):
    """Model for weather stations"""
    name = models.CharField(max_length=100, verbose_name="İstasyon Adı")
    station_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="İstasyon ID")
    location = models.CharField(max_length=200, verbose_name="Konum")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Enlem")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Boylam")
    elevation = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Rakım (m)", blank=True, null=True)
    api_key = models.CharField(max_length=100, blank=True, null=True, verbose_name="API Anahtarı")
    api_url = models.URLField(blank=True, null=True, verbose_name="API URL")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weather_stations", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Hava Durumu İstasyonu"
        verbose_name_plural = "Hava Durumu İstasyonları"
        ordering = ['name']

class WeatherData(models.Model):
    """Model for weather data records"""
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE, related_name="weather_data", verbose_name="İstasyon")
    timestamp = models.DateTimeField(verbose_name="Zaman")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Sıcaklık (°C)", blank=True, null=True)
    feels_like = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Hissedilen Sıcaklık (°C)", blank=True, null=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Nem (%)", blank=True, null=True)
    pressure = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Basınç (hPa)", blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Rüzgar Hızı (m/s)", blank=True, null=True)
    wind_direction = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Rüzgar Yönü (derece)", blank=True, null=True)
    precipitation = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Yağış (mm)", blank=True, null=True)
    precipitation_probability = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Yağış Olasılığı (%)", blank=True, null=True)
    cloud_cover = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Bulut Örtüsü (%)", blank=True, null=True)
    uv_index = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="UV İndeksi", blank=True, null=True)
    weather_condition = models.CharField(max_length=100, verbose_name="Hava Durumu", blank=True, null=True)
    weather_icon = models.CharField(max_length=50, verbose_name="Hava Durumu İkonu", blank=True, null=True)
    is_forecast = models.BooleanField(default=False, verbose_name="Tahmin mi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.station.name} - {self.timestamp} - {self.temperature}°C"
    
    class Meta:
        verbose_name = "Hava Durumu Verisi"
        verbose_name_plural = "Hava Durumu Verileri"
        ordering = ['-timestamp']
        unique_together = ['station', 'timestamp', 'is_forecast']

class WeatherAlert(models.Model):
    """Model for weather alerts/warnings"""
    ALERT_TYPES = [
        ('frost', 'Don'),
        ('extreme_heat', 'Aşırı Sıcaklık'),
        ('heavy_rain', 'Şiddetli Yağış'),
        ('flood', 'Sel'),
        ('drought', 'Kuraklık'),
        ('storm', 'Fırtına'),
        ('hail', 'Dolu'),
        ('snow', 'Kar'),
        ('other', 'Diğer'),
    ]
    
    SEVERITY_LEVELS = [
        ('info', 'Bilgi'),
        ('advisory', 'Tavsiye'),
        ('watch', 'İzleme'),
        ('warning', 'Uyarı'),
        ('emergency', 'Acil Durum'),
    ]
    
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE, related_name="weather_alerts", verbose_name="İstasyon")
    lands = models.ManyToManyField(Land, related_name="weather_alerts", verbose_name="Araziler", blank=True)
    parcels = models.ManyToManyField(Parcel, related_name="weather_alerts", verbose_name="Parseller", blank=True)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES, verbose_name="Uyarı Tipi")
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, verbose_name="Şiddet Seviyesi")
    title = models.CharField(max_length=100, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama")
    start_time = models.DateTimeField(verbose_name="Başlangıç Zamanı")
    end_time = models.DateTimeField(verbose_name="Bitiş Zamanı")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    is_read = models.BooleanField(default=False, verbose_name="Okundu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.start_time.date()}"
    
    class Meta:
        verbose_name = "Hava Durumu Uyarısı"
        verbose_name_plural = "Hava Durumu Uyarıları"
        ordering = ['-start_time']

class SoilMoistureData(models.Model):
    """Model for soil moisture data (from sensors or manual entry)"""
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name="soil_moisture_data", verbose_name="Parsel")
    timestamp = models.DateTimeField(verbose_name="Zaman")
    depth = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Derinlik (cm)")
    moisture_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Nem Oranı (%)")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Toprak Sıcaklığı (°C)", blank=True, null=True)
    sensor_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Sensör ID")
    battery_level = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Pil Seviyesi (%)", blank=True, null=True)
    is_manual_entry = models.BooleanField(default=False, verbose_name="Manuel Giriş mi?")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.parcel} - {self.timestamp.date()} - {self.moisture_percent}%"
    
    class Meta:
        verbose_name = "Toprak Nemi Verisi"
        verbose_name_plural = "Toprak Nemi Verileri"
        ordering = ['-timestamp']

class ClimateAnalysis(models.Model):
    """Model for long-term climate data analysis"""
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="climate_analyses", verbose_name="Arazi")
    title = models.CharField(max_length=100, verbose_name="Başlık")
    analysis_date = models.DateField(verbose_name="Analiz Tarihi")
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(verbose_name="Bitiş Tarihi")
    avg_temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Ortalama Sıcaklık (°C)", blank=True, null=True)
    min_temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Minimum Sıcaklık (°C)", blank=True, null=True)
    max_temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Maksimum Sıcaklık (°C)", blank=True, null=True)
    total_precipitation = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Toplam Yağış (mm)", blank=True, null=True)
    growing_degree_days = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Büyüme Derece Günleri", blank=True, null=True)
    frost_days = models.PositiveIntegerField(verbose_name="Don Günleri", blank=True, null=True)
    analysis_results = models.TextField(verbose_name="Analiz Sonuçları", blank=True, null=True)
    recommendations = models.TextField(verbose_name="Öneriler", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="climate_analyses", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.land.name} - {self.title} ({self.start_date} - {self.end_date})"
    
    class Meta:
        verbose_name = "İklim Analizi"
        verbose_name_plural = "İklim Analizleri"
        ordering = ['-analysis_date']
