from django.urls import path
from . import views

app_name = 'arazi'

urlpatterns = [
    # Arazi işlemleri
    path('', views.land_list, name='land_list'),
    path('<int:pk>/', views.land_detail, name='land_detail'),
    path('ekle/', views.land_create, name='land_create'),
    path('<int:pk>/duzenle/', views.land_update, name='land_update'),
    path('<int:pk>/sil/', views.land_delete, name='land_delete'),
    
    # Parsel işlemleri
    path('<int:land_id>/parsel/ekle/', views.parcel_create, name='parcel_create'),
    path('<int:land_id>/parsel/<int:parcel_id>/', views.parcel_detail, name='parcel_detail'),
    
    # Toprak analizi işlemleri
    path('<int:land_id>/parsel/<int:parcel_id>/toprak-analizi/ekle/', views.soil_analysis_create, name='soil_analysis_create'),
    
    # Sulama kayıtları işlemleri
    path('<int:land_id>/parsel/<int:parcel_id>/sulama-kaydi/ekle/', views.irrigation_record_create, name='irrigation_record_create'),
] 