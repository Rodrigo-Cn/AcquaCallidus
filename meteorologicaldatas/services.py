from django.utils import timezone
import requests
from django.db import transaction
from geolocations.models import Geolocation
from meteorologicaldatas.models import MeteorologicalData
from logs.models import Log

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def saveTodayWeather(geolocationId):
    try:
        geolocation = Geolocation.objects.get(pk=geolocationId)
    except Geolocation.DoesNotExist:
        now_brazil = timezone.now()
        Log.objects.create(
            reference="request_meteorologicaldata_services",
            exception={"error": "Propriedade não encontrada"},
            created_at=now_brazil
        )
        return {"message": "Propriedade não encontrada", "success": False}

    now_brazil = timezone.now()

    params = {
        "latitude": geolocation.latitude,
        "longitude": geolocation.longitude,
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "relative_humidity_2m_max,shortwave_radiation_sum,"
            "wind_speed_10m_max,surface_pressure_mean"
        ),
        "timezone": "America/Sao_Paulo"
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        Log.objects.create(
            reference="request_meteorologicaldata_services",
            exception={"error": str(e)},
            created_at=now_brazil
        )
        return {"message": "Erro na requisição da API", "success": False}

    data = response.json().get("daily", {})

    if not data:
        Log.objects.create(
            reference="request_meteorologicaldata_services",
            exception={"error": "Nenhum dado meteorológico encontrado"},
            created_at=now_brazil
        )
        return {"message": "Nenhum dado meteorológico encontrado", "success": False}

    temperature_max = data.get("temperature_2m_max", [None])[0]
    temperature_min = data.get("temperature_2m_min", [None])[0]
    relative_humidity = data.get("relative_humidity_2m_max", [None])[0]
    solar_radiation = data.get("shortwave_radiation_sum", [None])[0]
    air_speed = data.get("wind_speed_10m_max", [None])[0]
    pressure = data.get("surface_pressure_mean", [None])[0]

    if all(isNoneData(value) for value in [temperature_max, temperature_min, relative_humidity, solar_radiation, air_speed, pressure]):
        Log.objects.create(
            reference="request_meteorologicaldata_services",
            exception={"error": "Todos os dados retornados são inválidos"},
            created_at=now_brazil
        )
        return {"message": "Todos os dados meteorológicos são inválidos, não foram salvos", "success": False}

    if None in [temperature_max, temperature_min, relative_humidity, solar_radiation, air_speed, pressure]:
        Log.objects.create(
            reference="request_meteorologicaldata_services",
            exception={"error": "Dados incompletos recebidos da API"},
            created_at=now_brazil
        )
        return {"message": "Dados meteorológicos incompletos, não foram salvos", "success": False}

    with transaction.atomic():
        MeteorologicalData.objects.create(
            temperature_max=temperature_max,
            temperature_min=temperature_min,
            relative_humidity=relative_humidity,
            solar_radiation=solar_radiation,
            air_speed=air_speed,
            pressure=pressure,
            geolocation=geolocation,
        )

    return {"message": "Dados meteorológicos de hoje gerados com sucesso!", "success": True}

def isNoneData(value):
    return value is None
