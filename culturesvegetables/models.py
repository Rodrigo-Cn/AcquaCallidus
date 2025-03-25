from django.db import models

class CultureVegetable(models.Model):
    name = models.CharField(max_length=255)
    phase_germination = models.FloatField()
    phase_vegetative = models.FloatField()
    phase_emergence = models.FloatField()
    phase_frying = models.FloatField()
    phase_maturation = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return self.name
