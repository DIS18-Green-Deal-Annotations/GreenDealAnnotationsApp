from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from core.views import index
from core.views import DocumentViewer, timeline

urlpatterns = [
    # pages by groups
    path('timeline/', timeline),
    path('documentviewer/<str:id>/', DocumentViewer),

    # general
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('', index),
]