from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from logs.models import Log

@login_required(login_url='/auth/login/') 
def list(request):
    logs = Log.objects.order_by('-created_at')[:10]

    return render(request, 'meteorologicaldata/list.html', context={
        'user': request.user,
        'logs': logs,
    })
