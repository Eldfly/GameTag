from django import forms
from .models import Thread, Post

class NewThreadForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Thread
        fields = ['name', 'content']


class ReplyPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['content', ]
