from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import Product, Seed, PlantingPlan, Planting, Harvest
from arazi.models import Land, Parcel
from .forms import ProductForm, SeedForm, PlantingPlanForm, PlantingForm, HarvestForm

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
