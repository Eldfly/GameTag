from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewThreadForm, ReplyPostForm
from .models import Thread, Forum, Post
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count



# Create your views here.

def forum_threads(request, forum_id):

    #view the threads for the specific forum
    try:
        forum  = get_object_or_404(Forum, id=forum_id)
    except Forum.DoesNotExist:
        raise Http404

    threads = forum.threads.order_by('-last_activity').annotate(replies=Count('posts') - 1)
    return render(request, 'forums/thread.html', {'forum': forum, 'threads': threads})

@login_required
def new_thread(request, forum_id):

    try:
        forum  = get_object_or_404(Forum, id=forum_id)

    except Forum.DoesNotExist:
        raise Http404

    if request.method=='POST':

            form = NewThreadForm(request.POST)

            if form.is_valid():

                thread = form.save(commit=False)
                thread.forum = forum
                thread.creator = request.user
                thread.save()

                post = Post.objects.create(
                    content = form.cleaned_data.get('content'),
                    thread = thread,
                    creator = request.user
                )

                return redirect('forum_threads', forum_id=forum_id)

    else:
        form = NewThreadForm()

    return render(request, 'forums/new_thread.html', {'forum': forum, 'form': form})

@login_required
def thread_posts(request, forum_id, thread_id):

    thread = get_object_or_404(Thread, forum=forum_id, id=thread_id)
    thread.views += 1
    thread.save()

    return render(request, 'forums/thread_posts.html',  {'thread': thread})

@login_required
def reply_thread(request, forum_id, thread_id):

    try:
        thread  = get_object_or_404(Thread, id=thread_id)

    except Forum.DoesNotExist:
        raise Http404

    if request.method=='POST':

            form = ReplyPostForm(request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.thread = thread
                post.creator = request.user
                post.save()
                return redirect('thread_posts', forum_id=forum_id, thread_id=thread_id)

    else:
        form = ReplyPostForm()

    return render(request, 'forums/reply_thread.html', {'thread': thread, 'form': form})
