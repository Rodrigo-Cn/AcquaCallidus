from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from logs.models import Log
from .models import CultureVegetable
from .forms import CultureVegetableForm

@login_required(login_url='/auth/login/') 
def list(request):
    logs = Log.objects.order_by('-created_at')[:10]
    name_query = request.GET.get('name', '')
    form_culture_vegetable = CultureVegetableForm()

    culturevegetables = CultureVegetable.objects.all()

    if name_query:
        culturevegetables = culturevegetables.filter(name__icontains=name_query)

    paginator = Paginator(culturevegetables, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'culturevegetable/list.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': page_obj,
        'name_query': name_query,
        'form_culture_vegetable': form_culture_vegetable
    })


def create(request):
    if request.method == 'POST':
        form = CultureVegetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nome-da-sua-listagem-ou-sucesso')
    else:
        form = CultureVegetableForm()
    return render(request, 'seu_template.html', {'form': form})
