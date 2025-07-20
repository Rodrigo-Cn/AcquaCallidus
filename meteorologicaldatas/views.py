from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from culturesvegetables.forms import CultureVegetableForm
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.urls import reverse
from .models import MeteorologicalData
from .services import saveTodayWeather
from django.contrib import messages
from datetime import date
from geolocations.models import Geolocation
from logs.models import Log


@login_required(login_url='/auth/login/')
def listForGeolocation(request):
    logs = Log.objects.order_by('-created_at')[:10]
    geolocationList = Geolocation.objects.all()
    geolocationId = request.GET.get('geolocation_id', '')  # mantém nome da chave original
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
    logs = Log.objects.order_by('-created_at')[:10]
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
        'today': date.today()
    })

@login_required(login_url='/auth/login/')
def createForGeolocation(request, geolocationId):
    if geolocationId:
        response = saveTodayWeather(geolocationId)

        if response.get("success"):
            messages.success(request, response.get("message", "Dados meteorológicos de hoje gerados com sucesso!"))
        else:
            messages.error(request, response.get("message", "Ocorreu um erro ao gerar os dados meteorológicos!"))
        
        return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')
    else:
        messages.error(request, "Geolocalização não selecionada!")
        return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')
    
@login_required(login_url='/auth/login/')
def deleteForGeolocation(request, geolocationId):
    if geolocationId:
        response = saveTodayWeather(geolocationId)

        if response.get("success"):
            messages.success(request, response.get("message", "Dados meteorológicos de hoje gerados com sucesso!"))
        else:
            messages.error(request, response.get("message", "Ocorreu um erro ao gerar os dados meteorológicos!"))
        
        return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')
    else:
        messages.error(request, "Geolocalização não selecionada!")
        return redirect(f'{reverse("meteorologicaldata_list_geolocation")}?geolocation_id={geolocationId}')