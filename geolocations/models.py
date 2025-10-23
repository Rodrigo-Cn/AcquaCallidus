from django.db import models

class Geolocation(models.Model):
    property_name = models.CharField(max_length=255, default='Fazenda')
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.city}, {self.state}"
