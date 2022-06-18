
from django.urls import include, path
from .views import test_page


urlpatterns = [
    path('test/<str:id>/', test_page , name='test'),
]