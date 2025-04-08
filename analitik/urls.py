from django.urls import path
from . import views

app_name = 'analitik'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
] 