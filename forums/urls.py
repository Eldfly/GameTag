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

    #url for update post
    path('forums/<int:forum_id>/threads/<int:thread_id>/posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),

 # url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
 #        views.PostUpdateView.as_view(), name='edit_post'),

]
