from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
from logs.models import Log
from irrigationvolumes.models import IrrigationVolume
from geolocations.models import Geolocation
from culturesvegetables.models import CultureVegetable
from culturesvegetables.forms import CultureVegetableForm
from django.db.models import Count
from collections import OrderedDict
from datetime import timedelta

portugueseMonths = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

@login_required(login_url='/auth/login/') 
def home(request):
    logs = Log.objects.order_by('-created_at')[:10]
    today = now()

    form_culture_vegetable = CultureVegetableForm()
    irrigationCount = IrrigationVolume.objects.count()
    geolocationCount = Geolocation.objects.count()
    cultureCount = CultureVegetable.objects.count()

    months = OrderedDict()
    for i in range(3, -1, -1):
        monthDate = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        label = portugueseMonths[monthDate.month]
        months[label] = 0

    fromDate = today - timedelta(days=120)
    logsPerMonth = (
        Log.objects
        .filter(created_at__gte=fromDate)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    for item in logsPerMonth:
        label = portugueseMonths[item['month'].month]
        if label in months:
            months[label] = item['count']

    monthsIrrigation = OrderedDict()
    for i in range(6, -1, -1): 
        monthDate = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        label = portugueseMonths[monthDate.month]
        monthsIrrigation[label] = 0

    fromDateIrrigation = today - timedelta(days=210)
    irrigationPerMonth = (
        IrrigationVolume.objects
        .filter(date__gte=fromDateIrrigation)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    for item in irrigationPerMonth:
        label = portugueseMonths[item['month'].month]
        if label in monthsIrrigation:
            monthsIrrigation[label] = item['count']

    return render(request, 'pages/home.html', context={
        'user': request.user,
        'logs': logs,
        'chart_labels': list(months.keys()),
        'chart_data': list(months.values()),
        'chart_labels_irrigation': list(monthsIrrigation.keys()),
        'chart_data_irrigation': list(monthsIrrigation.values()),
        'irrigation_count': irrigationCount,
        'geolocation_count': geolocationCount,
        'culture_count': cultureCount,
        'form_culture_vegetable': form_culture_vegetable
    })
