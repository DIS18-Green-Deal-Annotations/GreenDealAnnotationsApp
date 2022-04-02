from django.db import models


class TestModel(models.Model):
    text = models.TextField()

    def __str__(self):
        return 'EinTestModell mit der ID: ' + str(self.id)

    class Meta:
        verbose_name = 'TestModell'
        verbose_name_plural = 'TestModelle'
