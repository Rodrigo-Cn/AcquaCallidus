from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from logs.models import Log
from culturesvegetables.forms import CultureVegetableForm

@login_required(login_url='/auth/login/')
def list(request):
    return render(request, 'controller/list.html')

@login_required(login_url='/auth/login/')
def create(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    formCulturevegetable = CultureVegetableForm()

    return render(request, 'controller/create.html', context={
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': formCulturevegetable,
        'has_unread': hasUnread
    })

@login_required(login_url='/auth/login/')
def irrigationsControllersList(request, id):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    formCulturevegetable = CultureVegetableForm()

    return render(request, 'controller/irrigationcontroller/list.html', context={
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': formCulturevegetable,
        'has_unread': hasUnread
    })