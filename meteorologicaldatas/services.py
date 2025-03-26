from django.utils import timezone
import requests
from django.db import transaction
from geolocations.models import Geolocation
from meteorologicaldatas.models import MeteorologicalData
from logs.models import Log

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def is_invalid_data(value):
    return value is None

def fetch_and_save_weather(geolocation_id):
    try:
        geolocation = Geolocation.objects.get(pk=geolocation_id)
    except Geolocation.DoesNotExist:
        now_brazil = timezone.now()
        Log.objects.create(
            reference="request_meteorologicaldata_services",
            exception={"error": "Geolocalização não encontrada"},
            created_at=now_brazil
        )
        return {"message": "Geolocalização não encontrada", "success": False}

    now_brazil = timezone.now()

    params = {
        "latitude": geolocation.latitude,
        "longitude": geolocation.longitude,
        "daily": "temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,shortwave_radiation_sum,wind_speed_10m_max",
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

    if all(is_invalid_data(value) for value in [temperature_max, temperature_min, relative_humidity, solar_radiation, air_speed]):
        Log.objects.create(
            reference="request_meteorologicaldata_services",
            exception={"error": "Todos os dados retornados são inválidos"},
            created_at=now_brazil
        )
        return {"message": "Todos os dados meteorológicos são inválidos, não foram salvos", "success": False}

    if None in [temperature_max, temperature_min, relative_humidity, solar_radiation, air_speed]:
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
            geolocation=geolocation,
        )

    return {"message": "Dados meteorológicos salvos com sucesso!", "success": True}