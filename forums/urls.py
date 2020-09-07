from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    #URL for showimg all forums
    #path('', views.index_view, name='index'),
    path('', views.ForumListView.as_view(), name='index'),

    #url for creating a new forum
    path('forums/new_forum/', views.new_forum, name='new_forum'),

    #url for showing all topics in a forum
    path('forum/<slug:forum_slug>/', views.TopicListView.as_view(), name='forum_topic'),

    #url for creating a new topic in a forum
    path('forum/<slug:forum_slug>/new_topic/', views.new_topic, name='new_topic'),

    #url for showing all threads in a forum topic
    path('forum/<slug:forum_slug>/topic/<slug:topic_slug>/threads/', views.ThreadListView.as_view(), name='topic_threads'),

    #url for creating a new thread in a forum topic
    path('forum/<slug:forum_slug>/topic/<slug:topic_slug>/new_thread/', views.new_thread, name='new_thread'),

    #url for showing all posts for a thread in a specific fourm
    path('forum/<slug:forum_slug>/topic/<slug:topic_slug>/threads/<int:thread_id>', views.PostListView.as_view(), name='thread_posts'),

    #url for reply to a post in a thread
    path('forum/<slug:forum_slug>/topic/<slug:topic_slug>/threads/<int:thread_id>/reply/', views.reply_thread, name='reply_thread'),

    #url for update post
    path('forum/<slug:forum_slug>/topic/<slug:topic_slug>/threads/<int:thread_id>/posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),



]
