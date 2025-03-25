from django.db import models

class IrrigationVolume(models.Model):
    phase_germination = models.FloatField()
    phase_vegetative = models.FloatField()
    phase_emergence = models.FloatField()
    phase_frying = models.FloatField()
    phase_maturation = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date

