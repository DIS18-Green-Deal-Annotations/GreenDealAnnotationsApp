import uuid

from django.db import models


# ----- GRUPPE DOCUMENT LINKING -----

class HtmlCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    html = models.TextField()
    document = models.TextField(default="no_title")

    class Meta:
        app_label = "core"


# ----- GRUPPE DATE EXTRACTION -----

class DateExtraction(models.Model):
    docname = models.CharField(max_length=500)
    docsentence = models.TextField()
    datelabel = models.CharField(max_length=10)
    isodate = models.CharField(max_length=10)  # do we need a string or a date?

    class Meta:
        app_label = "core"
