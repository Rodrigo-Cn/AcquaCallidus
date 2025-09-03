import random
import string
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from culturesvegetables.models import CultureVegetable
from geolocations.models import Geolocation

def generate_custom_code():
    date_part = now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"CTRL-{date_part}-{random_part}"

def generate_security_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

class Controller(models.Model):
    PHASE_CHOICES_VEGETABLE = [
        (1, 'Inicial'),
        (2, 'Vegetativa'),
        (3, 'Floração'),
        (4, 'Frutificação'),
        (5, 'Maturação'),
    ]

    name = models.CharField(max_length=60)

    device = models.CharField(max_length=60)

    security_code = models.CharField(
        max_length=40,
        unique=True,
        editable=False,
        default=generate_security_code
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    phase_vegetable = models.PositiveSmallIntegerField(
        choices=PHASE_CHOICES_VEGETABLE,
        help_text="Fase do cultivo no momento da irrigação"
    )

    status = models.BooleanField(default=False)

    active = models.BooleanField(default=False)

    last_irrigation = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    culturevegetable = models.ForeignKey(
        CultureVegetable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    geolocation = models.ForeignKey(
        Geolocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name}"

class IrrigationController(models.Model):
    PHASE_CHOICES_VEGETABLE = [
        (1, 'Inicial'),
        (2, 'Vegetativa'),
        (3, 'Floração'),
        (4, 'Frutificação'),
        (5, 'Maturação'),
    ]

    date = models.DateField(auto_now_add=True)
    
    time = models.TimeField(auto_now_add=True)

    total_liters = models.FloatField(
        help_text="Total de litros de água utilizados na irrigação"
    )

    valves_used = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Quantidade de válvulas utilizadas na irrigação do dia"
    )
    
    plants_per_valve = models.PositiveIntegerField(
        help_text="Quantidade de plantas/vegetais irrigados por válvula"
    )

    irrigation_radius = models.FloatField(
        help_text="Raio de cobertura da irrigação em metros"
    )

    phase_vegetable = models.PositiveSmallIntegerField(
        choices=PHASE_CHOICES_VEGETABLE,
        help_text="Fase do cultivo no momento da irrigação"
    )

    controller = models.ForeignKey(
        Controller,
        on_delete=models.SET_NULL,
        related_name='irrigations', 
        null=True
    )
    
    culturevegetable = models.ForeignKey(
        CultureVegetable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    geolocation = models.ForeignKey(
        Geolocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Irrigação em {self.date} {self.time} - {self.controller.name}"

class ValveController(models.Model):
    plants_number = models.PositiveIntegerField(
        help_text="Quantidade de plantas/vegetais irrigados por válvula"
    )

    irrigation_radius = models.FloatField(
        help_text="Raio de cobertura da irrigação em metros"
    )

    last_irrigation = models.DateField(null=True, blank=True)

    status = models.BooleanField(default=False)
    
    active = models.BooleanField(default=False)
    
    controller = models.ForeignKey(
        Controller,
        on_delete=models.CASCADE,
        related_name='valves'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora de criação da válvula"
    )

    def __str__(self):
        return f"Válvula - {self.controller.name} | {self.plants_number} plantas | {self.created_at.strftime('%d/%m/%Y %H:%M')}"
