from django.urls import path
from . import views

app_name = 'stok'  # İsim alanı tanımı

urlpatterns = [
    # Kategori yönetimi
    path('kategoriler/', views.category_list, name='category_list'),
    path('kategoriler/ekle/', views.category_create, name='category_create'),
    path('kategoriler/<int:pk>/duzenle/', views.category_update, name='category_update'),
    path('kategoriler/<int:pk>/sil/', views.category_delete, name='category_delete'),

    # Tedarikçi yönetimi
    path('tedarikciler/', views.supplier_list, name='supplier_list'),
    path('tedarikciler/ekle/', views.supplier_create, name='supplier_create'),
    path('tedarikciler/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('tedarikciler/<int:pk>/duzenle/', views.supplier_update, name='supplier_update'),
    path('tedarikciler/<int:pk>/sil/', views.supplier_delete, name='supplier_delete'),

    # Ölçü Birimleri
    path('birimler/', views.unit_list, name='unit_list'),
    path('birimler/ekle/', views.unit_create, name='unit_create'),
    path('birimler/<int:pk>/duzenle/', views.unit_update, name='unit_update'),
    path('birimler/<int:pk>/sil/', views.unit_delete, name='unit_delete'),

    # Depo yönetimi
    path('depolar/', views.warehouse_list, name='warehouse_list'),
    path('depolar/ekle/', views.warehouse_create, name='warehouse_create'),
    path('depolar/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    path('depolar/<int:pk>/duzenle/', views.warehouse_update, name='warehouse_update'),
    path('depolar/<int:pk>/sil/', views.warehouse_delete, name='warehouse_delete'),

    # Stok kalemleri yönetimi
    path('stok-kalemleri/', views.inventory_list, name='inventory_list'),
    path('stok-kalemleri/ekle/', views.inventory_create, name='inventory_create'),
    path('stok-kalemleri/<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('stok-kalemleri/<int:pk>/duzenle/', views.inventory_update, name='inventory_update'),
    path('stok-kalemleri/<int:pk>/sil/', views.inventory_delete, name='inventory_delete'),

    # Stok hareketleri yönetimi
    path('hareketler/', views.transaction_list, name='transaction_list'),
    path('hareketler/ekle/', views.transaction_create, name='transaction_create'),
    path('hareketler/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('hareketler/<int:pk>/duzenle/', views.transaction_update, name='transaction_update'),
    path('hareketler/<int:pk>/sil/', views.transaction_delete, name='transaction_delete'),
] 