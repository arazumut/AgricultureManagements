from django.urls import path
from . import views

app_name = 'gorev'

urlpatterns = [
    path('gorevler/', views.task_list, name='task_list'),
    path('gorevler/takvim/', views.task_calendar, name='task_calendar'),
    path('calisanlar/', views.worker_list, name='worker_list'),
    path('calisma-kayitlari/', views.worklog_list, name='worklog_list'),
    path('ekipmanlar/', views.equipment_list, name='equipment_list'),
    path('bakim-programlari/', views.maintenance_list, name='maintenance_list'),
] 