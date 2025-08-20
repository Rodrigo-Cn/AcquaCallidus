from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from culturesvegetables.forms import CultureVegetableForm
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.urls import reverse
from .models import MeteorologicalData
from .services import saveTodayWeather
from django.contrib import messages
from django.utils.timezone import now
from datetime import date
from geolocations.models import Geolocation
from logs.models import Log
from .models import MeteorologicalData


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
        'has_today_data': hasTodayData
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
def createForGeolocation(request, geolocationId):
    if not geolocationId:
        messages.error(request, "Geolocalização não selecionada!")
        return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')
    
    today = now().date()
    already_exists = MeteorologicalData.objects.filter(geolocation_id=geolocationId, date=today).exists()

    if already_exists:
        messages.warning(request, "Os dados meteorológicos de hoje já existem para essa geolocalização.")
    else:
        response = saveTodayWeather(geolocationId)
        if response.get("success"):
            messages.success(request, response.get("message", "Dados meteorológicos de hoje gerados com sucesso!"))
        else:
            messages.error(request, response.get("message", "Ocorreu um erro ao gerar os dados meteorológicos!"))

    return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')
    
@login_required(login_url='/auth/login/')
def deleteForGeolocation(request, meteorologicalDataId):
    try:
        meteorologicalData = get_object_or_404(MeteorologicalData, id=meteorologicalDataId)
        geolocationId = meteorologicalData.geolocation_id
        geolocation = meteorologicalData.geolocation.city + ' - ' + meteorologicalData.geolocation.state
        meteorologicalData.delete()
        messages.success(
            request,
            f"Dados meteorológicos de hoje para {geolocation} deletados com sucesso!"
        )
    except Exception as e:
        messages.error(request, "Ocorreu um erro ao deletar os dados meteorológicos.")

    return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')
