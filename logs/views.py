from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from logs.models import Log
from culturesvegetables.forms import CultureVegetableForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status 

@login_required(login_url='/auth/login/')
def list(request):
    logs = Log.objects.order_by('-created_at')  
    logs_page = Log.objects.order_by('-created_at')
    hasUnread = logs.filter(viewed=False).exists()
    logs = logs[:12]

    form_culture_vegetable = CultureVegetableForm()
    date_query = request.GET.get('date', '')

    if date_query:
        parsed_date = parse_date(date_query)
        if parsed_date:
            logs_page = logs_page.filter(created_at__date=parsed_date)

    paginator = Paginator(logs_page, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'log/list.html', {
        'logs': logs,
        'logs_page': logs_page,
        'page_obj': page_obj,
        'user': request.user,
        'date_query': date_query,
        'form_culture_vegetable': form_culture_vegetable,
        'has_unread': hasUnread
    })

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def markLogsViewed(request):
    updated_count = Log.objects.filter(viewed=False).update(viewed=True)
    return Response(
        {"message": f"{updated_count} registros atualizados."},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def getLogException(request, id):
    try:
        log = Log.objects.get(id=id)
    except Log.DoesNotExist:
        return Response({"error": "Log não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if not log.viewed:
        log.viewed = True
        log.save()

    return Response({"exception": log.exception}, status=status.HTTP_200_OK)