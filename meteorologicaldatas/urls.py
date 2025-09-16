from django.urls import path
from . import views

urlpatterns = [
    path('geolocations/', views.listForGeolocation, name='meteorologicaldata_list_geolocation'),
    path('dates/', views.listForDate, name='meteorologicaldata_list_date'),
    path('store/<int:geolocationId>/', views.storeForGeolocation, name='meteorologicaldata_store'),
    path('delete/<int:meteorologicalDataId>/', views.deleteForGeolocation, name='meteorologicaldata_delete'),
]
