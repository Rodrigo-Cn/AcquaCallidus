from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='culturevegetable_list'),
    path('create/', views.create, name='culturevegetable_create'),
    path('<int:id>/', views.delete, name='delete_culture'),
]
