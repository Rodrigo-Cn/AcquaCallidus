from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone
from pytz import timezone as pytzTimezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from logs.models import Log
from logs.services import logError
from .models import CultureVegetable
from .forms import CultureVegetableForm, CultureVegetableEditForm
from .serializers import CultureVegetableSerializer

@login_required(login_url='/auth/login/')
def list(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]

    nameQuery = request.GET.get('name', '')
    pageNumber = request.GET.get('page')

    formCultureVegetable = CultureVegetableForm()
    formEditCultureVegetable = CultureVegetableEditForm()

    cultureVegetables = CultureVegetable.objects.all().order_by('name')
    if nameQuery:
        cultureVegetables = cultureVegetables.filter(name__icontains=nameQuery)

    paginator = Paginator(cultureVegetables, 12)
    pageObj = paginator.get_page(pageNumber)

    context = {
        'user': request.user,
        'logs': logs,
        'page_obj': pageObj,
        'name_query': nameQuery,
        'form_culture_vegetable': formCultureVegetable,
        'form_edit_culture_vegetable': formEditCultureVegetable,
        'has_unread': hasUnread
    }

    return render(request, 'culturevegetable/list.html', context)

@require_POST
@login_required(login_url='/auth/login/')
def store(request):
    try:
        with transaction.atomic():
            form = CultureVegetableForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Cultura cadastrada com sucesso!")
                return redirect('culturevegetable_list')
            messages.error(request, "Dados inválidos! Verifique os campos.")
            return redirect(request.META.get('HTTP_REFERER', 'culturevegetable_list'))
    except Exception as e:
        logError("create_culturevegetable_view", {
            "step": "exception",
            "error": str(e),
        })
        messages.error(request, "Ocorreu um erro ao criar a cultura!")
        return redirect(request.META.get('HTTP_REFERER', 'culturevegetable_list'))
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def edit(request, id):
    cultureVegetable = get_object_or_404(CultureVegetable, id=id)
    serializer = CultureVegetableSerializer(cultureVegetable)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required(login_url='/auth/login/')
def delete(request, id):
    nameQuery = request.GET.get('name_page', '')
    pageNumber = request.GET.get('page')

    if request.method == "POST":
        try:
            with transaction.atomic():
                cultureVegetable = CultureVegetable.objects.get(id=id)
                cultureVegetable.delete()
                messages.success(request, "Cultura vegetal deletada com sucesso.")
        except CultureVegetable.DoesNotExist:
            messages.error(request, "Cultura vegetal não encontrada.")
        except Exception as e:
            logError("delete_culturevegetable_view", {
                "step": "exception",
                "error": str(e),
            })
            messages.error(request, "Erro ao deletar cultura vegetal")
    else:
        messages.error(request, "Método não permitido.")

    if pageNumber and nameQuery:
        return redirect(f"{reverse('culturevegetable_list')}?name={nameQuery}&page={pageNumber}")   
    elif pageNumber:
        return redirect(f"{reverse('culturevegetable_list')}?page={pageNumber}")
    return redirect('culturevegetable_list')

@login_required(login_url='/auth/login/')
def update(request, id):
    nameQuery = request.GET.get('name_page', '')
    pageNumber = request.GET.get('page')

    try:
        if request.method == "POST":
            with transaction.atomic():
                cultureVegetable = get_object_or_404(CultureVegetable, id=id)
                form = CultureVegetableForm(request.POST, instance=cultureVegetable)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Cultura vegetal {cultureVegetable.name} atualizado(a) com sucesso.")
                else:
                    messages.error(request, "Erro na atualização da cultura vegetal. Verifique os campos e tente novamente.")
        else:
            messages.error(request, "Método não permitido.")
    except Exception as e:
        logError("update_culturevegetable_view", {
            "step": "exception",
            "error": str(e),
        })
        messages.error(request, "Ocorreu um erro ao atualizar a cultura vegetal")

    if pageNumber and nameQuery:
        return redirect(f"{reverse('culturevegetable_list')}?name={nameQuery}&page={pageNumber}")   
    elif pageNumber:
        return redirect(f"{reverse('culturevegetable_list')}?page={pageNumber}")
    return redirect('culturevegetable_list')