from django.db import models
from geolocations.models import Geolocation

class MeteorologicalData(models.Model):
    temperature_max = models.FloatField()
    temperature_min = models.FloatField()
    relative_humidity = models.FloatField()
    solar_radiation = models.FloatField()
    air_speed = models.FloatField()
    pressure = models.FloatField()
    date = models.DateField(auto_now=True)
    geolocation = models.ForeignKey(
        Geolocation, 
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Dados Meteorológicos - {self.date}"
