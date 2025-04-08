from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Worker, WorkLog, Equipment, MaintenanceSchedule

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
    worklogs = WorkLog.objects.all().order_by('-date')
    return render(request, 'gorev/worklog_list.html', {
        'worklogs': worklogs
    })

@login_required
def equipment_list(request):
    """Ekipmanları listeler"""
    equipments = Equipment.objects.all().order_by('name')
    return render(request, 'gorev/equipment_list.html', {
        'equipments': equipments
    })

@login_required
def maintenance_list(request):
    """Bakım programlarını listeler"""
    maintenances = MaintenanceSchedule.objects.all().order_by('-next_maintenance_date')
    return render(request, 'gorev/maintenance_list.html', {
        'maintenances': maintenances
    })
