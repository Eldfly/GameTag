from django.urls import path
from . import views

urlpatterns = [
    path('user_licence_agreement/', views.license_view, name='licence'),
]
