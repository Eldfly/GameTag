from django.urls import path
from . import views

urlpatterns = [
    path('app/register', views.register, name='register'),
    path('user/profile/', views.home_profile, name='profile'),
]
