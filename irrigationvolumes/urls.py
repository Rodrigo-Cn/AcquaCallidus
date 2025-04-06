from django.urls import path
from . import views

urlpatterns = [
    path('api/<int:geolocation_id>/<int:culture_id>/', views.IrrigationVolumeAPI.as_view(), name='fetch_weather'),
    path('teste/', views.teste),
]
