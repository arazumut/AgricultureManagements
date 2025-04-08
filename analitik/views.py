from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from hayvan.models import Animal, HealthRecord, Birth
from arazi.models import Land, Parcel
from uretim.models import Product, Harvest
from finans.models import Transaction, Invoice
from datetime import datetime, timedelta

# Create your views here.

@login_required
def dashboard(request):
    """
    Ana analitik paneli (dashboard)
    """
    # Temel sayıları al
    animal_count = Animal.objects.filter(is_active=True).count()
    land_count = Land.objects.count()
    parcel_count = Parcel.objects.count()
    product_count = Product.objects.count()
    
    # Son 30 günlük finansal verileri al
    thirty_days_ago = datetime.now() - timedelta(days=30)
    income = Transaction.objects.filter(
        transaction_type='income', 
        date__gte=thirty_days_ago
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expense = Transaction.objects.filter(
        transaction_type='expense', 
        date__gte=thirty_days_ago
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Son hasatları al
    recent_harvests = Harvest.objects.all().order_by('-harvest_date')[:5]
    
    # Sağlık kayıtları istatistikleri
    health_stats = HealthRecord.objects.values('procedure_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Doğum istatistikleri
    birth_count = Birth.objects.count()
    avg_litter_size = Birth.objects.aggregate(avg=Avg('litter_size'))['avg'] or 0
    
    context = {
        'animal_count': animal_count,
        'land_count': land_count,
        'parcel_count': parcel_count,
        'product_count': product_count,
        'income': income,
        'expense': expense,
        'net': income - expense,
        'recent_harvests': recent_harvests,
        'health_stats': health_stats,
        'birth_count': birth_count,
        'avg_litter_size': avg_litter_size,
    }
    
    return render(request, 'analitik/dashboard.html', context)
