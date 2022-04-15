from django.contrib import admin

# Register your models here.

from apps.date_extraction.models import DateExtraction
admin.site.register(DateExtraction)
