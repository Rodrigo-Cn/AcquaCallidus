from django.db import models
from django.core.validators import MinValueValidator

class CultureVegetable(models.Model):
    name = models.CharField(max_length=255)
    phase_initial_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    phase_vegetative_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    phase_flowering_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    phase_fruiting_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    phase_maturation_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    radiusM2 = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return self.name
