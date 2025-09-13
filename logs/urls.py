from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='log_list'),
    path('viewed/', views.markLogsViewed, name='mark_logs_viewed'),
    path('<int:id>/', views.getLogException, name='get_log_exception'),
    path('<int:id>/get/', views.listOne, name='get_log'),
]
