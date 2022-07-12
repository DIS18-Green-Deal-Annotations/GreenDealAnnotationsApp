"""GreenDealAnnotations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import TemplateView
from apps.core.views import index
from apps.core.views import DocumentViewer
from apps.core.views import test_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('timeline/', include('apps.date_extraction.urls')),
    path('classification/', include('apps.document_classification.urls')),
    path('test/<str:id>/', test_page, name='test'),
    path('documentviewer', DocumentViewer),
    #path('core/', include('apps.core.urls')),
    path('', index),
]