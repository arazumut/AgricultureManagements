from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Supplier, UnitOfMeasure, InventoryItem, StockTransaction, Warehouse, InventoryLocation
from django.db.models import Count, Sum, Q, ProtectedError
from .forms import WarehouseForm, UnitForm, InventoryItemForm, StockTransactionForm

# Create your views here.

@login_required
def category_list(request):
    """Kategori listesi görüntüleme"""
    categories = Category.objects.filter(parent=None).annotate(
        subcategory_count=Count('subcategories'),
        item_count=Count('inventory_items')
    )
    return render(request, 'stok/category_list.html', {
        'categories': categories,
        'title': 'Kategoriler'
    })

@login_required
def category_create(request):
    """Yeni kategori oluşturma"""
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        description = request.POST.get('description')
        
        try:
            category = Category(
                name=name,
                description=description
            )
            if parent_id:
                category.parent = Category.objects.get(id=parent_id)
            category.save()
            messages.success(request, 'Kategori başarıyla oluşturuldu.')
            return redirect('stok:category_list')
        except Exception as e:
            messages.error(request, f'Kategori oluşturulurken bir hata oluştu: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'stok/category_form.html', {
        'categories': categories,
        'title': 'Yeni Kategori'
    })

@login_required
def category_update(request, pk):
    """Kategori düzenleme"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        description = request.POST.get('description')
        
        try:
            category.name = name
            category.description = description
            if parent_id and int(parent_id) != category.id:  # Kendisini parent olarak seçemez
                category.parent = Category.objects.get(id=parent_id)
            else:
                category.parent = None
            category.save()
            messages.success(request, 'Kategori başarıyla güncellendi.')
            return redirect('stok:category_list')
        except Exception as e:
            messages.error(request, f'Kategori güncellenirken bir hata oluştu: {str(e)}')
    
    categories = Category.objects.exclude(pk=pk)  # Kendisi hariç diğer kategoriler
    return render(request, 'stok/category_form.html', {
        'category': category,
        'categories': categories,
        'title': 'Kategori Düzenle'
    })

@login_required
def category_delete(request, pk):
    """Kategori silme"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        try:
            if category.inventory_items.exists():
                messages.error(request, 'Bu kategoriye ait ürünler bulunduğu için silinemez.')
                return redirect('stok:category_list')
            
            category.delete()
            messages.success(request, 'Kategori başarıyla silindi.')
            return redirect('stok:category_list')
        except Exception as e:
            messages.error(request, f'Kategori silinirken bir hata oluştu: {str(e)}')
            return redirect('stok:category_list')
    
    return render(request, 'stok/category_confirm_delete.html', {
        'category': category,
        'title': 'Kategori Sil'
    })

@login_required
def supplier_list(request):
    """Tedarikçi listesi görüntüleme"""
    suppliers = Supplier.objects.annotate(
        item_count=Count('inventory_items'),
        transaction_count=Count('transactions')
    )
    return render(request, 'stok/supplier_list.html', {
        'suppliers': suppliers,
        'title': 'Tedarikçiler'
    })

@login_required
def supplier_create(request):
    """Yeni tedarikçi oluşturma"""
    if request.method == 'POST':
        try:
            supplier = Supplier(
                name=request.POST.get('name'),
                contact_person=request.POST.get('contact_person'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
                website=request.POST.get('website'),
                tax_number=request.POST.get('tax_number'),
                notes=request.POST.get('notes')
            )
            supplier.save()
            messages.success(request, 'Tedarikçi başarıyla oluşturuldu.')
            return redirect('stok:supplier_list')
        except Exception as e:
            messages.error(request, f'Tedarikçi oluşturulurken bir hata oluştu: {str(e)}')
    
    return render(request, 'stok/supplier_form.html', {
        'title': 'Yeni Tedarikçi'
    })

@login_required
def supplier_update(request, pk):
    """Tedarikçi düzenleme"""
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        try:
            supplier.name = request.POST.get('name')
            supplier.contact_person = request.POST.get('contact_person')
            supplier.phone = request.POST.get('phone')
            supplier.email = request.POST.get('email')
            supplier.address = request.POST.get('address')
            supplier.website = request.POST.get('website')
            supplier.tax_number = request.POST.get('tax_number')
            supplier.notes = request.POST.get('notes')
            supplier.is_active = request.POST.get('is_active') == 'on'
            supplier.save()
            messages.success(request, 'Tedarikçi başarıyla güncellendi.')
            return redirect('stok:supplier_list')
        except Exception as e:
            messages.error(request, f'Tedarikçi güncellenirken bir hata oluştu: {str(e)}')
    
    return render(request, 'stok/supplier_form.html', {
        'supplier': supplier,
        'title': 'Tedarikçi Düzenle'
    })

@login_required
def supplier_delete(request, pk):
    """Tedarikçi silme"""
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        try:
            if supplier.inventory_items.exists():
                messages.error(request, 'Bu tedarikçiye ait ürünler bulunduğu için silinemez.')
                return redirect('stok:supplier_list')
            
            if supplier.transactions.exists():
                messages.error(request, 'Bu tedarikçiye ait işlemler bulunduğu için silinemez.')
                return redirect('stok:supplier_list')
            
            supplier.delete()
            messages.success(request, 'Tedarikçi başarıyla silindi.')
            return redirect('stok:supplier_list')
        except Exception as e:
            messages.error(request, f'Tedarikçi silinirken bir hata oluştu: {str(e)}')
            return redirect('stok:supplier_list')
    
    return render(request, 'stok/supplier_confirm_delete.html', {
        'supplier': supplier,
        'title': 'Tedarikçi Sil'
    })

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    context = {
        'supplier': supplier,
        'transactions': supplier.transactions.all().order_by('-transaction_date')[:10]  # Son 10 işlem
    }
    return render(request, 'stok/supplier_detail.html', context)

@login_required
def unit_list(request):
    """Ölçü birimlerini listeler"""
    units = UnitOfMeasure.objects.all()
    return render(request, 'stok/unit_list.html', {'units': units})

@login_required
def unit_create(request):
    """Yeni ölçü birimi oluşturur"""
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ölçü birimi başarıyla oluşturuldu.')
            return redirect('stok:unit_list')
    else:
        form = UnitForm()
    return render(request, 'stok/unit_form.html', {'form': form})

@login_required
def unit_update(request, pk):
    """Ölçü birimini günceller"""
    unit = get_object_or_404(UnitOfMeasure, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ölçü birimi başarıyla güncellendi.')
            return redirect('stok:unit_list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'stok/unit_form.html', {'form': form})

@login_required
def unit_delete(request, pk):
    """Ölçü birimini siler"""
    unit = get_object_or_404(UnitOfMeasure, pk=pk)
    try:
        unit.delete()
        messages.success(request, 'Ölçü birimi başarıyla silindi.')
    except ProtectedError:
        messages.error(request, 'Bu ölçü birimi kullanımda olduğu için silinemez.')
    return redirect('stok:unit_list')

@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'stok/warehouse_list.html', {
        'warehouses': warehouses
    })

@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            try:
                warehouse = form.save()
                messages.success(request, 'Depo başarıyla oluşturuldu.')
                return redirect('stok:warehouse_list')
            except Exception as e:
                messages.error(request, f'Depo oluşturulurken bir hata oluştu: {str(e)}')
    else:
        form = WarehouseForm()
    
    return render(request, 'stok/warehouse_form.html', {
        'form': form,
        'title': 'Yeni Depo Ekle'
    })

@login_required
def warehouse_update(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            try:
                warehouse = form.save()
                messages.success(request, 'Depo başarıyla güncellendi.')
                return redirect('stok:warehouse_list')
            except Exception as e:
                messages.error(request, f'Depo güncellenirken bir hata oluştu: {str(e)}')
    else:
        form = WarehouseForm(instance=warehouse)
    
    return render(request, 'stok/warehouse_form.html', {
        'form': form,
        'warehouse': warehouse,
        'title': 'Depo Düzenle'
    })

@login_required
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    
    if request.method == 'POST':
        try:
            if warehouse.inventory_items.exists():
                messages.error(request, 'Bu depoda stok kalemleri bulunduğu için silinemez.')
                return redirect('stok:warehouse_list')
            
            if warehouse.locations.exists():
                messages.error(request, 'Bu depoda konumlar bulunduğu için silinemez.')
                return redirect('stok:warehouse_list')
            
            warehouse.delete()
            messages.success(request, 'Depo başarıyla silindi.')
            return redirect('stok:warehouse_list')
        except Exception as e:
            messages.error(request, f'Depo silinirken bir hata oluştu: {str(e)}')
            return redirect('stok:warehouse_list')
    
    return render(request, 'stok/warehouse_confirm_delete.html', {
        'warehouse': warehouse
    })

@login_required
def warehouse_detail(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    locations = warehouse.locations.all()
    inventory_items = warehouse.inventory_items.all()
    
    return render(request, 'stok/warehouse_detail.html', {
        'warehouse': warehouse,
        'locations': locations,
        'inventory_items': inventory_items
    })

@login_required
def inventory_list(request):
    """Stok kalemlerini listeler"""
    items = InventoryItem.objects.filter(owner=request.user)
    return render(request, 'stok/inventory_list.html', {
        'items': items,
        'title': 'Stok Kalemleri'
    })

@login_required
def inventory_create(request):
    """Yeni stok kalemi oluşturur"""
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Stok kalemi başarıyla oluşturuldu.')
            return redirect('stok:inventory_list')
    else:
        form = InventoryItemForm()
    return render(request, 'stok/inventory_form.html', {
        'form': form,
        'title': 'Yeni Stok Kalemi'
    })

@login_required
def inventory_detail(request, pk):
    """Stok kalemi detaylarını gösterir"""
    item = get_object_or_404(InventoryItem, pk=pk, owner=request.user)
    return render(request, 'stok/inventory_detail.html', {
        'item': item,
        'title': item.name
    })

@login_required
def inventory_update(request, pk):
    """Stok kalemini günceller"""
    item = get_object_or_404(InventoryItem, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stok kalemi başarıyla güncellendi.')
            return redirect('stok:inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'stok/inventory_form.html', {
        'form': form,
        'title': 'Stok Kalemi Düzenle'
    })

@login_required
def inventory_delete(request, pk):
    """Stok kalemini siler"""
    item = get_object_or_404(InventoryItem, pk=pk, owner=request.user)
    try:
        item.delete()
        messages.success(request, 'Stok kalemi başarıyla silindi.')
    except ProtectedError:
        messages.error(request, 'Bu stok kalemi kullanımda olduğu için silinemez.')
    return redirect('stok:inventory_list')

@login_required
def transaction_list(request):
    """Stok hareketlerini listeler"""
    transactions = StockTransaction.objects.filter(created_by=request.user).select_related(
        'item', 'supplier', 'item__unit'
    ).order_by('-transaction_date')
    return render(request, 'stok/transaction_list.html', {
        'transactions': transactions,
        'title': 'Stok Hareketleri'
    })

@login_required
def transaction_create(request):
    """Yeni stok hareketi oluşturur"""
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            messages.success(request, 'Stok hareketi başarıyla oluşturuldu.')
            return redirect('stok:transaction_list')
    else:
        form = StockTransactionForm()
    return render(request, 'stok/transaction_form.html', {
        'form': form,
        'title': 'Yeni Stok Hareketi'
    })

@login_required
def transaction_detail(request, pk):
    """Stok hareketi detaylarını gösterir"""
    transaction = get_object_or_404(StockTransaction, pk=pk, created_by=request.user)
    return render(request, 'stok/transaction_detail.html', {
        'transaction': transaction,
        'title': f"{transaction.item.name} - {transaction.get_transaction_type_display()}"
    })

@login_required
def transaction_update(request, pk):
    """Stok hareketini günceller"""
    transaction = get_object_or_404(StockTransaction, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = StockTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stok hareketi başarıyla güncellendi.')
            return redirect('stok:transaction_list')
    else:
        form = StockTransactionForm(instance=transaction)
    return render(request, 'stok/transaction_form.html', {
        'form': form,
        'title': 'Stok Hareketi Düzenle'
    })

@login_required
def transaction_delete(request, pk):
    """Stok hareketini siler"""
    transaction = get_object_or_404(StockTransaction, pk=pk, created_by=request.user)
    try:
        transaction.delete()
        messages.success(request, 'Stok hareketi başarıyla silindi.')
    except ProtectedError:
        messages.error(request, 'Bu stok hareketi silinemez.')
    return redirect('stok:transaction_list')
