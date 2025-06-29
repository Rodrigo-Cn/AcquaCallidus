from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
from logs.models import Log
from irrigationvolumes.models import IrrigationVolume
from meteorologicaldatas.models import MeteorologicalData
from culturesvegetables.models import CultureVegetable
from django.db.models import Count
from collections import OrderedDict
from datetime import timedelta

portuguese_months = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

@login_required(login_url='/auth/login/') 
def home(request):
    logs = Log.objects.order_by('-created_at')[:10]
    today = now()

    irrigationCount = IrrigationVolume.objects.count()
    meteorologicalCount = MeteorologicalData.objects.count()
    cultureCount = CultureVegetable.objects.count()

    months = OrderedDict()
    for i in range(3, -1, -1):
        month_date = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        label = portuguese_months[month_date.month]
        months[label] = 0

    from_date = today - timedelta(days=120)
    logs_per_month = (
        Log.objects
        .filter(created_at__gte=from_date)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    for item in logs_per_month:
        label = portuguese_months[item['month'].month]
        if label in months:
            months[label] = item['count']

    months_irrigation = OrderedDict()
    for i in range(6, -1, -1): 
        month_date = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        label = portuguese_months[month_date.month]
        months_irrigation[label] = 0

    from_date_irrigation = today - timedelta(days=210)
    irrigation_per_month = (
        IrrigationVolume.objects
        .filter(date__gte=from_date_irrigation)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    for item in irrigation_per_month:
        label = portuguese_months[item['month'].month]
        if label in months_irrigation:
            months_irrigation[label] = item['count']

    return render(request, 'pages/home.html', context={
        'user': request.user,
        'logs': logs,
        'chart_labels': list(months.keys()),
        'chart_data': list(months.values()),
        'chart_labels_irrigation': list(months_irrigation.keys()),
        'chart_data_irrigation': list(months_irrigation.values()),
        'irrigation_count' : irrigationCount,
        'meteorological_count' : meteorologicalCount,
        'culture_count' : cultureCount
    })
