from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.http import require_POST
from django.contrib import messages
from pytz import timezone as pytzTimezone
from django.utils import timezone
from .models import Geolocation
from logs.models import Log
from culturesvegetables.forms import CultureVegetableForm
from .serializers import GeolocationSerializer
from rest_framework.response import Response
from rest_framework import status 
from django.db.models import Q

@login_required(login_url='/auth/login/')
def list(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    name_query = request.GET.get('name', '')
    form_culture_vegetable = CultureVegetableForm()

    geolocations = Geolocation.objects.all()

    if name_query:
        geolocations = geolocations.filter(
            Q(city__icontains=name_query) | Q(state__icontains=name_query)
        )

    paginator = Paginator(geolocations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'geolocation/list.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': page_obj,
        'name_query': name_query,
        'form_culture_vegetable': form_culture_vegetable,
        'has_unread': hasUnread
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

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def edit(request, id):
    geolocation = get_object_or_404(Geolocation, id=id)
    serializer = GeolocationSerializer(geolocation)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required(login_url='/auth/login/')
def delete(request, id):
    if request.method == "POST":
        try:
            geolocation = Geolocation.objects.get(id=id)
            geolocation.delete()
            messages.success(request, "Geolocalização deletada com sucesso.")
        except Geolocation.DoesNotExist:
            messages.error(request, "Geolocalização não encontrada.")
        except Exception as e:
            messages.error(request, "Erro ao deletar geolocalização")
        return redirect('geolocation_list')
    else:
        messages.error(request, "Método não permitido.")
        return redirect('geolocation_list')

@login_required(login_url='/auth/login/')
def update(request, id):
    try:
        if request.method == "POST":
            geolocation = get_object_or_404(Geolocation, id=id)

            city = request.POST.get('city')
            state = request.POST.get('state')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            if not all([city, state, latitude, longitude]):
                messages.error(request, "Todos os campos são obrigatórios.")
                return redirect('geolocation_list')

            geolocation.city = city
            geolocation.state = state
            geolocation.latitude = latitude
            geolocation.longitude = longitude
            geolocation.save()

            messages.success(request, f"Geolocalização {geolocation.city} - {geolocation.state} atualizada com sucesso.")
        else:
            messages.error(request, "Método não permitido.")
    except Exception as e:
        messages.error(request, "Ocorreu um erro ao atualizar a geolocalização")
    
    return redirect('geolocation_list')