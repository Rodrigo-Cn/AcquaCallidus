from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Geolocation
from logs.models import Log

def list(request):
    geolocations = Geolocation.objects.all()
    logs = Log.objects.order_by('-created_at')[:10]
    paginator = Paginator(geolocations, 10)  # 10 por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'geolocation/list.html', context={
        "page_obj": page_obj,
        'user': request.user,
        'logs': logs
    })
