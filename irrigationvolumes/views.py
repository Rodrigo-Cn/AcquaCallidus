from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import IrrigationVolume
from logs.models import Log
from culturesvegetables.models import CultureVegetable
from meteorologicaldatas.models import MeteorologicalData
from .serializers import IrrigationVolumeSerializer
from .services import calculateReferenceEvapotranspiration
from django.contrib.auth.decorators import login_required
from culturesvegetables.forms import CultureVegetableForm
from pytz import timezone as pytzTimezone
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date

class IrrigationVolumeAPI(APIView):
    def get(self, request, geolocationId, cultureId):
        today = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo")).date()
        todayWithHour = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))

        try:
            irrigationVolume = IrrigationVolume.objects.get(
                culturevegetable_id=cultureId,
                meteorologicaldata__geolocation_id=geolocationId,
                date=today
            )
            serializer = IrrigationVolumeSerializer(irrigationVolume)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IrrigationVolume.DoesNotExist:
            calculateEtoResult = calculateReferenceEvapotranspiration(geolocationId)

            if not calculateEtoResult.get('success', False):
                return Response(calculateEtoResult, status=status.HTTP_400_BAD_REQUEST)

            eto = calculateEtoResult["dataEto"]
            rootAreaM2 = 1

            try:
                cultureVegetable = CultureVegetable.objects.get(pk=cultureId)
            except CultureVegetable.DoesNotExist:
                Log.objects.create(
                    reference="get_irrigationvolume_controller",
                    exception={"error": "Alguns dos atributos de dados meteorológicos são inválidos"},
                    created_at=todayWithHour
                )
                return Response({"message": "Cultura não encontrada", "success": False}, status=status.HTTP_404_NOT_FOUND)

            meteorologicalData = MeteorologicalData.objects.get(date=today, geolocation_id=geolocationId)

            irrigationVolume = IrrigationVolume.objects.create(
                phase_initial=eto * cultureVegetable.phase_initial_kc * rootAreaM2,
                phase_vegetative=eto * cultureVegetable.phase_vegetative_kc * rootAreaM2,
                phase_flowering=eto * cultureVegetable.phase_flowering_kc * rootAreaM2,
                phase_fruiting=eto * cultureVegetable.phase_fruiting_kc * rootAreaM2,
                phase_maturation=eto * cultureVegetable.phase_maturation_kc * rootAreaM2,
                culturevegetable=cultureVegetable,
                meteorologicaldata=meteorologicalData,
            )

            serializer = IrrigationVolumeSerializer(irrigationVolume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@login_required(login_url='/auth/login/') 
def listForCulture(request):
    logs = Log.objects.order_by('-created_at')[:10]
    form_culture_vegetable = CultureVegetableForm()

    return render(request, 'irrigationvolume/listforculture.html', context={
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': form_culture_vegetable
    })

@login_required(login_url='/auth/login/')
def listForCulture(request):
    logs = Log.objects.order_by('-created_at')[:10]
    geolocationList = Geolocation.objects.all()
    cultureId = request.GET.get('culture_id', '')
    formCultureVegetable = CultureVegetableForm()
    hasTodayData = False
    irrigationVolumeList = IrrigationVolume.objects.all()

    if geolocationId:
        irrigationVolumeList = irrigationVolumeList.filter(culturevegetable_id=cultureId)
        hasTodayData = IrrigationVolume.objects.filter(
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

    IrrigationVolumeList = IrrigationVolume.objects.all()

    if dateQuery:
        parsedDate = parse_date(dateQuery)
        if parsedDate:
            IrrigationVolumeList = IrrigationVolumeList.filter(date=parsedDate)

    IrrigationVolumeList = IrrigationVolumeList.order_by('-date')
    paginator = Paginator(IrrigationVolumeList, 12)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    return render(request, 'irrigationvolume/listfordate.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': pageObj,
        'date_query': dateQuery,
        'form_culture_vegetable': formCultureVegetable,
        'today': date.today()
    })