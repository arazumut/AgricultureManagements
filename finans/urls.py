# Author: Umut Araz
# Date: 2025-04-08

from django.urls import path
from . import views

app_name = 'finans'

urlpatterns = [
    path('islemler/', views.transaction_list, name='transaction_list'),
    path('faturalar/', views.invoice_list, name='invoice_list'),
    path('faturalar/ekle/', views.invoice_create, name='invoice_create'),
    path('hesaplar/', views.bank_account_list, name='bank_account_list'),
    path('kategoriler/', views.account_category_list, name='account_category_list'),
    path('musteriler/', views.customer_list, name='customer_list'),
    path('butceler/', views.budget_list, name='budget_list'),
] 