from django.db import models
from django.contrib.auth.models import User
from arazi.models import Land, Parcel
from hayvan.models import Animal, AnimalGroup
from uretim.models import Planting

class TaskCategory(models.Model):
    """Model for task categories"""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    color_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Renk Kodu")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="İkon")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_categories", verbose_name="Sahibi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Görev Kategorisi"
        verbose_name_plural = "Görev Kategorileri"
        ordering = ['name']

class Worker(models.Model):
    """Model for farm workers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="worker_profile", verbose_name="Kullanıcı", blank=True, null=True)
    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True, verbose_name="E-posta")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pozisyon")
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Doğum Tarihi")
    hire_date = models.DateField(blank=True, null=True, verbose_name="İşe Başlama Tarihi")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Saatlik Ücret")
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Günlük Ücret")
    specializations = models.TextField(blank=True, null=True, verbose_name="Uzmanlıklar")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workers", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Çalışan"
        verbose_name_plural = "Çalışanlar"
        ordering = ['last_name', 'first_name']

class Equipment(models.Model):
    """Model for farm equipment"""
    name = models.CharField(max_length=100, verbose_name="Ekipman Adı")
    equipment_type = models.CharField(max_length=100, verbose_name="Ekipman Tipi")
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name="Model")
    manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name="Üretici")
    serial_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Seri No")
    purchase_date = models.DateField(blank=True, null=True, verbose_name="Satın Alma Tarihi")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Satın Alma Fiyatı")
    status = models.CharField(max_length=50, default="available", verbose_name="Durum")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="equipment", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Ekipman"
        verbose_name_plural = "Ekipmanlar"
        ordering = ['name']

class Task(models.Model):
    """Model for farm tasks"""
    STATUS_CHOICES = [
        ('not_started', 'Başlamadı'),
        ('in_progress', 'Devam Ediyor'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
        ('delayed', 'Ertelendi'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Düşük'),
        ('medium', 'Orta'),
        ('high', 'Yüksek'),
        ('urgent', 'Acil'),
    ]
    
    RECURRENCE_CHOICES = [
        ('none', 'Tekrar Yok'),
        ('daily', 'Günlük'),
        ('weekly', 'Haftalık'),
        ('monthly', 'Aylık'),
        ('yearly', 'Yıllık'),
        ('custom', 'Özel'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name="tasks", verbose_name="Kategori")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name="Durum")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Öncelik")
    
    # Task dates
    planned_start_date = models.DateField(verbose_name="Planlanan Başlangıç Tarihi")
    planned_end_date = models.DateField(verbose_name="Planlanan Bitiş Tarihi")
    actual_start_date = models.DateField(blank=True, null=True, verbose_name="Gerçek Başlangıç Tarihi")
    actual_end_date = models.DateField(blank=True, null=True, verbose_name="Gerçek Bitiş Tarihi")
    
    # Task time planning
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, 
                                         verbose_name="Tahmini Süre (saat)")
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, 
                                      verbose_name="Gerçek Süre (saat)")
    
    # Recurrence
    is_recurring = models.BooleanField(default=False, verbose_name="Tekrarlanan Görev mi?")
    recurrence_pattern = models.CharField(max_length=20, choices=RECURRENCE_CHOICES, default='none', 
                                         verbose_name="Tekrarlama Düzeni")
    recurrence_details = models.JSONField(blank=True, null=True, verbose_name="Tekrarlama Detayları")
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name="child_tasks", verbose_name="Üst Görev")
    
    # Assignments
    assigned_workers = models.ManyToManyField(Worker, blank=True, related_name="assigned_tasks", 
                                             verbose_name="Atanan Çalışanlar")
    equipment_needed = models.ManyToManyField(Equipment, blank=True, related_name="tasks", 
                                             verbose_name="Gereken Ekipmanlar")
    
    # Related entities
    related_land = models.ForeignKey(Land, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name="tasks", verbose_name="İlgili Arazi")
    related_parcel = models.ForeignKey(Parcel, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name="tasks", verbose_name="İlgili Parsel")
    related_planting = models.ForeignKey(Planting, on_delete=models.SET_NULL, null=True, blank=True, 
                                        related_name="tasks", verbose_name="İlgili Ekim")
    related_animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name="tasks", verbose_name="İlgili Hayvan")
    related_animal_group = models.ForeignKey(AnimalGroup, on_delete=models.SET_NULL, null=True, blank=True, 
                                           related_name="tasks", verbose_name="İlgili Hayvan Grubu")
    
    # Costs
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                        verbose_name="Tahmini Maliyet")
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                     verbose_name="Gerçek Maliyet")
    
    # Completion
    completion_percentage = models.PositiveIntegerField(default=0, verbose_name="Tamamlanma Yüzdesi")
    completion_notes = models.TextField(blank=True, null=True, verbose_name="Tamamlanma Notları")
    
    # System fields
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks", 
                                  verbose_name="Oluşturan")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks", verbose_name="Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Görev"
        verbose_name_plural = "Görevler"
        ordering = ['planned_start_date', 'priority']

class TaskComment(models.Model):
    """Model for comments on tasks"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", verbose_name="Görev")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_comments", verbose_name="Kullanıcı")
    comment = models.TextField(verbose_name="Yorum")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.task.title} - {self.user.username} - {self.created_at}"
    
    class Meta:
        verbose_name = "Görev Yorumu"
        verbose_name_plural = "Görev Yorumları"
        ordering = ['-created_at']

class WorkLog(models.Model):
    """Model for tracking work hours on tasks"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="work_logs", verbose_name="Görev")
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="work_logs", verbose_name="Çalışan")
    date = models.DateField(verbose_name="Tarih")
    start_time = models.TimeField(verbose_name="Başlangıç Saati")
    end_time = models.TimeField(verbose_name="Bitiş Saati")
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Çalışılan Saat")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.worker} - {self.task.title} - {self.date}"
    
    class Meta:
        verbose_name = "Çalışma Kaydı"
        verbose_name_plural = "Çalışma Kayıtları"
        ordering = ['-date', '-start_time']

class MaintenanceSchedule(models.Model):
    """Model for equipment maintenance scheduling"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="maintenance_schedules", 
                                 verbose_name="Ekipman")
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    interval_value = models.PositiveIntegerField(verbose_name="Aralık Değeri")
    interval_unit = models.CharField(max_length=20, verbose_name="Aralık Birimi")
    last_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Son Bakım Tarihi")
    next_maintenance_date = models.DateField(verbose_name="Sonraki Bakım Tarihi")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_maintenance_schedules", 
                                  verbose_name="Oluşturan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.equipment.name} - {self.title}"
    
    class Meta:
        verbose_name = "Bakım Programı"
        verbose_name_plural = "Bakım Programları"
        ordering = ['next_maintenance_date']
