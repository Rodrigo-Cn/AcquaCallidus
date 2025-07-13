from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from culturesvegetables.forms import CultureVegetableForm
from logs.models import Log

@login_required(login_url='/auth/login/') 
def listForGeolocation(request):
    logs = Log.objects.order_by('-created_at')[:10]
    form_culture_vegetable = CultureVegetableForm()

    return render(request, 'meteorologicaldata/listforgeolocation.html', context={
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': form_culture_vegetable  
    })

@login_required(login_url='/auth/login/') 
def listForDate(request):
    logs = Log.objects.order_by('-created_at')[:10]
    form_culture_vegetable = CultureVegetableForm()

    return render(request, 'meteorologicaldata/listfordate.html', context={
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': form_culture_vegetable
    })
