from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView

urlpatterns = [
     path('forums/<int:forum_id>/', views.forum_threads, name='forum_threads'),
     path('forums/<int:forum_id>/new/', views.new_thread, name='new_thread'),
     path('forums/<int:forum_id>/threads/<int:thread_id>/', views.thread_posts, name='thread_posts'),


]
