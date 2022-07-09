import uuid

from django.db import models


# ----- GRUPPE DOCUMENT LINKING -----

class Document(models.Model):  # EHEMALS CodeHtml
    FILE_TYPE_CHOICES = [
        ('html', 'html'),
        ('pdf', 'pdf')
    ]

    # id jetzt automatisch generiert statt uuid
    html_content = models.TextField(blank=True, null=True)  # EHEMALS HTML
    eu_id = models.CharField(max_length=18, default="no_title", unique=True) # EHEMALS DOCUMENT; enthält CELEX oder COM id
    title = models.CharField(max_length=200)  # title of the document on official website
    subtitle = models.CharField(max_length=200)  # title of the doc in html -> usually document title or a subtitle
    scope = models.CharField(max_length=200)  # main html title declaring a document as COMMUNICATION, REGULATION, DIRECTIVE, etc.
    url = models.URLField()  # URL to original html document
    file_type = models.CharField(max_length=4, choices=FILE_TYPE_CHOICES)  # type of document
    publish_date = models.DateField()

    class Meta:
        app_label = "core"


# ----- GRUPPE DATE EXTRACTION -----

class Sentence(models.Model):  # EHEMALS DateExtraction
    doc_reference = models.ForeignKey(
        Document,
        on_delete=models.PROTECT,
    ) # EHEMALS DOCNAME -> voller name des dokumentes
    sentence = models.TextField() # EHEMALS docsentence
    date_label = models.CharField(max_length=10) # EHEMALS datelabel
    date_iso = models.CharField(max_length=10)  # do we need a string or a date? EHEMALS isodate

    class Meta:
        app_label = "core"
