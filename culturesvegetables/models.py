from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

emoji_validator = RegexValidator(
    regex=r'^[\U0001F300-\U0001FAFF]$',
    message="Coloque apenas 1 emoji válido."
)

class CultureVegetable(models.Model):
    name = models.CharField(max_length=255)
    emoji = models.CharField(
        max_length=2,
        validators=[emoji_validator],
        help_text="Escolha um emoji para representar a cultura.",
        blank=True,
        null=True
    )
    phase_initial_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    phase_vegetative_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    phase_flowering_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    phase_fruiting_kc = models.FloatField(validators=[MinValueValidator(0.0)])
    phase_maturation_kc = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"{self.emoji} {self.name}"
