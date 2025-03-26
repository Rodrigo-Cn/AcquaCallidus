from django.db import models
from django.utils import timezone

class Log(models.Model):
    reference = models.CharField(max_length=255)
    exception = models.JSONField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Log {self.reference} - {self.created_at}"
