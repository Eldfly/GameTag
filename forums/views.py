from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewThreadForm, ReplyPostForm, NewTopicForm, CreateForumForm
from .models import Thread, Forum, Post, Topic
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.generic import UpdateView, ListView, DeleteView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse_lazy
from .filters import ForumFilter, TopicFilter, ThreadFilter


class ForumListView(ListView):

    model = Forum
    context_object_name = 'forums'
    template_name = 'index.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        forums = Forum.objects.filter(published=True).order_by('name')
        context = super().get_context_data(**kwargs)
        #adding the search box to the context
        context['searchForum'] = ForumFilter(self.request.GET, queryset=forums)
        return context

    def get_queryset(self):
        queryset = Forum.objects.filter(published=True).order_by('name')
        filter = ForumFilter(self.request.GET, queryset=queryset)
        return filter.qs


class TopicListView(ListView):

    model = Topic
    context_object_name = 'topics'
    template_name = 'forums/topics.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        kwargs['forum'] = self.forum
        topic = Topic.objects.filter(forum=self.forum.id)
        context = super().get_context_data(**kwargs)
        #adding the search box to the context
        context['searchTopic'] = TopicFilter(self.request.GET, queryset=topic)
        return context

    def get_queryset(self):
        self.forum = get_object_or_404(Forum, slug=self.kwargs.get('forum_slug'))
        queryset = self.forum.topics.order_by('-last_activity')
        filter = TopicFilter(self.request.GET, queryset=queryset)
        return filter.qs


class ThreadListView(ListView):

    model = Thread
    context_object_name = 'threads'
    template_name = 'forums/threads.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        kwargs['topic'] = self.topic
        thread = Thread.objects.filter(topic=self.topic.id)
        context = super().get_context_data(**kwargs)
        #adding the search box to the context
        context['searchThread'] = ThreadFilter(self.request.GET, queryset=thread)
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, id=self.kwargs.get('topic_id'))
        queryset = self.topic.threads.order_by('-last_activity').annotate(replies=Count('posts') - 1)
        filter = ThreadFilter(self.request.GET, queryset=queryset)
        return filter.qs

@method_decorator(login_required, name='dispatch')
class ThreadDeleteView(DeleteView):
    model = Thread

    def get_success_url(self):
        return reverse_lazy('topic_threads', kwargs={'forum_slug': self.kwargs['forum_slug'], 'topic_id': self.kwargs['topic_id']})


class PostListView(ListView):

    model = Post
    context_object_name = 'posts'
    template_name = 'forums/thread_posts.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):

        session_key = f'viewed_thread_{self.thread.id}'
        if not self.request.session.get(session_key, False):
            self.thread.views += 1
            self.thread.save()
            self.request.session[session_key] = True

        kwargs['thread'] = self.thread
        return super().get_context_data(**kwargs)

    def get_queryset(self):

        self.thread = get_object_or_404(Thread, id=self.kwargs.get('thread_id'))
        queryset = self.thread.posts.order_by('created_at')[1:]
        return queryset


# @login_required
# def user_forums(request):
#
#     #view the forums on the homepage for the logged in user
#     forums = Forum.objects.filter(owner=request.user.id).order_by('name')
#
#     context = {
#
#         'forums': forums,
#     }
#
#     return render(request, 'forums/user_forums.html', context)


def create_forum(request):

    if request.method=='POST':
            form = CreateForumForm(request.POST)

            if form.is_valid():

                forum = form.save(commit=False)
                forum.owner = request.user
                forum.save()

                return redirect('profile')

    else:
        form = CreateForumForm()

    return render(request, 'forums/create_forum.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ForumUpdateView(UpdateView):

    model = Forum
    fields = ('category', 'desc', 'published' )
    template_name = 'forums/edit_forum.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'forum'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #get the id from the slug
        forum_id = Forum.objects.filter(slug=self.kwargs.get('slug')).values_list('id', flat=True)[0]

        context['topics'] = Topic.objects.filter(forum=forum_id)
        topic = Topic.objects.filter(forum=10)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user.id)

    def form_valid(self, form):
        forum = form.save(commit=False)
        forum.updated_by = self.request.user
        forum.updated_at = timezone.now()
        forum.save()
        return redirect('profile')

@method_decorator(login_required, name='dispatch')
class ForumDeleteView(DeleteView):
    model = Forum
    success_url = reverse_lazy('profile')


@method_decorator(login_required, name='dispatch')
class TopicUpdateView(UpdateView):

    model = Topic
    fields = ('desc',)
    template_name = 'forums/edit_topic.html'
    pk_url_kwarg = 'topic_id'
    context_object_name = 'topic'

    def get_queryset(self):
        queryset = super().get_queryset()
        topic_id = self.kwargs.get('topic_id')
        return queryset.filter(id=topic_id)

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.updated_by = self.request.user
        topic.updated_at = timezone.now()
        topic.save()
        return redirect('edit_forum', slug=self.get_object().forum.slug)

@method_decorator(login_required, name='dispatch')
class TopicDeleteView(DeleteView):
    model = Topic

    def get_success_url(self):

      forum_slug = self.get_object().forum.slug
      return reverse_lazy('edit_forum', kwargs={'slug': forum_slug })


@login_required
def new_topic(request, forum_slug):

    try:
        forum  = get_object_or_404(Forum, slug=forum_slug)

    except Forum.DoesNotExist:
        raise Http404

    if request.method=='POST':

            form = NewTopicForm(request.POST)

            if form.is_valid():

                forum_id = forum.id
                topic_name = form.cleaned_data['name']

                if not Topic.objects.filter(forum=forum_id, name=topic_name).exists():
                    topic = form.save(commit=False)
                    topic.forum = forum
                    topic.creator = request.user
                    topic.save()
                else:
                    messages.error(request, 'This topic already exists in this')

                return redirect('edit_forum', slug=forum_slug)

    else:
        form = NewTopicForm()

    return render(request, 'forums/new_topic.html', {'forum': forum, 'form': form})


@login_required
def new_thread(request, forum_slug, topic_id):
    print(topic_id)
    try:
        topic  = get_object_or_404(Topic, id=topic_id)

    except Forum.DoesNotExist:
        raise Http404

    if request.method=='POST':

            form = NewThreadForm(request.POST)

            if form.is_valid():

                thread = form.save(commit=False)
                thread.topic = topic
                thread.creator = request.user
                thread.save()

                post = Post.objects.create(
                    content = form.cleaned_data.get('content'),
                    thread = thread,
                    creator = request.user
                )

                return redirect('topic_threads', forum_slug=forum_slug, topic_id=topic_id)

    else:
        form = NewThreadForm()

    return render(request, 'forums/new_thread.html', {'topic': topic, 'form': form})


@login_required
def reply_thread(request, forum_slug, topic_id, thread_id):

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

                thread.last_activity = timezone.now()
                thread.save()

                thread_url = reverse('thread_posts', kwargs={'forum_slug': forum_slug, 'topic_id': topic_id, 'thread_id': thread_id})
                thread_post_url = '{url}?page={page}#{id}'.format(
                    url=thread_url,
                    id=post.id,
                    page=thread.get_page_count()
                )

                return redirect(thread_post_url)
                #return redirect('thread_posts', forum_id=forum_id, thread_id=thread_id)

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
        return redirect('thread_posts', forum_slug=post.thread.topic.forum.slug, topic_id=post.thread.topic.id, thread_id=post.thread.id)

@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):

        return reverse_lazy('thread_posts', kwargs={'forum_slug': self.kwargs['forum_slug'], 'topic_id': self.kwargs['topic_id'], 'thread_id': self.kwargs['thread_id']})
