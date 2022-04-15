from django.db import models

# Create your models here.

class DateExtraction(models.Model):
    DocName = models.CharField(max_length=50)
    DocSentence = models.TextField()
    DateLabel = models.CharField(max_length=10) 
    IsoDate = models.CharField(max_length=10) # do we need a string or a date?
