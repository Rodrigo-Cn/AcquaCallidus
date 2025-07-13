from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Geolocation
from logs.models import Log
from culturesvegetables.forms import CultureVegetableForm

def list(request):
    geolocations = Geolocation.objects.all()
    logs = Log.objects.order_by('-created_at')[:10]
    paginator = Paginator(geolocations, 10)
    form_culture_vegetable = CultureVegetableForm()
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'geolocation/list.html', context={
        "page_obj": page_obj,
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': form_culture_vegetable
    })
