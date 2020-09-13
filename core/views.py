from django.shortcuts import render

def license_view(request):

    return render(request, 'user_agreement.html')
