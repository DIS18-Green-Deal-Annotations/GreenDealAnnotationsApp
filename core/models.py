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
    com_id = models.CharField(max_length=18, unique=True, blank=True, null=True) # blank und null true für Schreibprozess
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


# ----- GRUPPE DOCUMENT CLASSIFICATION -----

class Paragraphs(models.Model):
    """
    Removed fields:
    body -> redundant if clean_body exists
    titreobject -> exists in Document as subtitle
    doctype -> exists in Document as scope
    Altered fields:
    comnumber -> used as foreign key to connect do Document model
    """
    header = models.TextField()
    header2 = models.TextField()
    comnumber = models.ForeignKey(
        Document,
        on_delete=models.PROTECT,
    )
    structure = models.TextField()
    cleanbody = models.TextField()
    weightedsimilarities = models.TextField() # should this be text instead of number?
    deskriptor = models.TextField() # should this be text instead of foreign key?

    class Meta:
        app_label = "core"