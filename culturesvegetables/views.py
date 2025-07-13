from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from logs.models import Log
from .models import CultureVegetable

@login_required(login_url='/auth/login/') 
def list(request):
    logs = Log.objects.order_by('-created_at')[:10]
    name_query = request.GET.get('name', '')

    culturevegetables = CultureVegetable.objects.all()

    if name_query:
        culturevegetables = culturevegetables.filter(name__icontains=name_query)

    paginator = Paginator(culturevegetables, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'culturevegetable/list.html', context={
        'user': request.user,
        'logs': logs,
        'page_obj': page_obj,
        'name_query': name_query,
    })
