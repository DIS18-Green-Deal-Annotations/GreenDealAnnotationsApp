from django.db import models


# Create your models here.

class DocumentClassification(models.Model):
    header = models.TextField()
    header2 = models.TextField()
    body = models.TextField()
    doctype = models.CharField(max_length=255)
    titreobjet = models.CharField(max_length=255)
    comnumber = models.CharField(max_length=255)
    structure = models.CharField(max_length=255)
    deskriptor = models.TextField()
