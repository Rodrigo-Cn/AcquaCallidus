from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='controllers_list'),
    path('create/', views.create, name='controllers_create'),
    path('irrigationscontrollers/<int:id>/', views.irrigationsControllersList, name='irrigationscontrollers_list'),
    path('store/', views.createController, name='controllers_store'),
    path('<int:id>/', views.edit, name='get_controller'),
]