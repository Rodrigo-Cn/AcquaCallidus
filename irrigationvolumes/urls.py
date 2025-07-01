from django.urls import path
from . import views

urlpatterns = [
    path('api/<int:geolocationId>/<int:cultureId>/', views.IrrigationVolumeAPI.as_view(), name='fetch_weather'),
]
