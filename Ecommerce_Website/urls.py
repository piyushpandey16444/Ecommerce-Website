"""Ecommerce_Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from hoitymoppet import views
from des import urls as des_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('checkout/', include('checkout.urls')),
    path('', views.index),
    path('hoitymoppet/', include('hoitymoppet.urls')),
    path('accounts/', include('accounts.urls')),
    path('hoitymoppet/', include('generic_links.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', include(('vali.urls','vali'), namespace='dashboard')),
    path('django-des/', include(des_urls)),

    # path('', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)