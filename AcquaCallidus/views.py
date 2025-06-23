from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/auth/login/') 
def home(request):
    return render(request, 'pages/home.html')
