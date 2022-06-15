from django.db import models

# Create your models here.

class DateExtraction(models.Model):
    docname = models.CharField(max_length=500)
    docsentence = models.TextField()
    datelabel = models.CharField(max_length=10) 
    isodate = models.CharField(max_length=10) # do we need a string or a date?