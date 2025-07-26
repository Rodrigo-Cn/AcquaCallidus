from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='geolocation_list'),
    path('create/', views.create, name='create_geolocation'),
]
