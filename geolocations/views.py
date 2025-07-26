from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from pytz import timezone as pytzTimezone
from django.utils import timezone
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

@require_POST
@login_required(login_url='/auth/login/')
def create(request):
    todayWithHour = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))

    try:
        city = request.POST.get('city')
        state = request.POST.get('state')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if not all([city, state, latitude, longitude]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        Geolocation.objects.create(
            city=city,
            state=state,
            latitude=latitude,
            longitude=longitude
        )

        messages.success(request, "Geolocalização cadastrada com sucesso!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    except Exception as e:
        Log.objects.create(
            reference="create_geolocation_controller",
            exception={"error": str(e)},
            created_at=todayWithHour
        )
        messages.error(request, "Ocorreu um erro ao salvar a geolocalização.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

