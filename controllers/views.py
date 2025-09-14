from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from logs.models import Log
from culturesvegetables.forms import CultureVegetableForm
from rest_framework import status
from culturesvegetables.models import CultureVegetable
from geolocations.models import Geolocation
from django.contrib import messages
from django.utils.dateparse import parse_date
from .models import Controller, ValveController, IrrigationController
from irrigationvolumes.models import IrrigationVolume
from meteorologicaldatas.models import MeteorologicalData
from geolocations.models import Geolocation
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .services import calculateReferenceEvapotranspiration
from .serializers import ControllerSerializer
from rest_framework.views import APIView
from pytz import timezone as pytzTimezone
from django.db import transaction
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
import random
import string

@login_required(login_url='/auth/login/')
def listController(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    geolocations = Geolocation.objects.all()
    culturesVegetables = CultureVegetable.objects.all()

    nameQuery = request.GET.get('name', '')
    formCulturevegetable = CultureVegetableForm()

    controllers = Controller.objects.prefetch_related('valves').all().order_by('created_at')

    if nameQuery:
        controllers = controllers.filter(
            Q(name__icontains=nameQuery)
        )

    for c in controllers:
        valves = list(c.valves.all()[:3])
        while len(valves) < 3:
            valves.append(None)
        c.valves_fixed = valves

    paginator = Paginator(controllers, 9)
    pageNumber = request.GET.get('page')
    pageobj = paginator.get_page(pageNumber)

    return render(request, 'controller/list.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': pageobj,
        'name_query': nameQuery,
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
def storeController(request):
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
                security_code=generateSecurityCode(20)
            )

            for i in range(1, 5):
                plants = request.POST.get(f"valves[{i}][plants]")
                radius = request.POST.get(f"valves[{i}][radius]")
                if plants and radius:
                    ValveController.objects.create(
                        plants_number=plants,
                        irrigation_radius=radius,
                        controller=controller,
                        order=i,
                    )

            messages.success(request, "Controlador criado com sucesso")
            return redirect("controllers_list")
        except Exception as e:
            messages.error(request, "Erro ao salvar controlador")
            return redirect("controllers_list")


    messages.info(request, "Método incorreto.")
    return redirect("controllers_list")

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def edit(request, id):
    controller = get_object_or_404(Controller, id=id)
    serializer = ControllerSerializer(controller)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required(login_url='/auth/login/')
def update(request, id):
    if request.method == "POST":
        try:
            controller = get_object_or_404(Controller, id=id)

            controller.name = request.POST.get("name")
            controller.device = request.POST.get("device")
            controller.ip_address = request.POST.get("ip_address")
            controller.phase_vegetable = request.POST.get("phase_vegetable")
            controller.active = bool(request.POST.get("active"))
            controller.last_irrigation = parse_date(request.POST.get("last_irrigation")) if request.POST.get("last_irrigation") else None
            controller.culturevegetable = CultureVegetable.objects.filter(id=request.POST.get("culturevegetable")).first() if request.POST.get("culturevegetable") else None
            controller.geolocation = Geolocation.objects.filter(id=request.POST.get("geolocation")).first() if request.POST.get("geolocation") else None
            controller.save()

            existing_valves_ids = [] 
            for i in range(1, 5):
                valve_id = request.POST.get(f"valves[{i}][id]")
                plants = request.POST.get(f"valves[{i}][plants]")
                radius = request.POST.get(f"valves[{i}][radius]")

                if plants and radius:
                    if valve_id:  
                        valve = ValveController.objects.filter(id=valve_id, controller=controller).first()
                        if valve:
                            valve.plants_number = plants
                            valve.irrigation_radius = radius
                            valve.save()
                            existing_valves_ids.append(valve.id)
                    else:
                        valve = ValveController.objects.create(
                            plants_number=plants,
                            irrigation_radius=radius,
                            controller=controller,
                            active=True
                        )
                        existing_valves_ids.append(valve.id)

            ValveController.objects.filter(controller=controller).exclude(id__in=existing_valves_ids).delete()

            messages.success(request, "Controlador editado com sucesso")
            return redirect("controllers_list")

        except Exception as e:
            messages.error(request, "Erro ao editar controlador")
            return redirect("controllers_list")

    messages.info(request, "Método incorreto.")
    return redirect("controllers_create")

@login_required(login_url='/auth/login/')
def delete(request, id):
    nameQuery = request.GET.get('name_page', '')
    pageNumber = request.GET.get('page')

    if request.method == "POST":
        try:
            controller = Controller.objects.get(id=id)
            controller.delete()
            messages.success(request, "Controlador deletado com sucesso.")
        except Controller.DoesNotExist:
            messages.error(request, "Controlador não encontrado.")
        except Exception as e:
            messages.error(request, "Erro ao deletar controlador")
    else:
        messages.error(request, "Método não permitido.")

    if pageNumber and nameQuery :
        return redirect(f"{reverse('controllers_list')}?name={nameQuery}&page={pageNumber}")   
    elif pageNumber:
        return redirect(f"{reverse('controllers_list')}?page={pageNumber}")
    return redirect('controllers_list')

class ControllerOnAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            now_sp = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))
            controllerId = request.data.get("controllerId")
            valveId = request.data.get("valveId")
            securityCode = request.data.get("securityCode")
            controllerUuid = request.data.get("controllerUuid")
            ipAdress = request.data.get("ipAdress")
            today = now_sp.date()

            self._updateAttemptController(controllerId)
            
            with transaction.atomic():

                error = self._validateRequestData(controllerId, valveId, securityCode, controllerUuid)
                if error:
                    self._log_error("controller_api_post_on", {"step": "validate_request", "request": request.data})
                    return error

                controller = self._getController(controllerId, controllerUuid, securityCode)
                if isinstance(controller, Response):
                    self._log_error("controller_api_post_on", {"step": "get_controller", "controllerId": controllerId})
                    return controller

                valve = self._getValve(controller, valveId)
                if isinstance(valve, Response):
                    self._log_error("controller_api_post_on", {"step": "get_valve", "valveId": valveId})
                    return valve

                irrigationVolume = IrrigationVolume.objects.filter(
                    culturevegetable_id=controller.culturevegetable.id,
                    meteorologicaldata__geolocation_id=controller.geolocation.id,
                    date=today
                ).first()

                if not irrigationVolume:
                    irrigationVolume = self._storeIrrigationVolume(controller)
                    if irrigationVolume is None:
                        self._log_error("controller_api_post_on", {
                            "step": "create_irrigationvolume",
                            "error": "Cultura vegetal não encontrada"
                        })
                        return Response(
                            {"success": False, "message": "Falha ao gerar volume de irrigação."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                existingIrrigation = IrrigationController.objects.filter(
                    controller=controller,
                    culturevegetable=controller.culturevegetable,
                    geolocation=controller.geolocation,
                    phase_vegetable=controller.phase_vegetable,
                    date=today,
                    valvecontroller_id=valve.id
                ).first()

                if existingIrrigation:
                    self._log_error("controller_api_post_on", {
                        "step": "duplicate_irrigation",
                        "valveId": valve.id,
                        "message": "Já existe irrigação registrada para esta válvula hoje."
                    })
                    return Response(
                        {"success": False, "message": "Já existe irrigação registrada para esta válvula hoje."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                error = self._validateSingleValveActive(controller, valve)
                if error:
                    return error

                irrigationController = self._createIrrigationController(controller, valve, irrigationVolume)

                controller.status = True
                controller.ip_address = ipAdress or "127.0.0.1"
                controller.last_irrigation = now_sp
                controller.attempts = 0
                controller.save(update_fields=["status", "ip_address", "last_irrigation", "attempts"])

                valve.status = True
                valve.last_irrigation = now_sp
                valve.save(update_fields=["status", "last_irrigation"])

                return Response(
                    {
                        "success": True,
                        "total_liters": irrigationController.total_liters,
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            self._log_error("controller_api_post_on", {
                "step": "exception",
                "error": str(e),
                "request": request.data
            })
            return Response(
                {"success": False, "message": "Ocorreu um erro interno no servidor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _validateSingleValveActive(self, controller, valve):
        otherActiveValve = controller.valves.filter(status=True).exclude(id=valve.id).first()
        if otherActiveValve:
            self._log_error("controller_api_post_on", {
                "step": "one_valve_at_time",
                "controllerId": controller.id,
                "valveId": otherActiveValve.id,
                "message": "Já existe outra válvula ligada neste controlador."
            })
            return Response(
                {"success": False, "message": "Só é permitido ligar uma válvula por vez neste controlador."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return None

    def _validateRequestData(self, controllerId, valveId, securityCode, controllerUuid):
        if not controllerId or not valveId or not securityCode or not controllerUuid:
            return Response(
                {"success": False, "message": "Dados de autenticação do controlador estão incorretos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return None

    def _getController(self, controllerId, controllerUuid, securityCode):
        try:
            controller = Controller.objects.prefetch_related("valves").get(
                id=controllerId,
                uuid=controllerUuid,
                security_code=securityCode
            )
            if not controller.active:
                self._log_error("controller_api_post_on", {
                    "step": "get_controller",
                    "controllerId": controllerId,
                    "error": "Dispositivo desativado"
                })
                return Response(
                    {"success": False, "message": "Dispositivo desativado!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if controller.attempts >= 5:
                self._log_error("controller_api_post_on", {
                    "step": "get_controller",
                    "controllerId": controllerId,
                    "error": "Ocorreram várias tentativas de acessar o controlador"
                })
            return controller
        except Controller.DoesNotExist:
            self._log_error("controller_api_post_on", {
                "step": "get_controller",
                "controllerId": controllerId,
                "error": "Controlador não encontrado ou credenciais inválidas"
            })
            return Response(
                {"success": False, "message": "Dados de autenticação do controlador estão incorretos"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _updateAttemptController(self, controllerId):
        try:
            controller = Controller.objects.prefetch_related("valves").get(
                id=controllerId,
            )
        except Controller.DoesNotExist:
            return

        if controller.attempts >= 5:
            self._log_error("controller_api_post_on", {
                "step": "get_controller",
                "controllerId": controllerId,
                "error": "Ocorreram várias tentativas de acessar o controlador"
            })

        controller.attempts += 1
        controller.save()

    def _getValve(self, controller, valveId):
        try:
            return controller.valves.get(id=valveId)
        except ValveController.DoesNotExist:
            self._log_error("controller_api_post_on", {"step": "get_valve", "valveId": valveId})
            return Response(
                {"success": False, "message": f"Válvula {valveId} não encontrada neste controlador."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _storeIrrigationVolume(self, controller):
        today = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo")).date()
        calculateEtoResult = calculateReferenceEvapotranspiration(controller.geolocation.id)
        if not calculateEtoResult.get("success", False):
            self._log_error("controller_api_post_on", {"step": "calculate_eto", "error": "Falha ao calcular Eto"})
            return None

        try:
            meteorologicalData = MeteorologicalData.objects.get(
                date=today,
                geolocation_id=controller.geolocation.id
            )
        except MeteorologicalData.DoesNotExist:
            self._log_error("controller_api_post_on", {"step": "meteorological_data", "error": "Dados meteorológicos não encontrados"})
            return None

        return IrrigationVolume.objects.create(
            phase_initial=calculateEtoResult["dataEto"] * controller.culturevegetable.phase_initial_kc,
            phase_vegetative=calculateEtoResult["dataEto"] * controller.culturevegetable.phase_vegetative_kc,
            phase_flowering=calculateEtoResult["dataEto"] * controller.culturevegetable.phase_flowering_kc,
            phase_fruiting=calculateEtoResult["dataEto"] * controller.culturevegetable.phase_fruiting_kc,
            phase_maturation=calculateEtoResult["dataEto"] * controller.culturevegetable.phase_maturation_kc,
            culturevegetable=controller.culturevegetable,
            meteorologicaldata=meteorologicalData,
            date=today,
        )

    def _createIrrigationController(self, controller, valve, irrigationVolume):
        phaseMap = {
            1: irrigationVolume.phase_initial,
            2: irrigationVolume.phase_vegetative,
            3: irrigationVolume.phase_flowering,
            4: irrigationVolume.phase_fruiting,
            5: irrigationVolume.phase_maturation,
        }

        irrigationVolumeFase = phaseMap.get(controller.phase_vegetable)
        if irrigationVolumeFase is None:
            raise ValueError(f"Fase {controller.phase_vegetable} inválida.")

        return IrrigationController.objects.create(
            total_liters=(irrigationVolumeFase * valve.irrigation_radius) * valve.plants_number,
            plants_number=valve.plants_number,
            irrigation_radius=valve.irrigation_radius,
            phase_vegetable=controller.phase_vegetable,
            controller=controller,
            culturevegetable=controller.culturevegetable,
            geolocation=controller.geolocation,
            valvecontroller=valve 
        )

    def _log_error(self, reference, exception):
        Log.objects.create(
            reference=reference,
            exception=exception,
            created_at=timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))
        )

class ControllerOffAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            now_sp = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))
            controllerId = request.data.get("controllerId")
            valveId = request.data.get("valveId")
            securityCode = request.data.get("securityCode")
            controllerUuid = request.data.get("controllerUuid")

            self._updateAttemptController(controllerId)
            
            with transaction.atomic():
                error = self._validateRequestData(controllerId, valveId, securityCode, controllerUuid)
                if error:
                    self._log_error("controller_api_post_off", {"step": "validate_request", "request": request.data})
                    return error

                controller = self._getController(controllerId, controllerUuid, securityCode)
                if isinstance(controller, Response):
                    self._log_error("controller_api_post_off", {"step": "get_controller", "controllerId": controllerId})
                    return controller

                valve = self._getValve(controller, valveId)
                if isinstance(valve, Response):
                    self._log_error("controller_api_post_off", {"step": "get_valve", "valveId": valveId})
                    return valve

                if not valve.status:
                    return Response(
                        {"success": False, "message": "A válvula já está desligada."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                valve.status = False
                valve.save(update_fields=["status"])

                if controller.valves.count() == valve.order:
                    controller.status = False
                    controller.save(update_fields=["status"])
                
            return Response(
                {"success": True, "message": "Válvula desligada com sucesso."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            self._log_error("controller_api_post_off", {
                "step": "exception",
                "error": str(e),
                "request": request.data
            })
            return Response(
                {"success": False, "message": "Ocorreu um erro interno no servidor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _validateRequestData(self, controllerId, valveId, securityCode, controllerUuid):
        if not controllerId or not valveId or not securityCode or not controllerUuid:
            return Response(
                {"success": False, "message": "Dados de autenticação do controlador estão incorretos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return None

    def _getController(self, controllerId, controllerUuid, securityCode):
        try:
            controller = Controller.objects.prefetch_related("valves").get(
                id=controllerId,
                uuid=controllerUuid,
                security_code=securityCode
            )
            if not controller.active:
                self._log_error("controller_api_post_off", {
                    "step": "get_controller",
                    "controllerId": controllerId,
                    "error": "Dispositivo desativado"
                })
                return Response(
                    {"success": False, "message": "Dispositivo desativado!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if controller.attempts >= 5:
                self._log_error("controller_api_post_off", {
                    "step": "get_controller",
                    "controllerId": controllerId,
                    "error": "Ocorreram várias tentativas de acessar o controlador"
                })
            return controller
        except Controller.DoesNotExist:
            self._log_error("controller_api_post_off", {
                "step": "get_controller",
                "controllerId": controllerId,
                "error": "Controlador não encontrado ou credenciais inválidas"
            })
            return Response(
                {"success": False, "message": "Dados de autenticação do controlador estão incorretos"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _updateAttemptController(self, controllerId):
        try:
            controller = Controller.objects.prefetch_related("valves").get(
                id=controllerId,
            )
        except Controller.DoesNotExist:
            return

        if controller.attempts >= 5:
            self._log_error("controller_api_post_off", {
                "step": "get_controller",
                "controllerId": controllerId,
                "error": "Ocorreram várias tentativas de acessar o controlador"
            })

        controller.attempts += 1
        controller.save()

    def _getValve(self, controller, valveId):
        try:
            return controller.valves.get(id=valveId)
        except ValveController.DoesNotExist:
            self._log_error("controller_api_post_off", {"step": "get_valve", "valveId": valveId})
            return Response(
                {"success": False, "message": f"Válvula {valveId} não encontrada neste controlador."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _log_error(self, reference, exception):
        Log.objects.create(
            reference=reference,
            exception=exception,
            created_at=timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))
        )
