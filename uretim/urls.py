from django.urls import path
from . import views

app_name = 'uretim'

urlpatterns = [
    # Ürün işlemleri
    path('urunler/', views.product_list, name='product_list'),
    path('urunler/<int:pk>/', views.product_detail, name='product_detail'),
    path('urunler/ekle/', views.product_create, name='product_create'),
    path('urunler/<int:pk>/duzenle/', views.product_update, name='product_update'),
    
    # Tohum işlemleri
    path('tohumlar/ekle/', views.seed_create, name='seed_create'),
    path('urunler/<int:product_id>/tohum/ekle/', views.seed_create, name='seed_create_for_product'),
    path('tohumlar/<int:pk>/', views.seed_detail, name='seed_detail'),
    path('tohumlar/<int:pk>/duzenle/', views.seed_update, name='seed_update'),
    
    # Ekim planı işlemleri
    path('ekim-planlari/', views.planting_plan_list, name='planting_plan_list'),
    path('ekim-planlari/ekle/', views.planting_plan_create, name='planting_plan_create'),
    path('arazi/<int:parcel_id>/ekim-plani/ekle/', views.planting_plan_create, name='planting_plan_create_for_parcel'),
    path('ekim-planlari/<int:pk>/', views.planting_plan_detail, name='planting_plan_detail'),
    path('ekim-planlari/<int:pk>/duzenle/', views.planting_plan_update, name='planting_plan_update'),
    
    # Ekim işlemleri
    path('ekimler/', views.planting_list, name='planting_list'),
    path('ekimler/<int:pk>/', views.planting_detail, name='planting_detail'),
    path('ekimler/ekle/', views.planting_create, name='planting_create'),
    path('ekim-planlari/<int:plan_id>/ekle/', views.planting_create, name='planting_create_from_plan'),
    
    # Hasat işlemleri
    path('hasatlar/', views.harvest_list, name='harvest_list'),
    path('ekimler/<int:planting_id>/hasat/ekle/', views.harvest_create, name='harvest_create'),
] 