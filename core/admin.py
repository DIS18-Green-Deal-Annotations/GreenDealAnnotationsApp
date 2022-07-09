from django.contrib import admin

from .models import Document, Sentence


class SentenceAdmin(admin.ModelAdmin):
    fields = ['__all__']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'eu_id', 'html_content', 'title', 'subtitle', 'scope')
    # search_fields=('title', 'description') #create search field in the model admin


admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Document, DocumentAdmin)