from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import Truncator
from django.utils.timezone import now
from django.contrib.auth.models import User
import math
from django.utils.html import mark_safe
from markdown import markdown
from django.shortcuts import reverse

#DEFAULT VALUES IF none is set
DEFAULT_USER_ID = 1
DEFAULT_TOPIC_ID = 1
DEFAULT_CATEGORY_ID = 1


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    desc = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class Forum(models.Model):
    name = models.CharField(max_length=80, unique=True)
    desc = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forums', default=DEFAULT_USER_ID)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='forums', default=DEFAULT_CATEGORY_ID)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    def get_absolute_url(self):
        #return f'/forum/{self.slug}/'
        return reverse('forums', kwargs={'forum_slug': self.slug})

    def get_posts_count(self):
        return Post.objects.filter(thread__topic__forum=self).count()

    def get_last_post(self):
        return Post.objects.filter(thread__topic__forum=self).order_by('-created_at').first()

class Topic(models.Model):

    name = models.CharField(max_length=80)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topics')
    slug = models.SlugField(max_length=80, default="NONE")
    desc = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=now)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):

        truncated_name = Truncator(self.name).chars(30)

        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(truncated_name)
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        truncated_name = Truncator(self.name)
        return truncated_name.chars(30)

    # def get_absolute_url(self):
    #     #return f'/forum/{self.slug}/'
    #     return f'/forum/{self.forum.slug}/topic/{self.slug}/'

    def get_thread_count(self):
        return self.threads.count()

    def get_last_post(self):
        return Post.objects.filter(thread__topic=self).order_by('-created_at').first()

    def get_page_count(self):
        count = self.threads.count()
        pages = count / 4
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 4

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.threads.order_by('-created_at')[:10]


class Thread(models.Model):

    name = models.CharField(max_length=80)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='threads', default=DEFAULT_TOPIC_ID)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=now)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        truncated_name = Truncator(self.name)
        return truncated_name.chars(30)

    # def get_absolute_url(self):
    #     #return f'/forum/{self.slug}/'
    #     return f'/forum/{self.forum.slug}/topic/{self.topic.slug}/threads/{self.id}'

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 4
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 4

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]

class Post(models.Model):

    content = models.TextField()
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        truncated_content = Truncator(self.content)
        return truncated_content.chars(30)

    def get_content_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))
