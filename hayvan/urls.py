from django.urls import path
from . import views

app_name = 'hayvan'

urlpatterns = [
    # Hayvan işlemleri
    path('', views.animal_list, name='animal_list'),
    path('<int:pk>/', views.animal_detail, name='animal_detail'),
    path('ekle/', views.animal_create, name='animal_create'),
    path('<int:pk>/duzenle/', views.animal_update, name='animal_update'),
    path('<int:pk>/sil/', views.animal_delete, name='animal_delete'),
    
    # Sağlık kayıtları
    path('<int:animal_id>/saglik-kaydi/ekle/', views.health_record_create, name='health_record_create'),
    
    # Üreme kayıtları
    path('<int:animal_id>/ureme-kaydi/ekle/', views.reproduction_record_create, name='reproduction_record_create'),
    
    # Doğum kayıtları
    path('<int:animal_id>/dogum-kaydi/ekle/', views.birth_record_create, name='birth_record_create'),
    path('<int:animal_id>/dogum-kaydi/ekle/<int:reproduction_id>/', views.birth_record_create, name='birth_record_create_from_reproduction'),
    
    # Besleme kayıtları
    path('<int:animal_id>/besleme-kaydi/ekle/', views.feeding_create, name='feeding_create'),
    path('grup/<int:group_id>/besleme-kaydi/ekle/', views.feeding_create, name='group_feeding_create'),
    
    # İstatistikler ve raporlar
    path('istatistikler/', views.herd_statistics, name='herd_statistics'),
] 