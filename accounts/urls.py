from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('image/profile/', views.uploadProfileImage, name='upload_profile_image'),
    path('update/', views.updateUser, name='update_user'),
]
