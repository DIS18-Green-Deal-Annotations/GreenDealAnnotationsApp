from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from core.views import index
from core.views import DocumentViewer, timeline, browse_documents, tables

urlpatterns = [
    # pages by groups
    path('timeline/', timeline, name='timeline'),
    path('documentviewer/<int:id>/', DocumentViewer, name='document_details'),
    path('documentviewer/', browse_documents, name='all_documents'),
    path('tableviewer/', tables, name='tables'),

    # general
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('', index),
]