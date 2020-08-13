from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def register(request):

    print('?')
    if request.method == 'POST':
        print('!')
        form = UserCreationForm(request.POST)

        if form.is_valid():
            print('form is valid')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
        print('not ok')
    return render(request, 'registration/register.html', {'form': form})

def home_profile(request):

    return render(request, 'users/home.html')
