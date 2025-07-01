from django.db import models
from culturesvegetables.models import CultureVegetable
from meteorologicaldatas.models import MeteorologicalData

class IrrigationVolume(models.Model):
    phase_initial = models.FloatField() 
    phase_vegetative = models.FloatField()
    phase_flowering = models.FloatField()
    phase_fruiting = models.FloatField() 
    phase_maturation = models.FloatField()
    date = models.DateField(auto_now=True)
    culturevegetable = models.ForeignKey(
        CultureVegetable, 
        on_delete=models.CASCADE,
        blank=False
    )
    meteorologicaldata = models.OneToOneField(
        MeteorologicalData, 
        on_delete=models.CASCADE,
        blank=False
    )

    def __str__(self):
        return f"Irrigation Volume ({self.date.strftime('%Y-%m-%d %H:%M:%S')})"
