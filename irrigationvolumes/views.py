from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from meteorologicaldatas.services import fetch_and_save_weather

@csrf_exempt
def fetch_weather_view(request, geolocation_id):
    
    if request.method == "GET":
        result = fetch_and_save_weather(geolocation_id)
        return JsonResponse(result)
    
    return JsonResponse({"message": "Método não permitido"}, status=405)
