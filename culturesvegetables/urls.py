from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='culturevegetable_list'),
    path('create/', views.store, name='culturevegetable_create'),
    path('<int:id>/delete/', views.delete, name='delete_culture'),
    path('<int:id>/', views.edit, name='get_culture'),
    path('<int:id>/update/', views.update, name='update_culture'), 
]
