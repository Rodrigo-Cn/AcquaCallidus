from django.db import models

class Log(models.Model):
    reference = models.CharField(max_length=255)
    exception = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.reference} - {self.created_at}"
