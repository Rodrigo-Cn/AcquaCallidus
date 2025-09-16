from django.urls import path
from . import views

urlpatterns = [
    path('cultures/', views.listForCulture, name='irrigationvolume_list_cultures'),
    path('dates/', views.listForDate, name='irrigationvolume_list_date'),
    path('store/<int:geolocationId>/<int:cultureId>/', views.storeIrrigationVolume, name='store_irrigationvolume'),
    path('delete/<int:irrigationVolumeId>/', views.delete, name='delete_irrigationvolume'),
]