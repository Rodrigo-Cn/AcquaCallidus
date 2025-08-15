from rest_framework.serializers import ModelSerializer
from .models import Geolocation

class GeolocationSerializer(ModelSerializer):
    class Meta:
        model = Geolocation
        fields = '__all__'