from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from django.db.models import Count, Sum, Avg

class AnimalType(models.Model):
    """Model for animal types"""
    name = models.CharField(max_length=100, verbose_name="Tür Adı")
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Hayvan Türü"
        verbose_name_plural = "Hayvan Türleri"
        ordering = ['name']

class AnimalBreed(models.Model):
    """Model for animal breeds"""
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name="breeds", verbose_name="Tür")
    name = models.CharField(max_length=100, verbose_name="Irk Adı")
    characteristics = models.TextField(verbose_name="Özellikler", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    
    def __str__(self):
        return f"{self.animal_type.name} - {self.name}"
    
    class Meta:
        verbose_name = "Hayvan Irkı"
        verbose_name_plural = "Hayvan Irkları"
        ordering = ['animal_type__name', 'name']

class Animal(models.Model):
    """Model for individual animals on the farm"""
    GENDER_CHOICES = [
        ('M', _('Erkek')),
        ('F', _('Dişi')),
    ]
    
    tag_number = models.CharField(_('Küpe Numarası'), max_length=50, unique=True)
    name = models.CharField(_('İsim'), max_length=100, blank=True, null=True)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name="animals", verbose_name="Tür")
    breed = models.ForeignKey(AnimalBreed, on_delete=models.CASCADE, related_name="animals", verbose_name="Irk")
    gender = models.CharField(_('Cinsiyet'), max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(_('Doğum Tarihi'))
    mother_tag_number = models.CharField(max_length=50, verbose_name="Ana Küpe No", blank=True, null=True)
    father_tag_number = models.CharField(max_length=50, verbose_name="Baba Küpe No", blank=True, null=True)
    arrival_date = models.DateField(verbose_name="Geliş Tarihi", blank=True, null=True)
    source = models.CharField(max_length=200, verbose_name="Kaynak", blank=True, null=True)
    weight = models.DecimalField(_('Ağırlık (kg)'), max_digits=8, decimal_places=2, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Satın Alma Fiyatı", blank=True, null=True)
    image = models.ImageField(_('Fotoğraf'), upload_to='animals/', blank=True, null=True)
    notes = models.TextField(verbose_name="Notlar", blank=True, null=True)
    is_active = models.BooleanField(_('Aktif'), default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animals", verbose_name="Sahibi")
    created_at = models.DateTimeField(_('Oluşturulma Tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Güncelleme Tarihi'), auto_now=True)
    parent_birth = models.ForeignKey('Birth', on_delete=models.SET_NULL, related_name="offspring_animals", verbose_name="Doğum Kaydı", blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('hayvan:animal_detail', args=[str(self.id)])
    
    def get_age(self):
        if not self.birth_date:
            return "Bilinmiyor"
        
        today = timezone.now().date()
        years = today.year - self.birth_date.year
        months = today.month - self.birth_date.month
        
        if months < 0:
            years -= 1
            months += 12
        
        if years > 0:
            if months > 0:
                return f"{years} yıl {months} ay"
            return f"{years} yıl"
        elif months > 0:
            return f"{months} ay"
        else:
            days = (today - self.birth_date).days
            return f"{days} gün"
    
    def get_age_months(self):
        """Hayvanın toplam ay olarak yaşını hesapla"""
        today = date.today()
        born = self.birth_date
        months = (today.year - born.year) * 12 + today.month - born.month
        if today.day < born.day:
            months -= 1
        return months
    
    def get_gender_display_with_icon(self):
        """Cinsiyet görüntüleme"""
        if self.gender == 'M':
            return f'<i class="fas fa-mars text-primary"></i> {self.get_gender_display()}'
        else:
            return f'<i class="fas fa-venus text-danger"></i> {self.get_gender_display()}'
    
    def get_status(self):
        """Hayvan durumunu al"""
        if not self.is_active:
            return "Pasif"
        
        if self.gender == 'F':
            # Dişi hayvanlar için üreme durumu
            reproduction_records = self.reproduction_records.filter(
                pregnancy_status='pregnant'
            ).order_by('-insemination_date')
            
            if reproduction_records.exists():
                return "Gebe"
        
        return "Aktif"
    
    def get_health_statistics(self):
        """Sağlık istatistikleri hesapla"""
        health_records = self.health_records.all()
        
        stats = {
            'total_records': health_records.count(),
            'examination_count': health_records.filter(procedure_type='examination').count(),
            'vaccine_count': health_records.filter(procedure_type='vaccine').count(),
            'treatment_count': health_records.filter(procedure_type='treatment').count(),
            'surgery_count': health_records.filter(procedure_type='surgery').count(),
            'last_record': health_records.order_by('-procedure_date').first(),
            'total_cost': sum(record.cost or 0 for record in health_records),
        }
        
        # Son 12 aydaki sağlık kayıtları
        one_year_ago = timezone.now().date() - timedelta(days=365)
        stats['recent_records'] = health_records.filter(procedure_date__gte=one_year_ago).count()
        
        return stats
    
    def get_reproduction_statistics(self):
        """Üreme istatistikleri hesapla (sadece dişi hayvanlar için)"""
        if self.gender != 'F':
            return None
        
        reproduction_records = self.reproduction_records.all()
        births = self.births.all()
        
        stats = {
            'total_inseminations': reproduction_records.count(),
            'total_births': births.count(),
            'total_offspring': sum(birth.offspring_count or 0 for birth in births),
            'male_offspring': sum(birth.male_count or 0 for birth in births),
            'female_offspring': sum(birth.female_count or 0 for birth in births),
            'stillborns': sum(birth.stillborn_count or 0 for birth in births),
            'is_pregnant': reproduction_records.filter(pregnancy_status='pregnant').exists(),
            'last_birth': births.order_by('-birth_date').first(),
            'next_expected_birth': reproduction_records.filter(
                pregnancy_status='pregnant', 
                expected_birth_date__isnull=False
            ).order_by('expected_birth_date').first(),
        }
        
        # Doğurganlık hesabı (doğum sayısı / tohumlama sayısı)
        if stats['total_inseminations'] > 0:
            stats['fertility_rate'] = round((stats['total_births'] / stats['total_inseminations']) * 100)
        else:
            stats['fertility_rate'] = 0
            
        return stats
    
    def get_all_stats(self):
        """Hayvan için tüm istatistikleri getirir"""
        stats = {
            'yaş': self.get_age(),
            'yaş_ay': self.get_age_months(),
            'durum': self.get_status(),
            'sağlık': self.get_health_statistics(),
        }
        
        if self.gender == 'F':
            stats['üreme'] = self.get_reproduction_statistics()
            
        return stats
    
    def get_feed_consumption(self, days=30):
        """Belirli gün aralığındaki yem tüketimini hesaplar"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Doğrudan hayvana ait besleme kayıtları
        direct_feedings = self.feeding_records.filter(
            feeding_date__gte=start_date,
            feeding_date__lte=end_date
        ).aggregate(total=Sum('amount'))
        
        # Gruplara ait besleme kayıtları (hayvan bu gruba dahilse)
        group_feedings = 0
        for group in self.groups.all():
            group_size = group.animals.count()
            if group_size > 0:  # Sıfıra bölme hatası önlemek için
                group_total = group.feeding_records.filter(
                    feeding_date__gte=start_date,
                    feeding_date__lte=end_date
                ).aggregate(total=Sum('amount'))
                
                if group_total['total']:
                    # Gruptaki toplam miktarı hayvan sayısına bölerek hayvan başına düşen miktarı hesapla
                    group_feedings += group_total['total'] / group_size
        
        total_consumption = (direct_feedings['total'] or 0) + group_feedings
        
        return {
            'total': total_consumption,
            'daily_avg': total_consumption / days if total_consumption > 0 else 0,
            'period_days': days
        }
    
    def get_related_animals(self):
        """Akraba hayvanları getirir (anne, baba, yavrular)"""
        related = {
            'mother': None,
            'father': None,
            'offspring': []
        }
        
        # Anne ve baba bulma
        if self.mother_tag_number:
            try:
                related['mother'] = Animal.objects.get(tag_number=self.mother_tag_number, owner=self.owner)
            except Animal.DoesNotExist:
                pass
        
        if self.father_tag_number:
            try:
                related['father'] = Animal.objects.get(tag_number=self.father_tag_number, owner=self.owner)
            except Animal.DoesNotExist:
                pass
        
        # Doğumlardan yavruları bulma
        if self.gender == 'F':
            birth_offspring = []
            for birth in self.births.all():
                birth_offspring.extend(list(birth.offspring.all()))
            related['offspring'] = birth_offspring
        
        return related
    
    @classmethod
    def get_herd_statistics(cls, owner):
        """Sürü istatistiklerini hesaplar"""
        all_animals = cls.objects.filter(owner=owner, is_active=True)
        
        # Temel sayılar
        total = all_animals.count()
        males = all_animals.filter(gender='M').count()
        females = all_animals.filter(gender='F').count()
        
        # Tür ve ırk dağılımı
        animal_types = all_animals.values('animal_type__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        breeds = all_animals.values('breed__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Yaş grupları dağılımı
        today = timezone.now().date()
        
        # Yaşa göre gruplandırma için yardımcı fonksiyon
        def get_age_group(birth_date):
            if not birth_date:
                return 'Bilinmeyen'
                
            age_days = (today - birth_date).days
            
            if age_days < 30:
                return '1 aydan az'
            elif age_days < 180:  # ~6 ay
                return '1-6 ay'
            elif age_days < 365:  # 1 yıl
                return '6-12 ay'
            elif age_days < 730:  # 2 yıl
                return '1-2 yıl'
            else:
                return '2+ yıl'
        
        age_groups = {}
        for animal in all_animals:
            group = get_age_group(animal.birth_date)
            if group in age_groups:
                age_groups[group] += 1
            else:
                age_groups[group] = 1
                
        # Son 6 aydaki doğumlar
        six_months_ago = today - timedelta(days=180)
        recent_births = Birth.objects.filter(
            animal__owner=owner,
            birth_date__gte=six_months_ago
        ).aggregate(
            count=Count('id'),
            total_offspring=Sum('offspring_count'),
            males=Sum('male_count'),
            females=Sum('female_count'),
            stillborn=Sum('stillborn_count')
        )
        
        # Sağlık istatistikleri
        health_records = HealthRecord.objects.filter(
            animal__owner=owner,
            animal__is_active=True,
            procedure_date__gte=six_months_ago
        )
        
        health_stats = {
            'total': health_records.count(),
            'by_type': dict(health_records.values_list('procedure_type').annotate(count=Count('id'))),
            'total_cost': health_records.aggregate(sum=Sum('cost'))['sum'] or 0
        }
            
        return {
            'total': total,
            'males': males,
            'females': females,
            'pregnant': all_animals.filter(gender='F', reproduction_records__pregnancy_status='pregnant').distinct().count(),
            'animal_types': list(animal_types),
            'breeds': list(breeds),
            'age_groups': age_groups,
            'recent_births': recent_births,
            'health_stats': health_stats
        }
    
    def __str__(self):
        return self.tag_number
    
    class Meta:
        verbose_name = _('Hayvan')
        verbose_name_plural = _('Hayvanlar')
        ordering = ['-created_at']

class AnimalGroup(models.Model):
    """Model for grouping animals"""
    name = models.CharField(max_length=100, verbose_name="Grup Adı")
    animals = models.ManyToManyField(Animal, related_name="groups", verbose_name="Hayvanlar")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animal_groups", verbose_name="Sahibi")
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Grup"
        verbose_name_plural = "Gruplar"
        ordering = ['name']

class HealthRecord(models.Model):
    """Model for animal health records"""
    PROCEDURE_TYPES = [
        ('examination', 'Muayene'),
        ('vaccine', 'Aşı'),
        ('treatment', 'Tedavi'),
        ('surgery', 'Ameliyat'),
        ('other', 'Diğer')
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="health_records", verbose_name="Hayvan")
    procedure_date = models.DateField(verbose_name="İşlem Tarihi")
    procedure_type = models.CharField(max_length=20, choices=PROCEDURE_TYPES, verbose_name="İşlem Tipi")
    diagnosis = models.CharField(max_length=200, verbose_name="Tanı/İşlem", blank=True, null=True)
    treatment = models.TextField(verbose_name="Tedavi/Uygulama", blank=True, null=True)
    medication = models.CharField(max_length=200, verbose_name="İlaç", blank=True, null=True)
    dosage = models.CharField(max_length=100, verbose_name="Doz", blank=True, null=True)
    veterinarian = models.CharField(max_length=200, verbose_name="Veteriner", blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maliyet", blank=True, null=True)
    notes = models.TextField(verbose_name="Notlar", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.animal.tag_number} - {self.procedure_type} ({self.procedure_date})"
    
    class Meta:
        verbose_name = "Sağlık Kaydı"
        verbose_name_plural = "Sağlık Kayıtları"
        ordering = ['-procedure_date']

class FeedRation(models.Model):
    """Model for feed rations for animals"""
    name = models.CharField(max_length=100, verbose_name="Rasyon Adı")
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name="feed_rations", verbose_name="Hayvan Türü")
    age_group = models.CharField(max_length=100, verbose_name="Yaş Grubu", blank=True, null=True)
    production_purpose = models.CharField(max_length=100, verbose_name="Üretim Amacı", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    
    def __str__(self):
        return f"{self.name} ({self.animal_type.name})"
    
    class Meta:
        verbose_name = "Yem Rasyonu"
        verbose_name_plural = "Yem Rasyonları"
        ordering = ['animal_type__name', 'name']

class FeedRationDetail(models.Model):
    """Model for feed ration details"""
    feed_ration = models.ForeignKey(FeedRation, on_delete=models.CASCADE, related_name="details", verbose_name="Rasyon")
    feed_name = models.CharField(max_length=100, verbose_name="Yem Adı")
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Miktar (kg)")
    unit_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Birim Fiyat", blank=True, null=True)
    
    def __str__(self):
        return f"{self.feed_ration.name} - {self.feed_name}"
    
    class Meta:
        verbose_name = "Yem Rasyonu Detay"
        verbose_name_plural = "Yem Rasyonu Detayları"
        ordering = ['feed_ration__name', 'feed_name']

class Feeding(models.Model):
    """Model for feeding records"""
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="feeding_records", verbose_name="Hayvan", blank=True, null=True)
    animal_group = models.ForeignKey(AnimalGroup, on_delete=models.CASCADE, related_name="feeding_records", verbose_name="Grup", blank=True, null=True)
    feed_ration = models.ForeignKey(FeedRation, on_delete=models.CASCADE, related_name="feeding_records", verbose_name="Rasyon", blank=True, null=True)
    feeding_date = models.DateField(verbose_name="Besleme Tarihi")
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Miktar (kg)")
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        if self.animal:
            return f"{self.animal.tag_number} - {self.feeding_date}"
        else:
            return f"{self.animal_group.name} - {self.feeding_date}"
    
    class Meta:
        verbose_name = "Besleme Kaydı"
        verbose_name_plural = "Besleme Kayıtları"
        ordering = ['-feeding_date']

class ReproductionRecord(models.Model):
    """Model for female animal reproduction records"""
    INSEMINATION_TYPE_CHOICES = [
        ('natural', 'Doğal Aşım'),
        ('artificial', 'Suni Tohumlama'),
    ]
    
    PREGNANCY_STATUS_CHOICES = [
        ('', 'Bilinmiyor'),
        ('pregnant', 'Gebe'),
        ('not_pregnant', 'Gebe Değil'),
        ('miscarriage', 'Düşük'),
        ('birth_completed', 'Doğum Yaptı'),
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="reproduction_records", verbose_name="Hayvan")
    insemination_date = models.DateField(verbose_name="Tohumlama Tarihi", blank=True, null=True)
    insemination_type = models.CharField(max_length=20, choices=INSEMINATION_TYPE_CHOICES, default='natural', verbose_name="Tohumlama Tipi")
    father_tag_number = models.CharField(max_length=50, verbose_name="Baba Küpe No", blank=True, null=True)
    semen_source = models.CharField(max_length=200, verbose_name="Sperma Kaynağı", blank=True, null=True)
    technician = models.CharField(max_length=100, verbose_name="Teknisyen/Veteriner", blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maliyet", blank=True, null=True)
    pregnancy_status = models.CharField(max_length=20, choices=PREGNANCY_STATUS_CHOICES, blank=True, default='', verbose_name="Gebelik Durumu")
    pregnancy_check_date = models.DateField(verbose_name="Gebelik Kontrol Tarihi", blank=True, null=True)
    expected_birth_date = models.DateField(verbose_name="Tahmini Doğum Tarihi", blank=True, null=True)
    notes = models.TextField(verbose_name="Notlar", blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    
    def __str__(self):
        insemination_str = str(self.insemination_date) if self.insemination_date else "Tarih Yok"
        return f"{self.animal.tag_number} - {insemination_str}"
    
    class Meta:
        verbose_name = "Üreme Kaydı"
        verbose_name_plural = "Üreme Kayıtları"
        ordering = ['-insemination_date']

class Birth(models.Model):
    """Model for birth records"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Kolay'),
        ('normal', 'Normal'),
        ('difficult', 'Zor'),
        ('assisted', 'Yardımlı'),
        ('cesarean', 'Sezaryen'),
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="births", verbose_name="Anne")
    birth_date = models.DateField(verbose_name="Doğum Tarihi")
    reproduction_record = models.OneToOneField(ReproductionRecord, on_delete=models.SET_NULL, related_name="birth", verbose_name="Üreme Kaydı", blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='normal', verbose_name="Doğum Zorluğu")
    offspring_count = models.PositiveIntegerField(verbose_name="Yavru Sayısı")
    male_count = models.PositiveIntegerField(verbose_name="Erkek Sayısı", default=0)
    female_count = models.PositiveIntegerField(verbose_name="Dişi Sayısı", default=0)
    stillborn_count = models.PositiveIntegerField(verbose_name="Ölü Doğum", default=0)
    veterinarian = models.CharField(max_length=100, verbose_name="Veteriner", blank=True, null=True)
    notes = models.TextField(verbose_name="Notlar", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    
    def __str__(self):
        return f"{self.animal.tag_number} - {self.birth_date}"
    
    class Meta:
        verbose_name = "Doğum"
        verbose_name_plural = "Doğumlar"
        ordering = ['-birth_date']

class Offspring(models.Model):
    """Model for offspring information"""
    GENDER_CHOICES = [
        ('M', 'Erkek'),
        ('F', 'Dişi'),
    ]
    
    birth = models.ForeignKey(Birth, on_delete=models.CASCADE, related_name="offspring", verbose_name="Doğum")
    tag_number = models.CharField(max_length=50, verbose_name="Küpe No", blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Cinsiyet")
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Doğum Ağırlığı (kg)", blank=True, null=True)
    animal = models.OneToOneField(Animal, on_delete=models.SET_NULL, related_name="birth_record", verbose_name="Hayvan Kaydı", blank=True, null=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    
    def __str__(self):
        mother_tag = self.birth.animal.tag_number if self.birth and self.birth.animal else "Bilinmiyor"
        return f"{mother_tag} Yavrusu - {self.tag_number or 'Küpe Yok'}"
    
    class Meta:
        verbose_name = "Yavru"
        verbose_name_plural = "Yavrular"
