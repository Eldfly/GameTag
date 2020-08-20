from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import Truncator
from django.utils.timezone import now
from django.contrib.auth.models import User
import math
from django.utils.html import mark_safe
from markdown import markdown


# Create your models here.
class Forum(models.Model):
    name = models.CharField(max_length=80, unique=True)
    desc = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    def get_posts_count(self):
        return Post.objects.filter(thread__forum=self).count()


    def get_last_post(self):
        return Post.objects.filter(thread__forum=self).order_by('-created_at').first()

class Thread(models.Model):

    name = models.CharField(max_length=80, unique=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='threads')
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=now)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        truncated_name = Truncator(self.name)
        return truncated_name.chars(30)

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
