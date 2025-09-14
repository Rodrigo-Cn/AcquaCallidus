from django.urls import path
from . import views

urlpatterns = [
    path('', views.listController, name='controllers_list'),
    path('irrigationscontrollers/<int:id>/', views.irrigationsControllersList, name='irrigationscontrollers_list'),
    path('store/', views.storeController, name='controllers_store'),
    path('<int:id>/update/', views.update, name='get_controller'),
    path('<int:id>/delete/', views.delete, name='update_culture'), 
    path('<int:id>/', views.edit, name='get_controller'),
    path("api/valve/on/", views.ControllerOnAPI.as_view(), name="controller_api_post_on"),
    path("api/valve/off/", views.ControllerOffAPI.as_view(), name="controller_api_post_off"),
]