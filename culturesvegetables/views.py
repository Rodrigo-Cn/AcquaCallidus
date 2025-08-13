from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from logs.models import Log
from .models import CultureVegetable
from .forms import CultureVegetableForm
from django.contrib import messages
from pytz import timezone as pytzTimezone
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status 
from .serializers import CultureVegetableSerializer


@login_required(login_url='/auth/login/') 
def list(request):
    logs = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]
    name_query = request.GET.get('name', '')
    form_culture_vegetable = CultureVegetableForm()

    culturevegetables = CultureVegetable.objects.all().order_by('name')

    if name_query:
        culturevegetables = culturevegetables.filter(name__icontains=name_query)

    paginator = Paginator(culturevegetables, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'culturevegetable/list.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': page_obj,
        'name_query': name_query,
        'form_culture_vegetable': form_culture_vegetable,
        'has_unread': hasUnread
    })

@require_POST
@login_required(login_url='/auth/login/')
def store(request):
    todayWithHour = timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))

    try:
        form = CultureVegetableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cultura cadastrada com sucesso!")
            return redirect('culturevegetable_list')
        messages.error(request, "Dados inválidos! Verifique os campos.")
        return redirect(request.META.get('HTTP_REFERER', 'culturevegetable_list'))
    except Exception as e:
        Log.objects.create(
            reference="create_culturevegetable_controller",
            exception={"error": str(e)},
            created_at=todayWithHour
        )
        messages.error(request, "Ocorreu um erro ao criar a cultura!")
        return redirect(request.META.get('HTTP_REFERER', 'culturevegetable_list'))
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def edit(request, id):
    culture_vegetable = get_object_or_404(CultureVegetable, id=id)
    serializer = CultureVegetableSerializer(culture_vegetable)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
def delete(request, id):
    if request.method == "POST":
        try:
            culture_vegetable = CultureVegetable.objects.get(id=id)
            culture_vegetable.delete()
            messages.success(request, "Cultura vegetal deletada com sucesso.")
        except CultureVegetable.DoesNotExist:
            messages.error(request, "Cultura vegetal não encontrada.")
        except Exception as e:
            messages.error(request, "Erro ao deletar cultura vegetal")
        return redirect('culturevegetable_list')
    else:
        messages.error(request, "Método não permitido.")
        return redirect('culturevegetable_list')

@login_required
def update(request, id):
    if request.method == "POST":
        culture_vegetable = get_object_or_404(CultureVegetable, id=id)
        form = CultureVegetableForm(request.POST, instance=culture_vegetable)
        if form.is_valid():
            form.save()
            messages.success(request, "Cultura vegetal atualizada com sucesso.")
        else:
            messages.error(request, "Erro na atualização da cultura vegetal.")
    else:
        messages.error(request, "Método não permitido.")
    return redirect('culturevegetable_list')