from django.db import models

class CultureVegetable(models.Model):
    name = models.CharField(max_length=255)
    phase_germination_kc = models.FloatField()
    phase_vegetative_kc = models.FloatField()
    phase_emerging_kc = models.FloatField()
    phase_frying_kc = models.FloatField()
    phase_maturation_kc = models.FloatField()

    def __str__(self):
        return self.name
