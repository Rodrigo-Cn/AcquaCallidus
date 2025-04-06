import math
from .models import MeteorologicalData
from logs.models import Log
from django.utils import timezone
from pytz import timezone as pytz_timezone
from meteorologicaldatas.services import saveTodayWeather

def getNowBrazil():
    return timezone.now().astimezone(pytz_timezone("America/Sao_Paulo"))

def calculateReferenceEvapotranspiration(geolocation_id):
    now_brazil = getNowBrazil()
    today_brazil = now_brazil.date()

    try:
        meteorological_data = MeteorologicalData.objects.get(date=today_brazil, geolocation_id=geolocation_id)
    except MeteorologicalData.DoesNotExist:
        save_today_weather_result = saveTodayWeather(geolocation_id)
        if save_today_weather_result["success"] == False:
            return save_today_weather_result
        try:
            meteorological_data = MeteorologicalData.objects.get(date=today_brazil, geolocation_id=geolocation_id)
        except MeteorologicalData.DoesNotExist:
            Log.objects.create(
                reference="request_calculatereferenceevapotranspiration_services",
                exception={"error": "Dados meteorológicos de hoje não encontrados!"},
                created_at=now_brazil
            )
            return {"message": "Dados meteorológicos de hoje não foram encontrados!", "success": False}

    if not all([
        isinstance(meteorological_data.temperature_max, (int, float)),
        isinstance(meteorological_data.temperature_min, (int, float)),
        isinstance(meteorological_data.relative_humidity, (int, float)),
        isinstance(meteorological_data.solar_radiation, (int, float)),
        isinstance(meteorological_data.air_speed, (int, float)),
        isinstance(meteorological_data.pressure, (int, float)),
    ]):
        Log.objects.create(
            reference="request_calculatereferenceevapotranspiration_services",
            exception={"error": "Alguns dos atributos de dados meteorológicos são inválidos"},
            created_at=now_brazil
        )
        return {"message": "Alguns dos atributos de dados meteorológicos são inválidos", "success": False}

    temp_max = meteorological_data.temperature_max
    temp_min = meteorological_data.temperature_min
    temp_media = (temp_max + temp_min) / 2
    umidade_relativa = meteorological_data.relative_humidity
    rad_solar = meteorological_data.solar_radiation
    air_speed = meteorological_data.air_speed
    pressao = meteorological_data.pressure

    es_max = 0.6108 * math.exp((17.27 * temp_max) / (temp_max + 237.3))
    es_min = 0.6108 * math.exp((17.27 * temp_min) / (temp_min + 237.3))
    es = (es_max + es_min) / 2
    ea = es * (umidade_relativa / 100)
    deficit_vapor = es - ea
    delta = (4098 * es) / ((temp_media + 237.3) ** 2)
    gamma = 0.665 * 0.001 * pressao
    Rn = rad_solar * 0.77

    eto_result = (0.408 * delta * Rn + gamma * (900 / (temp_media + 273)) * air_speed * deficit_vapor) / \
          (delta + gamma * (1 + 0.34 * air_speed))

    return {"data_eto": eto_result, "success": True}
