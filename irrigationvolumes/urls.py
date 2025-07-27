from django.urls import path
from . import views

urlpatterns = [
    path('api/<int:geolocationId>/<int:cultureId>/', views.IrrigationVolumeAPI.as_view(), name='fetch_weather'),
    path('cultures/', views.listForCulture, name='irrigationvolume_list_cultures'),
    path('dates/', views.listForDate, name='irrigationvolume_list_date'),
    path('create/<int:geolocationId>/<int:cultureId>/', views.createIrrigationVolume, name='create_irrigationvolume'),
]