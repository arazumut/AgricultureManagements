# Author: Umut Araz
# Date: 2025-04-08

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Land, Parcel, SoilAnalysis, IrrigationRecord
from .forms import LandForm, ParcelForm, SoilAnalysisForm, IrrigationRecordForm

@login_required
def land_list(request):
    """List all lands with search and filtering options"""
    # Base queryset
    lands = Land.objects.filter(owner=request.user, is_active=True)
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    selected_sort = request.GET.get('sort', '-created_at')
    
    # Apply search filter
    if search_query:
        lands = lands.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Apply sorting
    lands = lands.order_by(selected_sort)
    
    # Pagination
    paginator = Paginator(lands, 10)  # 10 lands per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_sort': selected_sort,
    }
    
    return render(request, 'arazi/land_list.html', context)

@login_required
def land_detail(request, pk):
    """
    View to display detailed information about a specific land
    """
    land = get_object_or_404(Land, pk=pk, owner=request.user)
    
    # Get related parcels
    parcels = land.parcels.all().order_by('parcel_no')
    
    context = {
        'land': land,
        'parcels': parcels,
    }
    
    return render(request, 'arazi/land_detail.html', context)

@login_required
def land_create(request):
    """
    View to handle creation of a new land
    """
    if request.method == 'POST':
        form = LandForm(request.POST)
        if form.is_valid():
            land = form.save(commit=False)
            land.owner = request.user
            land.save()
            
            messages.success(request, 'Arazi başarıyla kaydedildi.')
            return redirect('arazi:land_detail', pk=land.pk)
    else:
        form = LandForm()
    
    return render(request, 'arazi/land_form.html', {'form': form})

@login_required
def land_update(request, pk):
    """
    View to handle updating an existing land
    """
    land = get_object_or_404(Land, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = LandForm(request.POST, instance=land)
        if form.is_valid():
            form.save()
            messages.success(request, 'Arazi bilgileri başarıyla güncellendi.')
            return redirect('arazi:land_detail', pk=land.pk)
    else:
        form = LandForm(instance=land)
    
    return render(request, 'arazi/land_form.html', {'form': form, 'land': land})

@login_required
def land_delete(request, pk):
    """
    View to handle land deletion (soft delete by marking as inactive)
    """
    land = get_object_or_404(Land, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        # Confirm checkbox is required
        if request.POST.get('confirm_delete'):
            land.is_active = False
            land.save()
            messages.success(request, 'Arazi başarıyla silindi.')
            return redirect('arazi:land_list')
        else:
            messages.error(request, 'Silme işlemini onaylamanız gerekmektedir.')
    
    return render(request, 'arazi/land_delete.html', {'land': land})

@login_required
def parcel_create(request, land_id):
    """
    View to handle creation of a new parcel for a land
    """
    land = get_object_or_404(Land, pk=land_id, owner=request.user)
    
    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.land = land
            parcel.save()
            
            messages.success(request, 'Parsel başarıyla oluşturuldu.')
            return redirect('arazi:land_detail', pk=land.pk)
    else:
        form = ParcelForm()
    
    context = {
        'form': form,
        'land': land
    }
    
    return render(request, 'arazi/parcel_form.html', context)

@login_required
def parcel_detail(request, land_id, parcel_id):
    """
    View to display detailed information about a specific parcel
    """
    land = get_object_or_404(Land, pk=land_id, owner=request.user)
    parcel = get_object_or_404(Parcel, pk=parcel_id, land=land)
    
    # Get related soil analyses
    soil_analyses = parcel.soil_analyses.all().order_by('-analysis_date')
    
    # Get related irrigation records
    irrigation_records = parcel.irrigation_records.all().order_by('-irrigation_date')
    
    # Get related plantings
    plantings = parcel.plantings.all().order_by('-planting_date')
    
    context = {
        'land': land,
        'parcel': parcel,
        'soil_analyses': soil_analyses,
        'irrigation_records': irrigation_records,
        'plantings': plantings,
    }
    
    return render(request, 'arazi/parcel_detail.html', context)

@login_required
def soil_analysis_create(request, land_id, parcel_id):
    """
    View to handle creation of a new soil analysis for a parcel
    """
    land = get_object_or_404(Land, pk=land_id, owner=request.user)
    parcel = get_object_or_404(Parcel, pk=parcel_id, land=land)
    
    if request.method == 'POST':
        form = SoilAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            soil_analysis = form.save(commit=False)
            soil_analysis.parcel = parcel
            soil_analysis.save()
            
            messages.success(request, 'Toprak analizi başarıyla kaydedildi.')
            return redirect('arazi:parcel_detail', land_id=land.pk, parcel_id=parcel.pk)
    else:
        form = SoilAnalysisForm()
    
    context = {
        'form': form,
        'land': land,
        'parcel': parcel
    }
    
    return render(request, 'arazi/soil_analysis_form.html', context)

@login_required
def irrigation_record_create(request, land_id, parcel_id):
    """
    View to handle creation of a new irrigation record for a parcel
    """
    land = get_object_or_404(Land, pk=land_id, owner=request.user)
    parcel = get_object_or_404(Parcel, pk=parcel_id, land=land)
    
    if request.method == 'POST':
        form = IrrigationRecordForm(request.POST)
        if form.is_valid():
            irrigation_record = form.save(commit=False)
            irrigation_record.parcel = parcel
            irrigation_record.save()
            
            messages.success(request, 'Sulama kaydı başarıyla oluşturuldu.')
            return redirect('arazi:parcel_detail', land_id=land.pk, parcel_id=parcel.pk)
    else:
        form = IrrigationRecordForm()
    
    context = {
        'form': form,
        'land': land,
        'parcel': parcel
    }
    
    return render(request, 'arazi/irrigation_record_form.html', context)

@login_required
def soil_analysis_list(request):
    """Toprak analizlerini listeler"""
    soil_analyses = SoilAnalysis.objects.all().order_by('-analysis_date')
    return render(request, 'arazi/soil_analysis_list.html', {
        'soil_analyses': soil_analyses
    })
