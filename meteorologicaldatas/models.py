from django.db import models

class MeteorologicalData(models.Model):
    temperature_max = models.FloatField()
    temperature_min = models.FloatField()
    relative_humidity = models.FloatField()
    solar_radiation = models.FloatField()
    air_speed = models.FloatField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Dados Meteorológicos - {self.date}"
