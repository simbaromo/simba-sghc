"""sghc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls

from core.api import *
from core.views import subir_dicom, FileFieldFormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/historiaclinica/', HistoriaClinicaView.as_view(), name='historiaclinica_view'),
    path('dicom/subir/', FileFieldFormView.as_view(), name='subir_dicom'),
    path('api/v1/historiaclinica/<int:pk>/', HistoriaClinicaDetail.as_view(), name='historiaclinica_detail'),
    path('api/v1/coreapi/', include_docs_urls(title=settings.ADMIN_SITE_NAME, permission_classes=(permissions.AllowAny,))),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = 'Sistema de Gestión de Historias Clínicas'
admin.site.site_title = "SGHC"
