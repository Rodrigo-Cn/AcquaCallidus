from datetime import date
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from pytz import timezone as pytzTimezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import IrrigationVolume
from geolocations.models import Geolocation
from logs.models import Log
from logs.services import logError
from culturesvegetables.models import CultureVegetable
from meteorologicaldatas.models import MeteorologicalData
from culturesvegetables.forms import CultureVegetableForm
from .services import calculateReferenceEvapotranspiration
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from pytz import timezone as pytzTimezone
from .models import IrrigationVolume, CultureVegetable, MeteorologicalData
from .services import calculateReferenceEvapotranspiration

@login_required(login_url='/auth/login/')
def storeIrrigationVolume(request, geolocationId, cultureId):
    if not geolocationId or not cultureId:
        messages.error(request, "Geolocalização ou cultura não informada!")
        return redirect(f'{reverse("irrigationvolume_list_cultures")}?culture_id={cultureId or ""}')
    
    today = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo")).date()
    now_sp = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))

    already_exists = IrrigationVolume.objects.filter(
        culturevegetable_id=cultureId,
        meteorologicaldata__geolocation_id=geolocationId,
        date=today
    ).exists()

    if already_exists:
        messages.warning(request, "O volume de irrigação de hoje já foi gerado para essa cultura e cidade.")
        return redirect(f'{reverse("irrigationvolume_list_cultures")}?culture_id={cultureId}')

    calculateEtoResult = calculateReferenceEvapotranspiration(geolocationId)
    if not calculateEtoResult.get("success", False):
        messages.error(request, calculateEtoResult.get("message", "Erro ao calcular evapotranspiração."))
        return redirect(f'{reverse("irrigationvolume_list_cultures")}?culture_id={cultureId}')
    
    eto = calculateEtoResult["dataEto"]

    try:
        cultureVegetable = CultureVegetable.objects.get(pk=cultureId)
    except CultureVegetable.DoesNotExist:
        Log.objects.create(
            reference="create_irrigationvolume_view",
            exception={"error": "Cultura vegetal não encontrada, ID:" . cultureId},
            created_at=now_sp
        )
        logError("store_irrigationvolume_view", {
            "step": "exception",
            "error": "Cultura vegetal não encontrada, ID:" . cultureId
        })
        messages.error(request, "Cultura vegetal não encontrada.")
        return redirect(f'{reverse("irrigationvolume_list_cultures")}?culture_id={cultureId}')

    try:
        meteorologicalData = MeteorologicalData.objects.get(
            date=today,
            geolocation_id=geolocationId
        )
    except MeteorologicalData.DoesNotExist:
        messages.error(request, "Dados meteorológicos de hoje não encontrados para essa geolocalização.")
        return redirect(f'{reverse("irrigationvolume_list_cultures")}?culture_id={cultureId}')

    try:
        with transaction.atomic():
            IrrigationVolume.objects.create(
                phase_initial=eto * cultureVegetable.phase_initial_kc,
                phase_vegetative=eto * cultureVegetable.phase_vegetative_kc,
                phase_flowering=eto * cultureVegetable.phase_flowering_kc,
                phase_fruiting=eto * cultureVegetable.phase_fruiting_kc,
                phase_maturation=eto * cultureVegetable.phase_maturation_kc,
                culturevegetable=cultureVegetable,
                meteorologicaldata=meteorologicalData,
                date=today,
            )
        messages.success(request, "Volumes de irrigação gerados com sucesso!")

    except Exception as e:
        logError("store_irrigationvolume_view", {
            "step": "exception",
            "error": str(e),
        })
        messages.error(request, "Ocorreu um erro ao gerar os volumes de irrigação.")

    return redirect(f'{reverse("irrigationvolume_list_cultures")}?culture_id={cultureId}')

@login_required(login_url='/auth/login/')
def listForCulture(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    cultureVegetableList = CultureVegetable.objects.all()
    cultureId = request.GET.get('culture_id', '')
    formCultureVegetable = CultureVegetableForm()
    hasTodayData = False
    irrigationVolumeList = IrrigationVolume.objects.all()
    geolocations = Geolocation.objects.all()

    if cultureId:
        irrigationVolumeList = irrigationVolumeList.filter(culturevegetable_id=cultureId)
        hasTodayData = IrrigationVolume.objects.filter(
            culturevegetable_id=cultureId,
            date=date.today()
        ).exists()

    irrigationVolumeList = irrigationVolumeList.order_by('-date')
    paginator = Paginator(irrigationVolumeList, 12)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    return render(request, 'irrigationvolume/listforculture.html', context={
        'user': request.user,
        'logs': logs,
        'culturesvegetables': cultureVegetableList,
        'geolocations': geolocations,
        'page_obj': pageObj,              
        'culture_id': cultureId,  
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
        'today': date.today(),
        'has_unread': hasUnread
    })

def delete(request, irrigationVolumeId):
    try:
        culture_id = request.GET.get('culture_id', '')
        page_number = request.GET.get('page', '')

        with transaction.atomic():
            irrigation_volume = get_object_or_404(IrrigationVolume, id=irrigationVolumeId)
            culture_name = irrigation_volume.culturevegetable.name
            city_name = f"{irrigation_volume.geolocation} - {irrigation_volume.state}"

            irrigation_volume.delete()

        messages.success(
            request,
            f"Volumes de irrigação de hoje para {culture_name} em {city_name} deletados com sucesso!"
        )
    except Exception as e:
        logError("delete_irrigationvolume_view", {
            "step": "exception",
            "error": str(e),
        })
        messages.error(request, "Ocorreu um erro ao deletar os volumes de irrigação.")

    return redirect(f'{reverse("irrigationvolume_list_cultures")}?culture_id={culture_id}&page={page_number}')