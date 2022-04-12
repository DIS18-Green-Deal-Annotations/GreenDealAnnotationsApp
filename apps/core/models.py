from django.db import models


class Documents(models.Model):
    id = models.BigAutoField(
        primary_key=True,
    )

    name = models.TextField()
