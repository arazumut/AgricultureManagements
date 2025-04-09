from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Task, Worker, WorkLog, Equipment, MaintenanceSchedule
from .forms import WorkLogForm, EquipmentForm

# Create your views here.

@login_required
def task_list(request):
    """Görevleri listeler"""
    tasks = Task.objects.all().order_by('-planned_end_date')
    return render(request, 'gorev/task_list.html', {
        'tasks': tasks
    })

@login_required
def task_calendar(request):
    """Görev takvimini gösterir"""
    tasks = Task.objects.all().order_by('planned_end_date')
    return render(request, 'gorev/task_calendar.html', {
        'tasks': tasks
    })

@login_required
def worker_list(request):
    """Çalışanları listeler"""
    workers = Worker.objects.all().order_by('last_name', 'first_name')
    return render(request, 'gorev/worker_list.html', {
        'workers': workers
    })

@login_required
def worklog_list(request):
    """Çalışma kayıtlarını listeler"""
    worklogs = WorkLog.objects.all().order_by('-start_time')
    
    # Sayfalama
    paginator = Paginator(worklogs, 10)  # Her sayfada 10 kayıt
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gorev/worklog_list.html', {
        'worklogs': page_obj,
        'is_paginated': True,
        'page_obj': page_obj
    })

@login_required
def equipment_list(request):
    """Ekipmanları listeler"""
    equipments = Equipment.objects.all().order_by('name')
    
    # Sayfalama
    paginator = Paginator(equipments, 10)  # Her sayfada 10 kayıt
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gorev/equipment_list.html', {
        'equipments': page_obj,
        'is_paginated': True,
        'page_obj': page_obj
    })

@login_required
def maintenance_list(request):
    """Bakım programlarını listeler"""
    maintenances = MaintenanceSchedule.objects.all().order_by('-next_maintenance_date')
    return render(request, 'gorev/maintenance_list.html', {
        'maintenances': maintenances
    })

@login_required
def worklog_create(request):
    """Yeni çalışma kaydı oluşturur"""
    if request.method == 'POST':
        form = WorkLogForm(request.POST)
        if form.is_valid():
            worklog = form.save()
            messages.success(request, 'Çalışma kaydı başarıyla oluşturuldu.')
            return redirect('gorev:worklog_list')
    else:
        form = WorkLogForm()
    
    return render(request, 'gorev/worklog_form.html', {
        'form': form,
        'title': 'Yeni Çalışma Kaydı'
    })

@login_required
def worklog_update(request, pk):
    """Çalışma kaydını günceller"""
    worklog = get_object_or_404(WorkLog, pk=pk)
    
    if request.method == 'POST':
        form = WorkLogForm(request.POST, instance=worklog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Çalışma kaydı başarıyla güncellendi.')
            return redirect('gorev:worklog_list')
    else:
        form = WorkLogForm(instance=worklog)
    
    return render(request, 'gorev/worklog_form.html', {
        'form': form,
        'title': 'Çalışma Kaydını Düzenle',
        'worklog': worklog
    })

@login_required
def worklog_delete(request, pk):
    """Çalışma kaydını siler"""
    worklog = get_object_or_404(WorkLog, pk=pk)
    
    if request.method == 'POST':
        worklog.delete()
        messages.success(request, 'Çalışma kaydı başarıyla silindi.')
        return redirect('gorev:worklog_list')
    
    return render(request, 'gorev/worklog_confirm_delete.html', {
        'worklog': worklog
    })

@login_required
def equipment_create(request):
    """Yeni ekipman oluşturur"""
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.owner = request.user
            equipment.save()
            messages.success(request, 'Ekipman başarıyla oluşturuldu.')
            return redirect('gorev:equipment_list')
    else:
        form = EquipmentForm()
    
    return render(request, 'gorev/equipment_form.html', {
        'form': form,
        'title': 'Yeni Ekipman'
    })

@login_required
def equipment_update(request, pk):
    """Ekipmanı günceller"""
    equipment = get_object_or_404(Equipment, pk=pk)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ekipman başarıyla güncellendi.')
            return redirect('gorev:equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    
    return render(request, 'gorev/equipment_form.html', {
        'form': form,
        'title': 'Ekipmanı Düzenle',
        'equipment': equipment
    })

@login_required
def equipment_delete(request, pk):
    """Ekipmanı siler"""
    equipment = get_object_or_404(Equipment, pk=pk)
    
    if request.method == 'POST':
        equipment.delete()
        messages.success(request, 'Ekipman başarıyla silindi.')
        return redirect('gorev:equipment_list')
    
    return render(request, 'gorev/equipment_confirm_delete.html', {
        'equipment': equipment
    })
