from django.db import models
from ..core.models import Documents

# Create your models here.

class Date(models.Models):
    document = models.ForeignKey(
        Documents,
        on_delete=models.CASCADE,
    )