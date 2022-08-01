from django.contrib import admin

from .models import Document, Sentence, TABLES, TABLE_CATEGORIES


class SentenceAdmin(admin.ModelAdmin):
    fields = ['__all__']



class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'eu_id', 'html_content', 'title', 'subtitle', 'scope')
    # search_fields=('title', 'description') #create search field in the model admin

admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Document, DocumentAdmin)

# TABLE EXTRACTION
class TABLESAdmin(admin.ModelAdmin):
    list_display = ('id', 'ComNr', 'DocID', 'TableNr', 'Filename', 'TableContentHTML', 'get_catids')
class TABLE_CATEGORIESAdmin(admin.ModelAdmin):
    list_display = ('id', 'Cat')

admin.site.register(TABLES, TABLESAdmin)
admin.site.register(TABLE_CATEGORIES, TABLE_CATEGORIESAdmin)