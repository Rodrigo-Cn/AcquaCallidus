from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserImage

def login(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user) 
            messages.success(request, f"Bem-vindo, {user.first_name or user.username}!")
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'authentication/login.html')

@login_required
def uploadProfileImage(request):
    if request.method == "POST" and "image" in request.FILES:
        try:
            img = request.FILES["image"]

            existing = UserImage.objects.filter(user=request.user).first()
            if existing:
                existing.image.delete(save=False)
                existing.delete()

            UserImage.objects.create(user=request.user, image=img)

            messages.success(request, "Foto de perfil salva com sucesso!")

        except Exception:
            messages.error(request, "Erro ao salvar foto de perfil")

    elif request.method == "POST":
        messages.error(request, "Nenhuma imagem enviada!")

    nextUrl = request.META.get("HTTP_REFERER", "/")
    return redirect(nextUrl)