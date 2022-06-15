from django.db import models
import uuid

class HtmlCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    html = models.TextField()
    document = models.TextField(default="no_title")