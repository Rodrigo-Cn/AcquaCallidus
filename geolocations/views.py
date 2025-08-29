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
from django.urls import reverse

@login_required(login_url='/auth/login/')
def list(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    nameQuery = request.GET.get('name', '')
    formCulturevegetable = CultureVegetableForm()

    geolocations = Geolocation.objects.all()

    if nameQuery:
        geolocations = geolocations.filter(
            Q(city__icontains=nameQuery) | Q(state__icontains=nameQuery)
        )

    paginator = Paginator(geolocations, 12)
    pageNumber = request.GET.get('page')
    pageobj = paginator.get_page(pageNumber)

    return render(request, 'geolocation/list.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': pageobj,
        'name_query': nameQuery,
        'form_culture_vegetable': formCulturevegetable,
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
    nameQuery = request.GET.get('name_page', '')
    pageNumber = request.GET.get('page')

    if request.method == "POST":
        try:
            geolocation = Geolocation.objects.get(id=id)
            geolocation.delete()
            messages.success(request, "Geolocalização deletada com sucesso.")
        except Geolocation.DoesNotExist:
            messages.error(request, "Geolocalização não encontrada.")
        except Exception:
            messages.error(request, "Erro ao deletar geolocalização")
    else:
        messages.error(request, "Método não permitido.")

    if pageNumber and nameQuery:
        return redirect(f"{reverse('geolocation_list')}?name={nameQuery}&page={pageNumber}")
    elif pageNumber:
        return redirect(f"{reverse('geolocation_list')}?page={pageNumber}")
    return redirect('geolocation_list')

@login_required(login_url='/auth/login/')
def update(request, id):
    nameQuery = request.GET.get('name_page', '')
    pageNumber = request.GET.get('page')

    try:
        if request.method == "POST":
            geolocation = get_object_or_404(Geolocation, id=id)

            city = request.POST.get('city')
            state = request.POST.get('state')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            if not all([city, state, latitude, longitude]):
                messages.error(request, "Todos os campos são obrigatórios.")
            else:
                geolocation.city = city
                geolocation.state = state
                geolocation.latitude = latitude
                geolocation.longitude = longitude
                geolocation.save()

                messages.success(
                    request,
                    f"Geolocalização {geolocation.city} - {geolocation.state} atualizada com sucesso."
                )
        else:
            messages.error(request, "Método não permitido.")
    except Exception:
        messages.error(request, "Ocorreu um erro ao atualizar a geolocalização")

    if pageNumber and nameQuery:
        return redirect(f"{reverse('geolocation_list')}?name={nameQuery}&page={pageNumber}")
    elif pageNumber:
        return redirect(f"{reverse('geolocation_list')}?page={pageNumber}")
    return redirect('geolocation_list')

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def favorite(request, id):
    Geolocation.objects.filter(favorite=True).update(favorite=False)
    geolocation = get_object_or_404(Geolocation, id=id)
    geolocation.favorite = True
    geolocation.save()

    return Response(status=204)