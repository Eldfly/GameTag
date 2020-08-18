from django import forms
from .models import Thread

class newThreadForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Thread
        fields = ['name', 'content']
