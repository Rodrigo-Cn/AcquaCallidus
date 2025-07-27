from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from logs.models import Log
from .models import CultureVegetable
from .forms import CultureVegetableForm
from django.contrib import messages
from pytz import timezone as pytzTimezone
from django.utils import timezone


@login_required(login_url='/auth/login/') 
def list(request):
    logs = Log.objects.order_by('-created_at')[:10]
    name_query = request.GET.get('name', '')
    form_culture_vegetable = CultureVegetableForm()

    culturevegetables = CultureVegetable.objects.all()

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
        'form_culture_vegetable': form_culture_vegetable
    })

@require_POST
@login_required(login_url='/auth/login/')
def create(request):
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