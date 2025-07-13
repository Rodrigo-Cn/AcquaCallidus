from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from culturesvegetables.forms import CultureVegetableForm
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from .models import MeteorologicalData
from datetime import date
from logs.models import Log

@login_required(login_url='/auth/login/') 
def listForGeolocation(request):
    logs = Log.objects.order_by('-created_at')[:10]
    geolocation_id = request.GET.get('geolocation_id', '')
    form_culture_vegetable = CultureVegetableForm()
    has_today_data = False
    meteorologicaldatas = MeteorologicalData.objects.all()

    if geolocation_id:
        meteorologicaldatas = meteorologicaldatas.filter(geolocation_id=geolocation_id)
        has_today_data = MeteorologicalData.objects.filter(
            geolocation_id=geolocation_id,
            date=date.today()
        ).exists()

    meteorologicaldatas = meteorologicaldatas.order_by('-date')
    paginator = Paginator(meteorologicaldatas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'meteorologicaldata/listforgeolocation.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': page_obj,
        'geolocation_id': geolocation_id,
        'form_culture_vegetable': form_culture_vegetable,
        'today': date.today(),
        'has_today_data': has_today_data
    })

@login_required(login_url='/auth/login/')
def listForDate(request):
    logs = Log.objects.order_by('-created_at')[:10]
    date_query = request.GET.get('date', '')
    form_culture_vegetable = CultureVegetableForm()

    meteorologicaldatas = MeteorologicalData.objects.all()

    if date_query:
        parsed_date = parse_date(date_query)
        if parsed_date:
            meteorologicaldatas = meteorologicaldatas.filter(date=parsed_date)

    meteorologicaldatas = meteorologicaldatas.order_by('-date')
    paginator = Paginator(meteorologicaldatas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'meteorologicaldata/listfordate.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': page_obj,
        'date_query': date_query,
        'form_culture_vegetable': form_culture_vegetable,
        'today': date.today()
    })