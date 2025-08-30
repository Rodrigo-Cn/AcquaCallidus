from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('irrigationvolumes/', include('irrigationvolumes.urls')),
    path('culturesvegetables/', include('culturesvegetables.urls')),
    path('meteorologicaldatas/', include('meteorologicaldatas.urls')),
    path('controllers/', include('controllers.urls')),
    path('geolocations/', include('geolocations.urls')),
    path('logs/', include('logs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)