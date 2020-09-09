from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    #URL for showimg all forums
    #path('', views.index_view, name='index'),
    path('', views.ForumListView.as_view(), name='index'),

    #path('forums/user_forums/', views.user_forums, name='user_forums'),

    #url for creating a new forum
    path('forums/create_forum/', views.create_forum, name='create_forum'),

    #url for edit a forum
    path('forums/user_forums/<slug:slug>/edit_forum/', views.ForumUpdateView.as_view(), name='edit_forum'),

    #url for edit a forum
    path('forums/user_forums/<slug:slug>/delete_forum/', views.ForumDeleteView.as_view(), name='delete_forum'),

    #url for edit a topic
    path('forums/user_forums/<int:topic_id>/edit_topic/', views.TopicUpdateView.as_view(), name='edit_topic'),

    #url for delete a topic
    path('forums/user_forums/<int:pk>/delete_topic/', views.TopicDeleteView.as_view(), name='delete_topic'),

    #url for showing all topics in a forum
    path('forum/<slug:forum_slug>/', views.TopicListView.as_view(), name='forum_topic'),

    #url for creating a new topic in a forum
    path('forum/<slug:forum_slug>/new_topic/', views.new_topic, name='new_topic'),

    #url for showing all threads in a forum topic
    path('forum/<slug:forum_slug>/topic/<int:topic_id>/threads/', views.ThreadListView.as_view(), name='topic_threads'),

    #url for creating a new thread in a forum topic
    path('forum/<slug:forum_slug>/topic/<int:topic_id>/new_thread/', views.new_thread, name='new_thread'),

    #url for showing all posts for a thread in a specific fourm
    path('forum/<slug:forum_slug>/topic/<slug:topic_slug>/threads/<int:thread_id>', views.PostListView.as_view(), name='thread_posts'),

    #url for reply to a post in a thread
    path('forum/<slug:forum_slug>/topic/<slug:topic_slug>/threads/<int:thread_id>/reply/', views.reply_thread, name='reply_thread'),

    #url for update post
    path('forum/<slug:forum_slug>/topic/<slug:topic_slug>/threads/<int:thread_id>/posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),



]
