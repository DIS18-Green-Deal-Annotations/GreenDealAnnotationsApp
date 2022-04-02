from django.contrib import admin
from apps.core.models import TestModel

# Register your models here.
@admin.register(TestModel)
class TestModelAmdin(admin.ModelAdmin):
    list_display = ['id', 'text']