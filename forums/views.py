from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewThreadForm, ReplyPostForm
from .models import Thread, Forum, Post
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator


class ThreadListView(ListView):
    model = Thread
    context_object_name = 'threads'
    template_name = 'forums/threads.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        kwargs['forum'] = self.forum
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.forum = get_object_or_404(Forum, id=self.kwargs.get('forum_id'))
        queryset = self.forum.threads.order_by('-last_activity').annotate(replies=Count('posts') - 1)
        return queryset

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'forums/thread_posts.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        self.thread.views += 1
        self.thread.save()
        kwargs['thread'] = self.thread
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, forum_id=self.kwargs.get('forum_id'), id=self.kwargs.get('thread_id'))
        queryset = self.thread.posts.order_by('created_at')
        return queryset


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


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('content', )
    template_name = 'forums/edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(creator=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('thread_posts', forum_id=post.thread.forum.id, thread_id=post.thread.id)
