from django.urls import path
from . import views

urlpatterns = [
    path('geolocations/', views.listForGeolocation, name='meteorologicaldata_list_geolocation'),
    path('dates/', views.listForDate, name='meteorologicaldata_list_date'),
    path('create/<int:geolocationId>/', views.createForGeolocation, name='meteorologicaldata_create'),
]
