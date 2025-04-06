from django.utils import timezone
from pytz import timezone as pytz_timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import IrrigationVolume
from logs.models import Log
from culturesvegetables.models import CultureVegetable
from meteorologicaldatas.models import MeteorologicalData
from .serializers import IrrigationVolumeSerializer
from .services import calculateReferenceEvapotranspiration

class IrrigationVolumeAPI(APIView):
    def get(self, request, geolocation_id, culture_id):
        today = timezone.now().astimezone(pytz_timezone("America/Sao_Paulo")).date()

        try:
            irrigation_volume = IrrigationVolume.objects.get(
                culturevegetable_id=culture_id,
                meteorologicaldata__geolocation_id=geolocation_id,
                date=today
            )
            serializer = IrrigationVolumeSerializer(irrigation_volume)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IrrigationVolume.DoesNotExist:
            calculate_eto_result = calculateReferenceEvapotranspiration(geolocation_id)

            if not calculate_eto_result.get('success', False):
                return Response(calculate_eto_result, status=status.HTTP_400_BAD_REQUEST)

            eto = calculate_eto_result["data_eto"]
            root_area_m2 = 1

            try:
                culture_vegetable = CultureVegetable.objects.get(pk=culture_id)
            except CultureVegetable.DoesNotExist:
                Log.objects.create(
                    reference="get_irrigationvolume_controller",
                    exception={"error": "Alguns dos atributos de dados meteorológicos são inválidos"},
                    created_at=today
                )
                return Response({"message": "Cultura não encontrada", "success": False}, status=status.HTTP_404_NOT_FOUND)

            meteorological_data = MeteorologicalData.objects.get(date=today, geolocation_id=geolocation_id)

            irrigation_volume = IrrigationVolume.objects.create(
                culturevegetable=culture_vegetable,
                meteorologicaldata=meteorological_data,
                phase_germination=eto * culture_vegetable.phase_germination_kc * root_area_m2,
                phase_vegetative=eto * culture_vegetable.phase_vegetative_kc * root_area_m2,
                phase_emerging=eto * culture_vegetable.phase_emerging_kc * root_area_m2,
                phase_frying=eto * culture_vegetable.phase_frying_kc * root_area_m2,
                phase_maturation=eto * culture_vegetable.phase_maturation_kc * root_area_m2,
            )

            serializer = IrrigationVolumeSerializer(irrigation_volume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
