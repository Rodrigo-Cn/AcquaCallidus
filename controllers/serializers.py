from rest_framework import serializers
from .models import Controller, ValveController


class ValveControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValveController
        fields = [
            'id',
            'plants_number',
            'irrigation_radius',
            'last_irrigation',
            'created_at'
        ]

class ControllerSerializer(serializers.ModelSerializer):
    valves = ValveControllerSerializer(many=True, read_only=True)

    class Meta:
        model = Controller
        fields = '__all__'
