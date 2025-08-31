from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from logs.models import Log
from culturesvegetables.forms import CultureVegetableForm
from rest_framework import status
from culturesvegetables.models import CultureVegetable
from geolocations.models import Geolocation
from django.contrib import messages
from django.utils.dateparse import parse_date
from .models import Controller, ValveController
from culturesvegetables.models import CultureVegetable
from geolocations.models import Geolocation
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import ControllerSerializer
import random
import string

@login_required(login_url='/auth/login/')
def list(request):
    return render(request, 'controller/list.html')

@login_required(login_url='/auth/login/')
def create(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    formCulturevegetable = CultureVegetableForm()
    geolocations = Geolocation.objects.all()
    culturesVegetables = CultureVegetable.objects.all()
    
    return render(request, 'controller/create.html', context={
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': formCulturevegetable,
        'has_unread': hasUnread,
        'geolocations': geolocations,
        'cultures_vegetables': culturesVegetables
    })

@login_required(login_url='/auth/login/')
def irrigationsControllersList(request, id):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    formCulturevegetable = CultureVegetableForm()
    geolocations = Geolocation.objects.all()
    culturesVegetables = CultureVegetable.objects.all()

    return render(request, 'controller/irrigationcontroller/list.html', context={
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': formCulturevegetable,
        'has_unread': hasUnread,
        'geolocations': geolocations,
        'cultures_vegetables': culturesVegetables
    })

def generateSecurityCode(length=40):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@login_required(login_url='/auth/login/')
def createController(request):
    if request.method == "POST":
        try:
            controller = Controller.objects.create(
                name=request.POST.get("name"),
                device=request.POST.get("device"),
                ip_address=request.POST.get("ip_address"),
                phase_vegetable=request.POST.get("phase_vegetable"),
                active=bool(request.POST.get("active")),                
                last_irrigation=parse_date(request.POST.get("last_irrigation")) if request.POST.get("last_irrigation") else None,
                culturevegetable=CultureVegetable.objects.filter(id=request.POST.get("culturevegetable")).first() if request.POST.get("culturevegetable") else None,
                geolocation=Geolocation.objects.filter(id=request.POST.get("geolocation")).first() if request.POST.get("geolocation") else None,
                security_code=generateSecurityCode(40)
            )

            for i in range(1, 5):
                plants = request.POST.get(f"valves[{i}][plants]")
                radius = request.POST.get(f"valves[{i}][radius]")
                if plants and radius:
                    ValveController.objects.create(
                        plants_number=plants,
                        irrigation_radius=radius,
                        controller=controller,
                        active=True
                    )

            messages.success(request, "Controlador criado com sucesso")
            return redirect("controllers_create")
        except Exception as e:
            messages.error(request, "Erro ao salvar controlador")
            return redirect("controllers_create")


    messages.info(request, "Método incorreto.")
    return redirect("controllers_create")

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def edit(request, id):
    controller = get_object_or_404(Controller, id=id)
    serializer = ControllerSerializer(controller)
    return Response(serializer.data, status=status.HTTP_200_OK)
