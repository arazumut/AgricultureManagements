from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.utils.translation import gettext as _
from .models import Animal, AnimalType, AnimalBreed, HealthRecord, ReproductionRecord, Birth, Feeding, AnimalGroup
from .forms import AnimalForm, HealthRecordForm, ReproductionRecordForm, BirthForm, AnimalTypeForm, AnimalBreedForm, AnimalGroupForm
from datetime import datetime
from django.views.decorators.http import require_GET

@login_required
def animal_list(request):
    """List all animals with search and filtering options"""
    # Base queryset
    animals = Animal.objects.all()
    
    # Get all animal types for filter dropdown
    animal_types = AnimalType.objects.all()
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    selected_type = request.GET.get('type', '')
    selected_sort = request.GET.get('sort', '-created_at')
    
    # Apply search filter
    if search_query:
        animals = animals.filter(
            Q(tag_number__icontains=search_query) |
            Q(animal_type__name__icontains=search_query) |
            Q(breed__name__icontains=search_query)
        )
    
    # Apply type filter
    if selected_type:
        animals = animals.filter(animal_type_id=selected_type)
    
    # Apply sorting
    if selected_sort == 'oldest':
        animals = animals.order_by('birth_date')
    elif selected_sort == 'youngest':
        animals = animals.order_by('-birth_date')
    else:
        animals = animals.order_by(selected_sort)
    
    # Pagination
    paginator = Paginator(animals, 10)  # 10 animals per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_type': selected_type,
        'selected_sort': selected_sort,
        'animal_types': animal_types,
    }
    
    return render(request, 'hayvan/animal_list.html', context)

@login_required
def animal_detail(request, pk):
    """
    View to display detailed information about a specific animal
    """
    animal = get_object_or_404(Animal, pk=pk, owner=request.user)
    
    # Get related health records
    health_records = animal.health_records.all().order_by('-procedure_date')
    
    # Get related reproduction records (for female animals)
    reproduction_records = None
    births = None
    
    if animal.gender == 'F':
        reproduction_records = animal.reproduction_records.all().order_by('-insemination_date')
        births = animal.births.all().order_by('-birth_date')
    
    # Hesapla istatistikler
    health_stats = animal.get_health_statistics()
    reproduction_stats = None
    
    if animal.gender == 'F':
        reproduction_stats = animal.get_reproduction_statistics()
    
    # Akraba hayvanları getir
    related_animals = animal.get_related_animals()
    
    # Yem tüketimi
    feed_consumption = animal.get_feed_consumption(days=30)
    
    context = {
        'animal': animal,
        'health_records': health_records,
        'reproduction_records': reproduction_records,
        'births': births,
        'health_stats': health_stats,
        'reproduction_stats': reproduction_stats,
        'related_animals': related_animals,
        'feed_consumption': feed_consumption,
    }
    
    return render(request, 'hayvan/animal_detail.html', context)

@login_required
def animal_create(request):
    """
    View to handle creation of a new animal
    """
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if tag number already exists
            tag_number = form.cleaned_data['tag_number']
            if Animal.objects.filter(tag_number=tag_number).exists():
                messages.error(request, _('Zaten bu küpe numarasına sahip bir hayvan kaydı bulunmaktadır.'))
                return render(request, 'hayvan/animal_form.html', {'form': form})
            
            animal = form.save(commit=False)
            animal.owner = request.user
            animal.save()
            
            messages.success(request, _('Hayvan başarıyla kaydedildi.'))
            return redirect('hayvan:animal_detail', pk=animal.pk)
    else:
        form = AnimalForm()
    
    # Get all animal types and breeds for the form
    animal_types = AnimalType.objects.all().order_by('name')
    animal_breeds = AnimalBreed.objects.none()  # Initially empty
    
    context = {
        'form': form,
        'animal_types': animal_types,
        'animal_breeds': animal_breeds,
    }
    
    return render(request, 'hayvan/animal_form.html', context)

@login_required
def animal_update(request, pk):
    """
    View to handle updating an existing animal
    """
    animal = get_object_or_404(Animal, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            # Check if tag number changed and already exists
            tag_number = form.cleaned_data['tag_number']
            if tag_number != animal.tag_number and Animal.objects.filter(tag_number=tag_number).exists():
                messages.error(request, _('Zaten bu küpe numarasına sahip bir hayvan kaydı bulunmaktadır.'))
                return render(request, 'hayvan/animal_form.html', {'form': form, 'animal': animal})
            
            form.save()
            messages.success(request, _('Hayvan bilgileri başarıyla güncellendi.'))
            return redirect('hayvan:animal_detail', pk=animal.pk)
    else:
        form = AnimalForm(instance=animal)
    
    return render(request, 'hayvan/animal_form.html', {'form': form, 'animal': animal})

@login_required
def animal_delete(request, pk):
    """
    View to handle animal deletion (soft delete by marking as inactive)
    """
    animal = get_object_or_404(Animal, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        # Confirm checkbox is required
        if request.POST.get('confirm_delete'):
            animal.is_active = False
            animal.save()
            messages.success(request, _('Hayvan başarıyla silindi.'))
            return redirect('hayvan:animal_list')
        else:
            messages.error(request, _('Silme işlemini onaylamanız gerekmektedir.'))
    
    return render(request, 'hayvan/animal_delete.html', {'animal': animal})

@login_required
def health_record_create(request, animal_id):
    """
    View to handle creation of a new health record for an animal
    """
    animal = get_object_or_404(Animal, pk=animal_id, owner=request.user)
    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.animal = animal
            health_record.save()
            
            messages.success(request, _('Sağlık kaydı başarıyla oluşturuldu.'))
            return redirect('hayvan:animal_detail', pk=animal.pk)
    else:
        form = HealthRecordForm()
    
    context = {
        'form': form,
        'animal': animal
    }
    
    return render(request, 'hayvan/health_record_form.html', context)

@login_required
def reproduction_record_create(request, animal_id):
    """
    View to handle creation of a new reproduction record for a female animal
    """
    animal = get_object_or_404(Animal, pk=animal_id, owner=request.user)
    
    # Only female animals can have reproduction records
    if animal.gender != 'F':
        messages.error(request, _('Sadece dişi hayvanlar için üreme kaydı oluşturabilirsiniz.'))
        return redirect('hayvan:animal_detail', pk=animal.pk)
    
    if request.method == 'POST':
        form = ReproductionRecordForm(request.POST)
        if form.is_valid():
            reproduction_record = form.save(commit=False)
            reproduction_record.animal = animal
            reproduction_record.save()
            
            messages.success(request, _('Üreme kaydı başarıyla oluşturuldu.'))
            return redirect('hayvan:animal_detail', pk=animal.pk)
    else:
        form = ReproductionRecordForm()
    
    context = {
        'form': form,
        'animal': animal
    }
    
    return render(request, 'hayvan/reproduction_record_form.html', context)

@login_required
def birth_record_create(request, animal_id, reproduction_id=None):
    """
    View to handle creation of a new birth record for a female animal
    """
    animal = get_object_or_404(Animal, pk=animal_id, owner=request.user)
    reproduction_record = None
    
    # Only female animals can have birth records
    if animal.gender != 'F':
        messages.error(request, _('Sadece dişi hayvanlar için doğum kaydı oluşturabilirsiniz.'))
        return redirect('hayvan:animal_detail', pk=animal.pk)
    
    if reproduction_id:
        reproduction_record = get_object_or_404(ReproductionRecord, pk=reproduction_id, animal=animal)
    
    if request.method == 'POST':
        form = BirthForm(request.POST)
        if form.is_valid():
            birth = form.save(commit=False)
            birth.animal = animal
            if reproduction_record:
                birth.reproduction_record = reproduction_record
                # Update the reproduction record status
                reproduction_record.pregnancy_status = 'birth_completed'
                reproduction_record.save()
            birth.save()
            
            messages.success(request, _('Doğum kaydı başarıyla oluşturuldu.'))
            return redirect('hayvan:animal_detail', pk=animal.pk)
    else:
        form = BirthForm(initial={'reproduction_record': reproduction_record})
    
    context = {
        'form': form,
        'animal': animal,
        'reproduction_record': reproduction_record
    }
    
    return render(request, 'hayvan/birth_record_form.html', context)

@login_required
def feeding_create(request, animal_id=None, group_id=None):
    """
    Besleme kaydı oluşturma görünümü
    """
    animal = None
    animal_group = None
    
    if animal_id:
        animal = get_object_or_404(Animal, pk=animal_id, owner=request.user)
    elif group_id:
        animal_group = get_object_or_404(AnimalGroup, pk=group_id, owner=request.user)
        
    if not animal and not animal_group:
        messages.error(request, _('Besleme kaydı için bir hayvan veya grup seçilmelidir.'))
        return redirect('hayvan:animal_list')
        
    if request.method == 'POST':
        # Form alanlarını al
        feeding_date = request.POST.get('feeding_date')
        amount = request.POST.get('amount')
        feed_ration_id = request.POST.get('feed_ration') or None
        description = request.POST.get('description', '')
        
        # Temel doğrulama
        if not feeding_date or not amount:
            messages.error(request, _('Tarih ve miktar alanları doldurulmalıdır.'))
        else:
            try:
                # Besleme kaydı oluştur
                feeding = Feeding(
                    animal=animal,
                    animal_group=animal_group,
                    feeding_date=feeding_date,
                    amount=float(amount),
                    description=description
                )
                
                if feed_ration_id:
                    feeding.feed_ration_id = feed_ration_id
                    
                feeding.save()
                
                if animal:
                    messages.success(request, _('Besleme kaydı başarıyla oluşturuldu.'))
                    return redirect('hayvan:animal_detail', pk=animal.pk)
                else:
                    messages.success(request, _('Grup besleme kaydı başarıyla oluşturuldu.'))
                    return redirect('hayvan:animal_list')  # TODO: Grup detay sayfasına yönlendir
            except Exception as e:
                messages.error(request, _('Besleme kaydı oluşturulurken bir hata oluştu: {0}').format(str(e)))
    
    context = {
        'animal': animal,
        'animal_group': animal_group,
    }
    
    return render(request, 'hayvan/feeding_form.html', context)

@login_required
def herd_statistics(request):
    """
    Sürü istatistikleri görünümü
    """
    stats = Animal.get_herd_statistics(request.user)
    
    context = {
        'stats': stats,
    }
    
    return render(request, 'hayvan/herd_statistics.html', context)

@require_GET
@login_required
def load_breeds(request):
    """
    AJAX view to load breeds for a selected animal type
    """
    animal_type_id = request.GET.get('animal_type')
    
    if not animal_type_id:
        return JsonResponse({'error': 'Hayvan türü belirtilmedi'}, status=400)
    
    try:
        breeds = AnimalBreed.objects.filter(animal_type_id=animal_type_id).order_by('name')
        data = [{'id': breed.id, 'name': breed.name} for breed in breeds]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def animal_type_list(request):
    """Hayvan türlerini listeler"""
    animal_types = AnimalType.objects.all().order_by('name')
    return render(request, 'hayvan/animal_type_list.html', {
        'animal_types': animal_types
    })

@login_required
def animal_type_create(request):
    """Yeni hayvan türü oluşturur"""
    if request.method == 'POST':
        form = AnimalTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hayvan türü başarıyla oluşturuldu.')
            return redirect('hayvan:animal_type_list')
    else:
        form = AnimalTypeForm()
    
    return render(request, 'hayvan/animal_type_form.html', {
        'form': form,
        'title': 'Yeni Hayvan Türü Ekle'
    })

@login_required
def animal_type_update(request, pk):
    """Hayvan türünü günceller"""
    animal_type = get_object_or_404(AnimalType, pk=pk)
    
    if request.method == 'POST':
        form = AnimalTypeForm(request.POST, instance=animal_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hayvan türü başarıyla güncellendi.')
            return redirect('hayvan:animal_type_list')
    else:
        form = AnimalTypeForm(instance=animal_type)
    
    return render(request, 'hayvan/animal_type_form.html', {
        'form': form,
        'title': 'Hayvan Türünü Düzenle',
        'animal_type': animal_type
    })

@login_required
def animal_type_delete(request, pk):
    """Hayvan türünü siler"""
    animal_type = get_object_or_404(AnimalType, pk=pk)
    
    if request.method == 'POST':
        try:
            animal_type.delete()
            messages.success(request, 'Hayvan türü başarıyla silindi.')
            return redirect('hayvan:animal_type_list')
        except Exception as e:
            messages.error(request, f'Hayvan türü silinirken bir hata oluştu: {str(e)}')
            return redirect('hayvan:animal_type_list')
    
    return render(request, 'hayvan/animal_type_confirm_delete.html', {
        'animal_type': animal_type
    })

@login_required
def animal_breed_list(request):
    """Hayvan ırklarını listeler"""
    animal_breeds = AnimalBreed.objects.all().order_by('animal_type__name', 'name')
    return render(request, 'hayvan/animal_breed_list.html', {
        'animal_breeds': animal_breeds
    })

@login_required
def animal_breed_create(request):
    """Yeni hayvan ırkı oluşturur"""
    if request.method == 'POST':
        form = AnimalBreedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hayvan ırkı başarıyla oluşturuldu.')
            return redirect('hayvan:animal_breed_list')
    else:
        form = AnimalBreedForm()
    
    return render(request, 'hayvan/animal_breed_form.html', {
        'form': form,
        'title': 'Yeni Hayvan Irkı Ekle'
    })

@login_required
def animal_breed_update(request, pk):
    """Hayvan ırkını günceller"""
    animal_breed = get_object_or_404(AnimalBreed, pk=pk)
    
    if request.method == 'POST':
        form = AnimalBreedForm(request.POST, instance=animal_breed)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hayvan ırkı başarıyla güncellendi.')
            return redirect('hayvan:animal_breed_list')
    else:
        form = AnimalBreedForm(instance=animal_breed)
    
    return render(request, 'hayvan/animal_breed_form.html', {
        'form': form,
        'title': 'Hayvan Irkını Düzenle',
        'animal_breed': animal_breed
    })

@login_required
def animal_breed_delete(request, pk):
    """Hayvan ırkını siler"""
    animal_breed = get_object_or_404(AnimalBreed, pk=pk)
    
    if request.method == 'POST':
        try:
            animal_breed.delete()
            messages.success(request, 'Hayvan ırkı başarıyla silindi.')
            return redirect('hayvan:animal_breed_list')
        except Exception as e:
            messages.error(request, f'Hayvan ırkı silinirken bir hata oluştu: {str(e)}')
            return redirect('hayvan:animal_breed_list')
    
    return render(request, 'hayvan/animal_breed_confirm_delete.html', {
        'animal_breed': animal_breed
    })

@login_required
def animal_group_list(request):
    """Hayvan gruplarını listeler"""
    animal_groups = AnimalGroup.objects.all().order_by('name')
    return render(request, 'hayvan/animal_group_list.html', {
        'animal_groups': animal_groups
    })

@login_required
def animal_group_create(request):
    """Yeni hayvan grubu oluşturur"""
    if request.method == 'POST':
        form = AnimalGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hayvan grubu başarıyla oluşturuldu.')
            return redirect('hayvan:animal_group_list')
    else:
        form = AnimalGroupForm()
    
    return render(request, 'hayvan/animal_group_form.html', {
        'form': form,
        'title': 'Yeni Hayvan Grubu Ekle'
    })

@login_required
def animal_group_update(request, pk):
    """Hayvan grubunu günceller"""
    animal_group = get_object_or_404(AnimalGroup, pk=pk)
    
    if request.method == 'POST':
        form = AnimalGroupForm(request.POST, instance=animal_group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hayvan grubu başarıyla güncellendi.')
            return redirect('hayvan:animal_group_list')
    else:
        form = AnimalGroupForm(instance=animal_group)
    
    return render(request, 'hayvan/animal_group_form.html', {
        'form': form,
        'title': 'Hayvan Grubunu Düzenle',
        'animal_group': animal_group
    })

@login_required
def animal_group_delete(request, pk):
    """Hayvan grubunu siler"""
    animal_group = get_object_or_404(AnimalGroup, pk=pk)
    
    if request.method == 'POST':
        try:
            animal_group.delete()
            messages.success(request, 'Hayvan grubu başarıyla silindi.')
            return redirect('hayvan:animal_group_list')
        except Exception as e:
            messages.error(request, f'Hayvan grubu silinirken bir hata oluştu: {str(e)}')
            return redirect('hayvan:animal_group_list')
    
    return render(request, 'hayvan/animal_group_confirm_delete.html', {
        'animal_group': animal_group
    })

@login_required
def health_record_list(request):
    """Tüm sağlık kayıtlarını listeler"""
    # Base queryset
    health_records = HealthRecord.objects.select_related('animal', 'animal__animal_type').all()
    
    # Get all animal types for filter dropdown
    animal_types = AnimalType.objects.all()
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    selected_type = request.GET.get('animal_type', '')
    selected_procedure = request.GET.get('procedure_type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Apply search filter
    if search_query:
        health_records = health_records.filter(
            Q(animal__tag_number__icontains=search_query) |
            Q(procedure_name__icontains=search_query) |
            Q(veterinarian__icontains=search_query) |
            Q(notes__icontains=search_query)
        )
    
    # Apply animal type filter
    if selected_type:
        health_records = health_records.filter(animal__animal_type_id=selected_type)
    
    # Apply procedure type filter
    if selected_procedure:
        health_records = health_records.filter(procedure_type=selected_procedure)
    
    # Apply date range filters
    if date_from:
        health_records = health_records.filter(procedure_date__gte=date_from)
    
    if date_to:
        health_records = health_records.filter(procedure_date__lte=date_to)
    
    # Order by procedure date (newest first)
    health_records = health_records.order_by('-procedure_date')
    
    # Pagination
    paginator = Paginator(health_records, 10)  # 10 records per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'animal_types': animal_types,
    }
    
    return render(request, 'hayvan/health_record_list.html', context)

@login_required
def health_record_update(request, pk):
    """Sağlık kaydını günceller"""
    health_record = get_object_or_404(HealthRecord, pk=pk)
    animal = health_record.animal
    
    # Check if the user owns the animal
    if animal.owner != request.user:
        messages.error(request, _('Bu sağlık kaydını düzenleme yetkiniz yok.'))
        return redirect('hayvan:health_record_list')
    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            messages.success(request, _('Sağlık kaydı başarıyla güncellendi.'))
            return redirect('hayvan:animal_detail', pk=animal.pk)
    else:
        form = HealthRecordForm(instance=health_record)
    
    context = {
        'form': form,
        'animal': animal,
        'health_record': health_record
    }
    
    return render(request, 'hayvan/health_record_form.html', context)

@login_required
def health_record_delete(request, pk):
    """Sağlık kaydını siler"""
    health_record = get_object_or_404(HealthRecord, pk=pk)
    animal = health_record.animal
    
    # Check if the user owns the animal
    if animal.owner != request.user:
        messages.error(request, _('Bu sağlık kaydını silme yetkiniz yok.'))
        return redirect('hayvan:health_record_list')
    
    if request.method == 'POST':
        # Confirm delete checkbox is required
        if request.POST.get('confirm_delete'):
            health_record.delete()
            messages.success(request, _('Sağlık kaydı başarıyla silindi.'))
            return redirect('hayvan:animal_detail', pk=animal.pk)
        else:
            messages.error(request, _('Silme işlemini onaylamanız gerekmektedir.'))
    
    context = {
        'health_record': health_record,
        'animal': animal
    }
    
    return render(request, 'hayvan/health_record_confirm_delete.html', context)

@login_required
def bulk_feeding(request):
    """
    Birden fazla hayvan için toplu besleme kaydı oluşturan görünüm
    """
    # Tüm aktif hayvanları al
    animals = Animal.objects.filter(is_active=True).select_related('animal_type', 'breed')
    animal_types = AnimalType.objects.all()
    animal_groups = AnimalGroup.objects.all()
    
    if request.method == 'POST':
        # Form verilerini al
        feeding_date = request.POST.get('feeding_date')
        feed_type = request.POST.get('feed_type')
        notes = request.POST.get('notes', '')
        selected_animals = request.POST.getlist('selected_animals')
        
        # Temel doğrulama
        if not feeding_date or not feed_type or not selected_animals:
            messages.error(request, _('Tarih, yem türü ve en az bir hayvan seçilmelidir.'))
        else:
            # Başarılı kayıt sayısı
            success_count = 0
            error_count = 0
            
            # Seçilen her hayvan için besleme kaydı oluştur
            for animal_id in selected_animals:
                try:
                    animal = Animal.objects.get(id=animal_id, is_active=True)
                    amount = request.POST.get(f'amount_{animal_id}')
                    
                    if amount and float(amount) > 0:
                        # Besleme kaydı oluştur
                        Feeding.objects.create(
                            animal=animal,
                            feeding_date=feeding_date,
                            feed_type=feed_type,
                            amount=float(amount),
                            description=notes
                        )
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Besleme kaydı oluşturulurken hata: {str(e)}")
            
            if success_count > 0:
                messages.success(request, _(f'{success_count} hayvan için besleme kaydı başarıyla oluşturuldu.'))
                
            if error_count > 0:
                messages.warning(request, _(f'{error_count} hayvan için besleme kaydı oluşturulamadı. Lütfen miktarları kontrol edin.'))
                
            if success_count > 0:
                return redirect('hayvan:animal_list')
    
    # Bugünün tarihini context'e ekle
    from datetime import date
    today = date.today()
    
    context = {
        'animals': animals,
        'animal_types': animal_types,
        'animal_groups': animal_groups,
        'today': today,
    }
    
    return render(request, 'hayvan/bulk_feeding_form.html', context)
