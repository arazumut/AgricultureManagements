from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Kullanıcı profil modeli"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Kullanıcı")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Şehir")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name="Profil Fotoğrafı")
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="İşletme Adı")
    tax_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Vergi No")
    preferred_language = models.CharField(max_length=10, default='tr', verbose_name="Tercih Edilen Dil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"
