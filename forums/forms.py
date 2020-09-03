from django import forms
from .models import Forum, Topic, Thread, Post



class NewForumForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ['category', 'name', 'desc', 'published']

class NewTopicForm(forms.ModelForm):

    desc = forms.CharField(widget=forms.Textarea(), max_length=200)

    class Meta:
        model = Topic
        fields = ['name', 'desc']


class NewThreadForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Thread
        fields = ['name', 'content']




class ReplyPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['content', ]
