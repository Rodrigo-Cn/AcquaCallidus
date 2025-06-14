from django.shortcuts import render
from django.contrib import messages

def home(request):
    ## pages/
    return render(request, 'culturevegetable/list.html')