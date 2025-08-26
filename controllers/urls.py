from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='controllers_list'),
    path('irrigationscontrollers/<int:id>/', views.irrigationsControllersList, name='irrigationscontrollers_list'),
]