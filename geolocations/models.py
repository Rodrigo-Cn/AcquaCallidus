from django.db import models

class Geolocation(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.city}, {self.state}"
