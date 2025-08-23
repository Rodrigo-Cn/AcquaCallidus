from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='controllers_list'),
]