"""
URL configuration for tarim_hay_takip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from kullanici.views import home_view, login_view, logout_view, register_view, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Kullanıcı işlemleri
    path('', home_view, name='home'),
    path('giris/', login_view, name='login'),
    path('cikis/', logout_view, name='logout'),
    path('kayit/', register_view, name='register'),
    path('profilim/', profile_view, name='profile'),
    
    # Uygulama URL'leri
    path('hayvan/', include('hayvan.urls', namespace='hayvan')),
    path('arazi/', include('arazi.urls', namespace='arazi')),
    path('uretim/', include('uretim.urls', namespace='uretim')),
    # path('stok/', include('stok.urls')),
    # path('finans/', include('finans.urls')),
    # path('gorev/', include('gorev.urls')),
    # path('analitik/', include('analitik.urls')),
]

# Geliştirme ortamında statik ve medya dosyalarına erişim
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
