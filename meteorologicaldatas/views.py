from datetime import date
from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from culturesvegetables.forms import CultureVegetableForm
from geolocations.models import Geolocation
from logs.models import Log
from logs.services import logError
from .models import MeteorologicalData
from .services import saveTodayWeather
from django.shortcuts import redirect, get_object_or_404

@login_required(login_url='/auth/login/')
def listForGeolocation(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    geolocationList = Geolocation.objects.all()
    geolocationId = request.GET.get('geolocation_id', '')
    formCultureVegetable = CultureVegetableForm()
    hasTodayData = False
    meteorologicalDataList = MeteorologicalData.objects.all()

    if geolocationId:
        meteorologicalDataList = meteorologicalDataList.filter(geolocation_id=geolocationId)
        hasTodayData = MeteorologicalData.objects.filter(
            geolocation_id=geolocationId,
            date=date.today()
        ).exists()

    meteorologicalDataList = meteorologicalDataList.order_by('-date')
    paginator = Paginator(meteorologicalDataList, 15)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    return render(request, 'meteorologicaldata/listforgeolocation.html', context={
        'user': request.user,
        'logs': logs,
        'geolocations': geolocationList, 
        'page_obj': pageObj,              
        'geolocation_id': geolocationId,  
        'form_culture_vegetable': formCultureVegetable,
        'today': date.today(),
        'has_today_data': hasTodayData,
        'has_unread': hasUnread
    })

@login_required(login_url='/auth/login/')
def listForDate(request):
    logs = Log.objects.order_by('-created_at') 
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    dateQuery = request.GET.get('date', '')
    formCultureVegetable = CultureVegetableForm()

    meteorologicalDataList = MeteorologicalData.objects.all()

    if dateQuery:
        parsedDate = parse_date(dateQuery)
        if parsedDate:
            meteorologicalDataList = meteorologicalDataList.filter(date=parsedDate)

    meteorologicalDataList = meteorologicalDataList.order_by('-date')
    paginator = Paginator(meteorologicalDataList, 15)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    return render(request, 'meteorologicaldata/listfordate.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': pageObj,
        'date_query': dateQuery,
        'form_culture_vegetable': formCultureVegetable,
        'today': date.today(),
        'has_unread': hasUnread
    })

@login_required(login_url='/auth/login/')
def storeForGeolocation(request, geolocationId):
    if not geolocationId:
        messages.error(request, "Propriedade não selecionada!")
        return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')

    try:
        with transaction.atomic():
            already_exists = MeteorologicalData.objects.filter(
                geolocation_id=geolocationId,
                date=now().date()
            ).exists()

            if already_exists:
                messages.warning(
                    request,
                    "Os dados meteorológicos de hoje já existem para essa propriedade."
                )
            else:
                response = saveTodayWeather(geolocationId)
                if response.get("success"):
                    messages.success(
                        request,
                        response.get("message", "Dados meteorológicos de hoje gerados com sucesso!")
                    )
                else:
                    messages.error(
                        request,
                        response.get("message", "Ocorreu um erro ao gerar os dados meteorológicos!")
                    )

    except Exception as e:
        logError("store_meteorologicaldata_view", {
            "step": "exception",
            "error": str(e),
        })
        messages.error(request, "Erro inesperado ao criar dados meteorológicos.")

    return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')


@login_required(login_url='/auth/login/')
def deleteForGeolocation(request, meteorologicalDataId):
    try:
        with transaction.atomic():
            meteorologicalData = get_object_or_404(MeteorologicalData, id=meteorologicalDataId)
            geolocationId = meteorologicalData.geolocation_id
            geolocation = f"{meteorologicalData.geolocation.city} - {meteorologicalData.geolocation.state}"
            meteorologicalData.delete()

        messages.success(
            request,
            f"Dados meteorológicos de hoje para {geolocation} deletados com sucesso!"
        )

    except Exception as e:
        logError("delete_meteorologicaldata_view", {
            "step": "exception",
            "error": str(e),
        })
        messages.error(request, "Ocorreu um erro ao deletar os dados meteorológicos.")

    return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId or ""}')