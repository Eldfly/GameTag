from django.contrib import admin
from .models import Forum, Post, Thread, Topic, Category

# Register your models here.
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Category)
