from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('irrigationvolumes/', include('irrigationvolumes.urls')),
    path('culturesvegetables/', include('culturesvegetables.urls')),
    path('meteorologicaldatas/', include('meteorologicaldatas.urls')),
    path('geolocations/', include('geolocations.urls')),
]
