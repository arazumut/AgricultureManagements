from django.urls import path
from . import views

app_name = 'hayvan'

urlpatterns = [
    # Hayvan türü yönetimi
    path('turler/', views.animal_type_list, name='animal_type_list'),
    path('turler/ekle/', views.animal_type_create, name='animal_type_create'),
    path('turler/<int:pk>/duzenle/', views.animal_type_update, name='animal_type_update'),
    path('turler/<int:pk>/sil/', views.animal_type_delete, name='animal_type_delete'),
    
    # Hayvan ırkı yönetimi
    path('irklar/', views.animal_breed_list, name='animal_breed_list'),
    path('irklar/ekle/', views.animal_breed_create, name='animal_breed_create'),
    path('irklar/<int:pk>/duzenle/', views.animal_breed_update, name='animal_breed_update'),
    path('irklar/<int:pk>/sil/', views.animal_breed_delete, name='animal_breed_delete'),
    
    # Hayvan grubu yönetimi
    path('gruplar/', views.animal_group_list, name='animal_group_list'),
    path('gruplar/ekle/', views.animal_group_create, name='animal_group_create'),
    path('gruplar/<int:pk>/duzenle/', views.animal_group_update, name='animal_group_update'),
    path('gruplar/<int:pk>/sil/', views.animal_group_delete, name='animal_group_delete'),
    
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
    path('ajax/load-breeds/', views.load_breeds, name='ajax_load_breeds'),
] 