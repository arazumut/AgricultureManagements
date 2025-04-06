from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.db import transaction
from hayvan.models import Animal, HealthRecord, ReproductionRecord, Birth
from arazi.models import Land, Parcel
from uretim.models import Planting, PlantingPlan, Harvest
from django.utils import timezone
from datetime import timedelta

def home_view(request):
    """Ana sayfa görünümü"""
    context = {}
    
    if request.user.is_authenticated:
        # Toplam hayvan sayısını al
        animal_count = Animal.objects.filter(owner=request.user, is_active=True).count()
        
        # Toplam arazi sayısını al
        land_count = Land.objects.filter(owner=request.user, is_active=True).count()
        
        # Son eklenen 4 hayvanı al
        latest_animals = Animal.objects.filter(owner=request.user, is_active=True).order_by('-created_at')[:4]
        
        # Yaklaşan sağlık kayıtlarını getir (bugün ve sonraki 7 gün)
        today = timezone.now().date()
        next_week = today + timedelta(days=7)
        upcoming_health_procedures = HealthRecord.objects.filter(
            animal__owner=request.user,
            animal__is_active=True,
            procedure_date__gte=today,
            procedure_date__lte=next_week
        ).order_by('procedure_date')[:5]
        
        # Yakında doğum yapacak hayvanları getir
        pregnant_animals = Animal.objects.filter(
            owner=request.user,
            is_active=True,
            gender='F',
            reproduction_records__pregnancy_status='pregnant'
        ).distinct()[:5]
        
        # Doğum tarihi yaklaşan hayvanlar
        upcoming_births = ReproductionRecord.objects.filter(
            animal__owner=request.user,
            animal__is_active=True,
            pregnancy_status='pregnant',
            expected_birth_date__isnull=False,
            expected_birth_date__gte=today,
            expected_birth_date__lte=next_week
        ).order_by('expected_birth_date')[:5]
        
        # Son doğum kayıtları
        recent_births = Birth.objects.filter(
            animal__owner=request.user,
            animal__is_active=True
        ).order_by('-birth_date')[:5]
        
        # Aktif ekimleri getir
        parcels = Parcel.objects.filter(land__owner=request.user, land__is_active=True, is_active=True)
        active_plantings = Planting.objects.filter(
            parcel__in=parcels
        ).order_by('-planting_date')[:5]
        
        # Yaklaşan ekim planlarını getir (bugün ve sonraki 30 gün)
        next_month = today + timedelta(days=30)
        upcoming_plans = PlantingPlan.objects.filter(
            parcel__in=parcels,
            planned_planting_date__gte=today,
            planned_planting_date__lte=next_month,
            is_completed=False
        ).order_by('planned_planting_date')[:5]
        
        context = {
            'animal_count': animal_count,
            'land_count': land_count,
            'latest_animals': latest_animals,
            'upcoming_health_procedures': upcoming_health_procedures,
            'pregnant_animals': pregnant_animals,
            'upcoming_births': upcoming_births,
            'recent_births': recent_births,
            'active_plantings': active_plantings,
            'upcoming_plans': upcoming_plans,
        }
    
    return render(request, 'index.html', context)

def login_view(request):
    """Kullanıcı giriş görünümü"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hoş geldiniz, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'kullanici/login.html', {'form': form})

def logout_view(request):
    """Kullanıcı çıkış görünümü"""
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect('home')

def register_view(request):
    """Kullanıcı kayıt görünümü"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Temel doğrulama
        if password1 != password2:
            messages.error(request, "Şifreler eşleşmiyor!")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten kullanılıyor!")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu e-posta adresi zaten kullanılıyor!")
            return redirect('register')
        
        # Kullanıcı oluşturma
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password1)
                user_profile = UserProfile.objects.create(user=user)
                login(request, user)
                messages.success(request, f"Hoş geldiniz, {username}! Hesabınız başarıyla oluşturuldu.")
                return redirect('home')
        except Exception as e:
            messages.error(request, f"Kayıt sırasında bir hata oluştu: {str(e)}")
    
    return render(request, 'kullanici/register.html')

@login_required
def profile_view(request):
    """Kullanıcı profil görünümü"""
    profile = request.user.profile
    
    if request.method == 'POST':
        # Profil güncelleme işlemi
        try:
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()
            
            profile.phone = request.POST.get('phone', profile.phone)
            profile.address = request.POST.get('address', profile.address)
            profile.city = request.POST.get('city', profile.city)
            profile.company_name = request.POST.get('company_name', profile.company_name)
            profile.tax_number = request.POST.get('tax_number', profile.tax_number)
            
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            
            profile.save()
            
            messages.success(request, "Profiliniz başarıyla güncellendi.")
        except Exception as e:
            messages.error(request, f"Profil güncellenirken bir hata oluştu: {str(e)}")
    
    return render(request, 'kullanici/profile.html', {'profile': profile})
