from django.contrib.auth.decorators import login_required
from django.forms.widgets import FileInput
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from forums.models import Forum


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            messages.success(request, f'Your account has been created for {username}. You can now login')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):

    if request.method == 'POST':
        #u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        #u_form.is_valid() and
        #u_form.save()
        if p_form.is_valid:

            p_form.save()
            messages.success(request, f'You have updated your information')
            return redirect('profile')

    else:
        #u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    forums = Forum.objects.filter(owner=request.user)

    context = {
        #'u_form': u_form,
        'p_form': p_form,
        'forums': forums,

    }
    return render(request, 'users/profile.html', context)

def license_view(request):
    return render(request, 'users/user_agreement.html')
