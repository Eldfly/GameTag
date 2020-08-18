from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    #url for showing all threads in a forum
    path('forums/<int:forum_id>/', views.forum_threads, name='forum_threads'),

    #url for creating a new thread in a forum
    path('forums/<int:forum_id>/new/', views.new_thread, name='new_thread'),

    #url for showing all posts for a thread in a specific fourm
    path('forums/<int:forum_id>/threads/<int:thread_id>/', views.thread_posts, name='thread_posts'),

    #url for reply to a post in a thread
    path('forums/<int:forum_id>/threads/<int:thread_id>/reply/', views.reply_thread, name='reply_thread'),


]
