import math
from .models import MeteorologicalData
from logs.models import Log
from django.utils import timezone
from pytz import timezone as pytzTimezone
from meteorologicaldatas.services import saveTodayWeather

def getNowBrazil():
    return timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))

def calculateReferenceEvapotranspiration(geolocationId):
    nowBrazil = getNowBrazil()
    todayBrazil = nowBrazil.date()

    try:
        meteorologicalData = MeteorologicalData.objects.get(date=todayBrazil, geolocation_id=geolocationId)
    except MeteorologicalData.DoesNotExist:
        saveTodayWeatherResult = saveTodayWeather(geolocationId)
        if not saveTodayWeatherResult["success"]:
            return saveTodayWeatherResult
        try:
            meteorologicalData = MeteorologicalData.objects.get(date=todayBrazil, geolocation_id=geolocationId)
        except MeteorologicalData.DoesNotExist:
            Log.objects.create(
                reference="request_calculateReferenceEvapotranspiration_services",
                exception={"error": "Dados meteorológicos de hoje não encontrados!"},
                createdAt=nowBrazil
            )
            return {"message": "Dados meteorológicos de hoje não foram encontrados!", "success": False}

    if not all([
        isinstance(meteorologicalData.temperature_max, (int, float)),
        isinstance(meteorologicalData.temperature_min, (int, float)),
        isinstance(meteorologicalData.relative_humidity, (int, float)),
        isinstance(meteorologicalData.solar_radiation, (int, float)),
        isinstance(meteorologicalData.air_speed, (int, float)),
        isinstance(meteorologicalData.pressure, (int, float)),
    ]):
        Log.objects.create(
            reference="request_calculateReferenceEvapotranspiration_services",
            exception={"error": "Alguns dos atributos de dados meteorológicos são inválidos"},
            createdAt=nowBrazil
        )
        return {"message": "Alguns dos atributos de dados meteorológicos são inválidos", "success": False}

    tempMax = meteorologicalData.temperature_max
    tempMin = meteorologicalData.temperature_min
    tempAvg = (tempMax + tempMin) / 2
    relativeHumidity = meteorologicalData.relative_humidity
    solarRadiation = meteorologicalData.solar_radiation
    airSpeed = meteorologicalData.air_speed
    pressure = meteorologicalData.pressure

    esMax = 0.6108 * math.exp((17.27 * tempMax) / (tempMax + 237.3))
    esMin = 0.6108 * math.exp((17.27 * tempMin) / (tempMin + 237.3))
    es = (esMax + esMin) / 2
    ea = es * (relativeHumidity / 100)
    vaporDeficit = es - ea
    delta = (4098 * es) / ((tempAvg + 237.3) ** 2)
    gamma = 0.665 * 0.001 * pressure
    rn = solarRadiation * 0.77

    etoResult = (0.408 * delta * rn + gamma * (900 / (tempAvg + 273)) * airSpeed * vaporDeficit) / \
          (delta + gamma * (1 + 0.34 * airSpeed))

    return {"dataEto": etoResult, "success": True}
