from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import Truncator
from django.utils.timezone import now
from django.contrib.auth.models import User



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

class Thread(models.Model):

    name = models.CharField(max_length=80, unique=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='threads')
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=now)

    def __str__(self):
        truncated_name = Truncator(self.name)
        return truncated_name.chars(30)



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
