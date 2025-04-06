from django.contrib import admin
from .models import (
    TaskCategory, Worker, Equipment, Task, 
    TaskComment, WorkLog, MaintenanceSchedule
)

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'icon', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position', 'phone', 'email', 'is_active']
    list_filter = ['is_active', 'position']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    fieldsets = [
        ('Kişisel Bilgiler', {'fields': ['user', 'first_name', 'last_name', 'birth_date', 'is_active']}),
        ('İletişim Bilgileri', {'fields': ['phone', 'email', 'address']}),
        ('İş Bilgileri', {'fields': ['position', 'hire_date', 'hourly_rate', 'daily_rate', 'specializations']}),
        ('Diğer', {'fields': ['notes', 'owner']}),
    ]

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'model', 'manufacturer', 'status', 'is_active']
    list_filter = ['equipment_type', 'status', 'is_active']
    search_fields = ['name', 'model', 'manufacturer', 'serial_number']
    fieldsets = [
        ('Temel Bilgiler', {'fields': ['name', 'equipment_type', 'model', 'manufacturer', 'status', 'is_active']}),
        ('Finansal Bilgiler', {'fields': ['purchase_date', 'purchase_price']}),
        ('Teknik Bilgiler', {'fields': ['serial_number']}),
        ('Diğer', {'fields': ['notes', 'owner']}),
    ]

class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 1

class WorkLogInline(admin.TabularInline):
    model = WorkLog
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'priority', 'planned_start_date', 'planned_end_date', 'completion_percentage']
    list_filter = ['status', 'priority', 'category', 'is_recurring', 'is_active']
    search_fields = ['title', 'description']
    date_hierarchy = 'planned_start_date'
    filter_horizontal = ['assigned_workers', 'equipment_needed']
    inlines = [TaskCommentInline, WorkLogInline]
    fieldsets = [
        ('Temel Bilgiler', {'fields': ['title', 'description', 'category', 'status', 'priority', 'is_active']}),
        ('Tarihler', {'fields': ['planned_start_date', 'planned_end_date', 'actual_start_date', 'actual_end_date']}),
        ('Zaman Planlaması', {'fields': ['estimated_hours', 'actual_hours']}),
        ('Tekrarlama', {'fields': ['is_recurring', 'recurrence_pattern', 'recurrence_details', 'parent_task']}),
        ('Atamalar', {'fields': ['assigned_workers', 'equipment_needed']}),
        ('İlişkili Kayıtlar', {'fields': ['related_land', 'related_parcel', 'related_planting', 'related_animal', 'related_animal_group']}),
        ('Maliyet', {'fields': ['estimated_cost', 'actual_cost']}),
        ('Tamamlama', {'fields': ['completion_percentage', 'completion_notes']}),
        ('Sistem', {'fields': ['created_by', 'owner']}),
    ]

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['comment', 'task__title']
    date_hierarchy = 'created_at'

@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ['task', 'worker', 'date', 'start_time', 'end_time', 'hours_worked']
    list_filter = ['date', 'worker']
    search_fields = ['task__title', 'worker__first_name', 'worker__last_name', 'description']
    date_hierarchy = 'date'

@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'title', 'interval_value', 'interval_unit', 'last_maintenance_date', 'next_maintenance_date']
    list_filter = ['interval_unit', 'next_maintenance_date']
    search_fields = ['title', 'equipment__name', 'description']
    date_hierarchy = 'next_maintenance_date'
