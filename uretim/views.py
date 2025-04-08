from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Avg
from .models import Product, Seed, PlantingPlan, Planting, Harvest, MaintenanceRecord
from arazi.models import Land, Parcel
from .forms import ProductForm, SeedForm, PlantingPlanForm, PlantingForm, HarvestForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pandas as pd
import io
from datetime import datetime

@login_required
def product_list(request):
    """List all products with search and filtering options"""
    # Base queryset
    products = Product.objects.filter(is_active=True)
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    
    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(type__icontains=search_query) |
            Q(variety__icontains=search_query)
        )
    
    # Apply sorting
    products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'uretim/product_list.html', context)

@login_required
def product_detail(request, pk):
    """View to display detailed information about a specific product"""
    product = get_object_or_404(Product, pk=pk)
    
    # Get related seeds
    seeds = product.seeds.all()
    
    # Get related plantings
    plantings = product.plantings.all().order_by('-planting_date')
    
    # Calculate total planted area and total harvest
    total_planted_area = plantings.aggregate(Sum('planting_area'))['planting_area__sum'] or 0
    total_harvest = 0
    total_yield = 0
    harvest_count = 0
    
    for planting in plantings:
        try:
            harvest = planting.harvest
            if harvest.harvest_amount:
                total_harvest += harvest.harvest_amount
                if harvest.yield_rate:
                    total_yield += harvest.yield_rate
                    harvest_count += 1
        except Harvest.DoesNotExist:
            pass
    
    avg_yield = total_yield / harvest_count if harvest_count > 0 else 0
    
    context = {
        'product': product,
        'seeds': seeds,
        'plantings': plantings,
        'total_planted_area': total_planted_area,
        'total_harvest': total_harvest,
        'avg_yield': avg_yield,
    }
    
    return render(request, 'uretim/product_detail.html', context)

@login_required
def product_create(request):
    """View to handle creation of a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Ürün başarıyla kaydedildi.')
            return redirect('uretim:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'uretim/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    """View to handle updating an existing product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürün başarıyla güncellendi.')
            return redirect('uretim:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    # Get related seeds
    seeds = product.seeds.all()
    
    context = {
        'form': form,
        'product': product,
        'seeds': seeds
    }
    
    return render(request, 'uretim/product_form.html', context)

@login_required
def seed_create(request, product_id=None):
    """View to handle creation of a new seed"""
    product = None
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = SeedForm(request.POST, initial={'product': product})
        if form.is_valid():
            seed = form.save()
            messages.success(request, 'Tohum başarıyla kaydedildi.')
            if product:
                return redirect('uretim:product_detail', pk=product.pk)
            else:
                return redirect('uretim:product_list')
    else:
        form = SeedForm(initial={'product': product})
    
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'uretim/seed_form.html', context)

@login_required
def seed_detail(request, pk):
    """View to display detailed information about a specific seed"""
    seed = get_object_or_404(Seed, pk=pk)
    
    # Get related plantings
    plantings = Planting.objects.filter(seed=seed)
    
    context = {
        'seed': seed,
        'plantings': plantings,
    }
    
    return render(request, 'uretim/seed_detail.html', context)

@login_required
def seed_update(request, pk):
    """View to handle updating an existing seed"""
    seed = get_object_or_404(Seed, pk=pk)
    
    if request.method == 'POST':
        form = SeedForm(request.POST, request.FILES, instance=seed)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tohum bilgileri başarıyla güncellendi.')
            return redirect('uretim:seed_detail', pk=seed.pk)
    else:
        form = SeedForm(instance=seed)
    
    context = {
        'form': form,
        'seed': seed
    }
    
    return render(request, 'uretim/seed_form.html', context)

@login_required
def planting_plan_list(request):
    """List all planting plans with search and filtering options"""
    # Get all lands belonging to the user
    lands = Land.objects.filter(owner=request.user, is_active=True)
    parcels = Parcel.objects.filter(land__in=lands, is_active=True)
    
    # Base queryset
    plans = PlantingPlan.objects.filter(parcel__in=parcels).select_related('parcel', 'product')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    completed = request.GET.get('completed', '')
    
    # Apply search filter
    if search_query:
        plans = plans.filter(
            Q(product__name__icontains=search_query) |
            Q(parcel__land__name__icontains=search_query) |
            Q(parcel__parcel_no__icontains=search_query)
        )
    
    # Apply completed filter
    if completed:
        is_completed = completed == 'true'
        plans = plans.filter(is_completed=is_completed)
    
    # Apply sorting
    plans = plans.order_by('planned_planting_date')
    
    # Pagination
    paginator = Paginator(plans, 10)  # 10 plans per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'completed': completed,
    }
    
    return render(request, 'uretim/planting_plan_list.html', context)

@login_required
def planting_plan_detail(request, pk):
    """View to display detailed information about a specific planting plan"""
    plan = get_object_or_404(PlantingPlan, pk=pk, parcel__land__owner=request.user)
    
    # Get related plantings
    plantings = Planting.objects.filter(planting_plan=plan)
    
    context = {
        'plan': plan,
        'plantings': plantings,
    }
    
    return render(request, 'uretim/planting_plan_detail.html', context)

@login_required
def planting_plan_update(request, pk):
    """View to handle updating an existing planting plan"""
    plan = get_object_or_404(PlantingPlan, pk=pk, parcel__land__owner=request.user)
    
    if request.method == 'POST':
        form = PlantingPlanForm(request.POST, user=request.user, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ekim planı başarıyla güncellendi.')
            return redirect('uretim:planting_plan_detail', pk=plan.pk)
    else:
        form = PlantingPlanForm(user=request.user, instance=plan)
    
    # Get related plantings
    plantings = Planting.objects.filter(planting_plan=plan)
    
    context = {
        'form': form,
        'plan': plan,
        'related_plantings': plantings
    }
    
    return render(request, 'uretim/planting_plan_form.html', context)

@login_required
def planting_plan_create(request, parcel_id=None):
    """View to handle creation of a new planting plan"""
    parcel = None
    if parcel_id:
        parcel = get_object_or_404(Parcel, pk=parcel_id, land__owner=request.user)
    
    if request.method == 'POST':
        form = PlantingPlanForm(request.POST, user=request.user, initial={'parcel': parcel})
        if form.is_valid():
            plan = form.save()
            messages.success(request, 'Ekim planı başarıyla kaydedildi.')
            return redirect('uretim:planting_plan_list')
    else:
        form = PlantingPlanForm(user=request.user, initial={'parcel': parcel})
    
    context = {
        'form': form,
        'parcel': parcel,
    }
    
    return render(request, 'uretim/planting_plan_form.html', context)

@login_required
def planting_list(request):
    """List all plantings with search and filtering options"""
    # Get all lands belonging to the user
    lands = Land.objects.filter(owner=request.user, is_active=True)
    parcels = Parcel.objects.filter(land__in=lands, is_active=True)
    
    # Base queryset
    plantings = Planting.objects.filter(parcel__in=parcels).select_related('parcel', 'product')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    product_filter = request.GET.get('product', '')
    
    # Apply search filter
    if search_query:
        plantings = plantings.filter(
            Q(product__name__icontains=search_query) |
            Q(parcel__land__name__icontains=search_query) |
            Q(parcel__parcel_no__icontains=search_query)
        )
    
    # Apply product filter
    if product_filter:
        plantings = plantings.filter(product_id=product_filter)
    
    # Apply sorting
    plantings = plantings.order_by('-planting_date')
    
    # Get all products for filter dropdown
    products = Product.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(plantings, 10)  # 10 plantings per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'product_filter': product_filter,
        'products': products,
    }
    
    return render(request, 'uretim/planting_list.html', context)

@login_required
def planting_create(request, plan_id=None):
    """View to handle creation of a new planting"""
    plan = None
    if plan_id:
        plan = get_object_or_404(PlantingPlan, pk=plan_id, parcel__land__owner=request.user)
    
    if request.method == 'POST':
        form = PlantingForm(request.POST, user=request.user, initial={'planting_plan': plan})
        if form.is_valid():
            planting = form.save()
            if plan:
                plan.is_completed = True
                plan.save()
            messages.success(request, 'Ekim başarıyla kaydedildi.')
            return redirect('uretim:planting_list')
    else:
        initial_data = {}
        if plan:
            initial_data = {
                'planting_plan': plan,
                'parcel': plan.parcel,
                'product': plan.product,
                'planting_date': plan.planned_planting_date,
                'estimated_harvest_date': plan.planned_harvest_date,
            }
        form = PlantingForm(user=request.user, initial=initial_data)
    
    context = {
        'form': form,
        'plan': plan,
    }
    
    return render(request, 'uretim/planting_form.html', context)

@login_required
def planting_detail(request, pk):
    """View to display detailed information about a specific planting"""
    planting = get_object_or_404(Planting, pk=pk, parcel__land__owner=request.user)
    
    # Check if harvest exists
    try:
        harvest = planting.harvest
        has_harvest = True
    except Harvest.DoesNotExist:
        harvest = None
        has_harvest = False
    
    context = {
        'planting': planting,
        'harvest': harvest,
        'has_harvest': has_harvest,
    }
    
    return render(request, 'uretim/planting_detail.html', context)

@login_required
def harvest_create(request, planting_id):
    """View to handle creation of a new harvest"""
    planting = get_object_or_404(Planting, pk=planting_id, parcel__land__owner=request.user)
    
    # Check if harvest already exists
    try:
        existing_harvest = planting.harvest
        messages.error(request, 'Bu ekim için zaten bir hasat kaydı bulunmaktadır.')
        return redirect('uretim:planting_detail', pk=planting.pk)
    except Harvest.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = HarvestForm(request.POST)
        if form.is_valid():
            harvest = form.save(commit=False)
            harvest.planting = planting
            harvest.save()
            messages.success(request, 'Hasat başarıyla kaydedildi.')
            return redirect('uretim:planting_detail', pk=planting.pk)
    else:
        form = HarvestForm()
    
    context = {
        'form': form,
        'planting': planting,
    }
    
    return render(request, 'uretim/harvest_form.html', context)

@login_required
def harvest_list(request):
    """List all harvests with search and filtering options"""
    # Get all lands belonging to the user
    lands = Land.objects.filter(owner=request.user, is_active=True)
    parcels = Parcel.objects.filter(land__in=lands, is_active=True)
    plantings = Planting.objects.filter(parcel__in=parcels)
    
    # Base queryset
    harvests = Harvest.objects.filter(planting__in=plantings).select_related('planting', 'planting__product')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    product_filter = request.GET.get('product', '')
    
    # Apply search filter
    if search_query:
        harvests = harvests.filter(
            Q(planting__product__name__icontains=search_query) |
            Q(planting__parcel__land__name__icontains=search_query) |
            Q(planting__parcel__parcel_no__icontains=search_query)
        )
    
    # Apply product filter
    if product_filter:
        harvests = harvests.filter(planting__product_id=product_filter)
    
    # Apply sorting
    harvests = harvests.order_by('-harvest_date')
    
    # Get all products for filter dropdown
    products = Product.objects.filter(is_active=True)
    
    # Calculate totals
    total_harvest = harvests.aggregate(Sum('harvest_amount'))['harvest_amount__sum'] or 0
    
    # Pagination
    paginator = Paginator(harvests, 10)  # 10 harvests per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'product_filter': product_filter,
        'products': products,
        'total_harvest': total_harvest,
    }
    
    return render(request, 'uretim/harvest_list.html', context)

def export_statistics(request):
    format = request.GET.get('format', 'pdf')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    product_id = request.GET.get('product')
    parcel_id = request.GET.get('parcel')

    # Filtreleme
    harvests = Harvest.objects.all()
    if start_date:
        harvests = harvests.filter(harvest_date__gte=start_date)
    if end_date:
        harvests = harvests.filter(harvest_date__lte=end_date)
    if product_id:
        harvests = harvests.filter(planting__product_id=product_id)
    if parcel_id:
        harvests = harvests.filter(planting__parcel_id=parcel_id)

    # İstatistikleri hesapla
    total_harvest_amount = harvests.aggregate(total=Sum('amount'))['total'] or 0
    total_cost = harvests.aggregate(total=Sum('total_cost'))['total'] or 0
    average_yield = harvests.aggregate(avg=Avg('yield_rate'))['avg'] or 0

    if format == 'pdf':
        template = get_template('uretim/statistics_pdf.html')
        context = {
            'harvests': harvests,
            'total_harvest_amount': total_harvest_amount,
            'total_cost': total_cost,
            'average_yield': average_yield,
            'start_date': start_date,
            'end_date': end_date,
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="uretim_raporu_{datetime.now().strftime("%Y%m%d")}.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF oluşturulurken bir hata oluştu')
        return response

    elif format == 'excel':
        # Excel için veri hazırla
        data = []
        for harvest in harvests:
            data.append({
                'Ürün': harvest.planting.product.name,
                'Parsel': harvest.planting.parcel.name,
                'Hasat Tarihi': harvest.harvest_date,
                'Miktar': harvest.amount,
                'Birim': harvest.get_unit_display(),
                'Verim': harvest.yield_rate,
                'Toplam Maliyet': harvest.total_cost,
            })

        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Hasat Raporu', index=False)
        
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="uretim_raporu_{datetime.now().strftime("%Y%m%d")}.xlsx"'
        return response

    elif format == 'csv':
        # CSV için veri hazırla
        data = []
        for harvest in harvests:
            data.append({
                'Ürün': harvest.planting.product.name,
                'Parsel': harvest.planting.parcel.name,
                'Hasat Tarihi': harvest.harvest_date,
                'Miktar': harvest.amount,
                'Birim': harvest.get_unit_display(),
                'Verim': harvest.yield_rate,
                'Toplam Maliyet': harvest.total_cost,
            })

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="uretim_raporu_{datetime.now().strftime("%Y%m%d")}.csv"'
        df.to_csv(response, index=False)
        return response

    return HttpResponse('Geçersiz format', status=400)

@login_required
def statistics(request):
    """View to display production statistics and reports"""
    # Get all lands belonging to the user
    lands = Land.objects.filter(owner=request.user, is_active=True)
    parcels = Parcel.objects.filter(land__in=lands, is_active=True)
    plantings = Planting.objects.filter(parcel__in=parcels)
    
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    product_id = request.GET.get('product')
    parcel_id = request.GET.get('parcel')
    
    # Base queryset
    harvests = Harvest.objects.filter(planting__in=plantings)
    
    # Apply filters
    if start_date:
        harvests = harvests.filter(harvest_date__gte=start_date)
    if end_date:
        harvests = harvests.filter(harvest_date__lte=end_date)
    if product_id:
        harvests = harvests.filter(planting__product_id=product_id)
    if parcel_id:
        harvests = harvests.filter(planting__parcel_id=parcel_id)
    
    # Calculate general statistics
    total_planting_area = plantings.aggregate(total=Sum('planting_area'))['total'] or 0
    total_harvest_amount = harvests.aggregate(total=Sum('amount'))['total'] or 0
    total_cost = harvests.aggregate(total=Sum('total_cost'))['total'] or 0
    average_yield = harvests.aggregate(avg=Avg('yield_rate'))['avg'] or 0
    
    # Calculate product statistics
    product_stats = []
    products = Product.objects.filter(plantings__in=plantings).distinct()
    for product in products:
        product_harvests = harvests.filter(planting__product=product)
        product_plantings = plantings.filter(product=product)
        
        stats = {
            'product': product,
            'planting_area': product_plantings.aggregate(total=Sum('planting_area'))['total'] or 0,
            'harvest_amount': product_harvests.aggregate(total=Sum('amount'))['total'] or 0,
            'total_cost': product_harvests.aggregate(total=Sum('total_cost'))['total'] or 0,
            'average_yield': product_harvests.aggregate(avg=Avg('yield_rate'))['avg'] or 0,
            'unit': product_harvests.first().get_unit_display() if product_harvests.exists() else '-',
        }
        
        if stats['harvest_amount'] > 0:
            stats['unit_cost'] = stats['total_cost'] / stats['harvest_amount']
        else:
            stats['unit_cost'] = 0
            
        product_stats.append(stats)
    
    # Calculate parcel statistics
    parcel_stats = []
    for parcel in parcels:
        parcel_harvests = harvests.filter(planting__parcel=parcel)
        parcel_plantings = plantings.filter(parcel=parcel)
        
        if parcel_harvests.exists():
            stats = {
                'parcel': parcel,
                'product': parcel_harvests.first().planting.product,
                'planting_area': parcel_plantings.aggregate(total=Sum('planting_area'))['total'] or 0,
                'harvest_amount': parcel_harvests.aggregate(total=Sum('amount'))['total'] or 0,
                'total_cost': parcel_harvests.aggregate(total=Sum('total_cost'))['total'] or 0,
                'yield': parcel_harvests.aggregate(avg=Avg('yield_rate'))['avg'] or 0,
                'unit': parcel_harvests.first().get_unit_display(),
            }
            parcel_stats.append(stats)
    
    # Calculate maintenance statistics
    maintenance_stats = []
    maintenance_types = dict(MaintenanceRecord.MAINTENANCE_TYPE_CHOICES)
    for type_code, type_name in maintenance_types.items():
        records = MaintenanceRecord.objects.filter(planting__in=plantings, maintenance_type=type_code)
        if records.exists():
            stats = {
                'maintenance_type': type_code,
                'get_maintenance_type_display': type_name,
                'count': records.count(),
                'total_cost': records.aggregate(total=Sum('total_cost'))['total'] or 0,
                'average_cost': records.aggregate(avg=Avg('total_cost'))['avg'] or 0,
                'total_area': records.aggregate(total=Sum('area'))['total'] or 0,
            }
            maintenance_stats.append(stats)
    
    # Calculate cost percentages
    labor_cost = harvests.aggregate(total=Sum('labor_cost'))['total'] or 0
    material_cost = harvests.aggregate(total=Sum('material_cost'))['total'] or 0
    equipment_cost = harvests.aggregate(total=Sum('equipment_cost'))['total'] or 0
    
    if total_cost > 0:
        labor_cost_percentage = (labor_cost / total_cost) * 100
        material_cost_percentage = (material_cost / total_cost) * 100
        equipment_cost_percentage = (equipment_cost / total_cost) * 100
    else:
        labor_cost_percentage = material_cost_percentage = equipment_cost_percentage = 0
    
    # Get all products and parcels for filter dropdowns
    all_products = Product.objects.filter(is_active=True)
    all_parcels = parcels
    
    context = {
        'total_planting_area': total_planting_area,
        'total_harvest_amount': total_harvest_amount,
        'total_cost': total_cost,
        'average_yield': average_yield,
        'product_stats': product_stats,
        'parcel_stats': parcel_stats,
        'maintenance_stats': maintenance_stats,
        'labor_cost': labor_cost,
        'material_cost': material_cost,
        'equipment_cost': equipment_cost,
        'labor_cost_percentage': labor_cost_percentage,
        'material_cost_percentage': material_cost_percentage,
        'equipment_cost_percentage': equipment_cost_percentage,
        'products': all_products,
        'parcels': all_parcels,
        'selected_product': product_id,
        'selected_parcel': parcel_id,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'uretim/statistics.html', context)
