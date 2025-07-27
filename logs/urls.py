from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='log_list'),
    path('viewed/', views.markLogsViewed, name='mark_logs_viewed'),
]
