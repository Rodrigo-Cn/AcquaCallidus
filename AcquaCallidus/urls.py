from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('irrigationvolumes/', include('irrigationvolumes.urls')),
    path('culturesvegetables/', include('culturesvegetables.urls')),
    path('auth/', include('accounts.urls')),
]
