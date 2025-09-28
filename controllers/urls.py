from django.urls import path
from . import views

urlpatterns = [
    path('', views.listController, name='controllers_list'),
    path('irrigationscontroller/<int:id>/', views.irrigationsForValveList, name='irrigationscontrollers_list'),
    path('irrigationsforcontroller/<int:id>/', views.irrigationsControllersList, name='irrigationsforcontrollers_list'),
    path('irrigationscontroller/<int:id>/delete/', views.deleteIrrigationController, name='irrigationscontrollers_delete'),
    path('store/', views.storeController, name='controllers_store'),
    path('<int:id>/update/', views.update, name='get_controller'),
    path('<int:id>/delete/', views.delete, name='update_culture'), 
    path('<int:id>/', views.edit, name='get_controller'),
    path("api/connect/", views.ControllerConnect.as_view(), name="controller_api_post_on"),
    path("api/valve/on/", views.ControllerOnAPI.as_view(), name="controller_api_post_on"),
    path("api/valve/off/", views.ControllerOffAPI.as_view(), name="controller_api_post_off"),
    path("api/update/vegetablephase/", views.ControllerUpdatePhase.as_view(), name="controller_api_update_phase"),
]