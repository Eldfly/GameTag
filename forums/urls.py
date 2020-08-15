from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     path('forums/<int:forum_id>/', views.forum_threads, name='forum_threads'),

]
