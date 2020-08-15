from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):

    #profile_pic = forms.ImageField(widget=forms.widgets.FileInput)

    class Meta:
        model = Profile
        fields = ['profile_pic']
        widgets = {
            'profile_pic': forms.widgets.FileInput,
        }
        labels = {
            'profile_pic': 'Image'
        }
