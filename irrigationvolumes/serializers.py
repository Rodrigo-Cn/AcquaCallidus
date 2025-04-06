from rest_framework.serializers import ModelSerializer
from .models import IrrigationVolume

class IrrigationVolumeSerializer(ModelSerializer):
    class Meta:
        model = IrrigationVolume
        fields = '__all__'