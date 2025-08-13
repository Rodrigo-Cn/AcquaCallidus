from rest_framework.serializers import ModelSerializer
from .models import CultureVegetable

class CultureVegetableSerializer(ModelSerializer):
    class Meta:
        model = CultureVegetable
        fields = '__all__'