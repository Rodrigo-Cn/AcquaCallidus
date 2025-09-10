from django.utils import timezone
from pytz import timezone as pytzTimezone
from irrigationvolumes.models import IrrigationVolume
from culturesvegetables.models import CultureVegetable
from meteorologicaldatas.models import MeteorologicalData
from logs.models import Log
from irrigationvolumes.services import calculateReferenceEvapotranspiration

def getOrCreateIrrigationVolume(geolocationId: int, cultureId: int):
    today = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo")).date()
    todayWithHour = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))

    try:
        irrigationVolume = IrrigationVolume.objects.get(
            culturevegetable_id=cultureId,
            meteorologicaldata__geolocation_id=geolocationId,
            date=today
        )
        return {"success": True, "irrigationVolume": irrigationVolume, "created": False}

    except IrrigationVolume.DoesNotExist:
        calculateEtoResult = calculateReferenceEvapotranspiration(geolocationId)

        if not calculateEtoResult.get("success", False):
            return {"success": False, "error": calculateEtoResult}

        eto = calculateEtoResult["dataEto"]

        try:
            cultureVegetable = CultureVegetable.objects.get(pk=cultureId)
        except CultureVegetable.DoesNotExist:
            Log.objects.create(
                reference="get_irrigationvolume_service",
                exception={"error": "Cultura não encontrada"},
                created_at=todayWithHour
            )
            return {"success": False, "error": "Cultura não encontrada"}

        try:
            meteorologicalData = MeteorologicalData.objects.get(
                date=today, geolocation_id=geolocationId
            )
        except MeteorologicalData.DoesNotExist:
            Log.objects.create(
                reference="get_irrigationvolume_service",
                exception={"error": "Dados meteorológicos não encontrados"},
                created_at=todayWithHour
            )
            return {"success": False, "error": "Dados meteorológicos não encontrados"}

        try:
            irrigationVolume = IrrigationVolume.objects.create(
                phase_initial=eto * cultureVegetable.phase_initial_kc,
                phase_vegetative=eto * cultureVegetable.phase_vegetative_kc,
                phase_flowering=eto * cultureVegetable.phase_flowering_kc,
                phase_fruiting=eto * cultureVegetable.phase_fruiting_kc,
                phase_maturation=eto * cultureVegetable.phase_maturation_kc,
                culturevegetable=cultureVegetable,
                meteorologicaldata=meteorologicalData,
                date=today,
            )
            return {"success": True, "irrigationVolume": irrigationVolume, "created": True}

        except Exception as e:
            Log.objects.create(
                reference="get_irrigationvolume_service",
                exception={"error": str(e)},
                created_at=todayWithHour
            )
            return {"success": False, "error": "Erro ao criar volumes de irrigação"}
