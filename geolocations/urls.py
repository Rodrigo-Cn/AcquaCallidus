from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='geolocation_list'),
    path('create/', views.create, name='create_geolocation'),
    path('<int:id>/delete/', views.delete, name='delete_geolocation'),
    path('<int:id>/', views.edit, name='get_geolocation'),
    path('<int:id>/update/', views.update, name='update_geolocation'), 
]
