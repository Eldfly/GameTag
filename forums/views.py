from django.shortcuts import render
#from .forms import ThreadForm
from .models import Thread, Forum, Post

# Create your views here.

def forum_threads(request, forum_id):

    #view the threads for the specific forum
    forum  = Forum.objects.get(id=forum_id)
    return render(request, 'forums/thread.html', {'forum': forum})

def create_thread(request):

    if request.method == 'POST':
        form = ThreadForm(request.POST)

        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            content = form.cleaned_data.get('content')
            messages.success(request, f'You created a new thread')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('login')
    else:
        form = ThreadForm()
    return render(request, 'users/register.html', {'form': form})

def delete_thread(request):

    if request.method == 'POST':
        form = ThreadForm(request.POST)

        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            content = form.cleaned_data.get('content')
            messages.success(request, f'Your account has been created for {username}. You can now login')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('login')
    else:
        form = ThreadForm()
    return render(request, 'users/register.html', {'form': form})
