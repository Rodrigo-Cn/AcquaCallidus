from django.urls import path
from . import views

urlpatterns = [
    path('fetchweather/<int:geolocation_id>/', views.fetch_weather_view, name='fetch_weather'),
]
