from django.contrib import admin

# Register your models here.

from apps.date_extraction.models import DateExtraction
from apps.core.models import HtmlCode


class HtmlCodeAdmin(admin.ModelAdmin):
    list_display=('id', 'document' ,'html')
    #search_fields=('title', 'description') #create search field in the model admin

admin.site.register(DateExtraction)
