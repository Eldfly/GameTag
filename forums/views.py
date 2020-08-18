from django.shortcuts import render, redirect, get_object_or_404
from .forms import newThreadForm
from .models import Thread, Forum, Post
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def forum_threads(request, forum_id):

    #view the threads for the specific forum
    try:
        forum  = get_object_or_404(Forum, id=forum_id)
    except Forum.DoesNotExist:
        raise Http404
    return render(request, 'forums/thread.html', {'forum': forum})

@login_required
def new_thread(request, forum_id):

    try:
        forum  = get_object_or_404(Forum, id=forum_id)

    except Forum.DoesNotExist:
        raise Http404

    if request.method=='POST':

            form = newThreadForm(request.POST)

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

                return redirect('home')

    else:
        form = newThreadForm()

    return render(request, 'forums/new_thread.html', {'forum': forum, 'form': form})

@login_required
def thread_posts(request, forum_id, thread_id):


    thread = get_object_or_404(Thread, forum=forum_id, id=thread_id)

    #posts = Post.objects.filter(thread=1)

    # thread3 = Thread.objects.get(id=3)
    #
    # print(thread3)

    # threads = Thread.objects.filter(forum=2, posts=1)
    # for thread in threads:
    #     print(thread.name)
    #
    # print(threads)

    #print(thread.forum.id)
    posts = Post.objects.all()
    for post in posts:
        print(post.content, post.thread.id, post.thread.forum)

    # threads = Thread.objects.all()
    # for thready in threads:
    #     print(thready.content, thready.id, thready.forum)




    return render(request, 'forums/thread_posts.html',  {'thread': thread})
