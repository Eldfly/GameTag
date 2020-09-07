from django.shortcuts import render
from forums.models import Forum

# def index_view(request):
#
#     #view the forums on the homepage for the logged in user
#     forums = Forum.objects.all()
#     context = {
#         'forums': forums
#     }
#
#     return render(request, 'index.html', context)
