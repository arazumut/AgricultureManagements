from django.urls import path
from . import views

app_name = 'gorev'

urlpatterns = [
    path('gorevler/', views.task_list, name='task_list'),
    path('gorevler/takvim/', views.task_calendar, name='task_calendar'),
    path('calisanlar/', views.worker_list, name='worker_list'),
    path('calisma-kayitlari/', views.worklog_list, name='worklog_list'),
    path('calisma-kayitlari/ekle/', views.worklog_create, name='worklog_create'),
    path('calisma-kayitlari/<int:pk>/duzenle/', views.worklog_update, name='worklog_update'),
    path('calisma-kayitlari/<int:pk>/sil/', views.worklog_delete, name='worklog_delete'),
    path('ekipmanlar/', views.equipment_list, name='equipment_list'),
    path('ekipmanlar/ekle/', views.equipment_create, name='equipment_create'),
    path('ekipmanlar/<int:pk>/duzenle/', views.equipment_update, name='equipment_update'),
    path('ekipmanlar/<int:pk>/sil/', views.equipment_delete, name='equipment_delete'),
    path('bakim-programlari/', views.maintenance_list, name='maintenance_list'),
] 