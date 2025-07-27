from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from logs.models import Log
from culturesvegetables.forms import CultureVegetableForm

@login_required(login_url='/auth/login/')
def list(request):
    logs = Log.objects.order_by('-created_at')[:10]
    paginator = Paginator(logs, 10)
    form_culture_vegetable = CultureVegetableForm()
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'log/list.html', context={
        "page_obj": page_obj,
        'user': request.user,
        'logs': logs,
        'form_culture_vegetable': form_culture_vegetable
    })