from django.utils import timezone
from django.shortcuts import render
from pytz import timezone as pytzTimezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import IrrigationVolume
from logs.models import Log
from culturesvegetables.models import CultureVegetable
from meteorologicaldatas.models import MeteorologicalData
from .serializers import IrrigationVolumeSerializer
from .services import calculateReferenceEvapotranspiration
from django.contrib.auth.decorators import login_required

class IrrigationVolumeAPI(APIView):
    def get(self, request, geolocationId, cultureId):
        today = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo")).date()
        todayWithHour = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))

        try:
            irrigationVolume = IrrigationVolume.objects.get(
                culturevegetable_id=cultureId,
                meteorologicaldata__geolocation_id=geolocationId,
                date=today
            )
            serializer = IrrigationVolumeSerializer(irrigationVolume)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IrrigationVolume.DoesNotExist:
            calculateEtoResult = calculateReferenceEvapotranspiration(geolocationId)

            if not calculateEtoResult.get('success', False):
                return Response(calculateEtoResult, status=status.HTTP_400_BAD_REQUEST)

            eto = calculateEtoResult["dataEto"]
            rootAreaM2 = 1

            try:
                cultureVegetable = CultureVegetable.objects.get(pk=cultureId)
            except CultureVegetable.DoesNotExist:
                Log.objects.create(
                    reference="get_irrigationvolume_controller",
                    exception={"error": "Alguns dos atributos de dados meteorológicos são inválidos"},
                    created_at=todayWithHour
                )
                return Response({"message": "Cultura não encontrada", "success": False}, status=status.HTTP_404_NOT_FOUND)

            meteorologicalData = MeteorologicalData.objects.get(date=today, geolocation_id=geolocationId)

            irrigationVolume = IrrigationVolume.objects.create(
                phase_initial=eto * cultureVegetable.phase_initial_kc * rootAreaM2,
                phase_vegetative=eto * cultureVegetable.phase_vegetative_kc * rootAreaM2,
                phase_flowering=eto * cultureVegetable.phase_flowering_kc * rootAreaM2,
                phase_fruiting=eto * cultureVegetable.phase_fruiting_kc * rootAreaM2,
                phase_maturation=eto * cultureVegetable.phase_maturation_kc * rootAreaM2,
                culturevegetable=cultureVegetable,
                meteorologicaldata=meteorologicalData,
            )

            serializer = IrrigationVolumeSerializer(irrigationVolume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@login_required(login_url='/auth/login/') 
def listForCulture(request):
    logs = Log.objects.order_by('-created_at')[:10]

    return render(request, 'irrigationvolume/listforculture.html', context={
        'user': request.user,
        'logs': logs,
    })

@login_required(login_url='/auth/login/') 
def listForDate(request):
    logs = Log.objects.order_by('-created_at')[:10]

    return render(request, 'irrigationvolume/listfordate.html', context={
        'user': request.user,
        'logs': logs,
    })
