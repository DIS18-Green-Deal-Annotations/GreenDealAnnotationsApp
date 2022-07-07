from django.contrib import admin

from .models import DateExtraction, HtmlCode


class DateExtractionAdmin(admin.ModelAdmin):
    fields = ['__all__']


class HtmlCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'html')
    # search_fields=('title', 'description') #create search field in the model admin


admin.site.register(DateExtraction, DateExtractionAdmin)
admin.site.register(HtmlCode, HtmlCodeAdmin)
