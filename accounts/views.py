from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
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

@login_required(login_url='/auth/login/')
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

        except Exception as e:
            messages.error(request, "Erro ao salvar foto de perfil")

    elif request.method == "POST":
        messages.error(request, "Nenhuma imagem enviada!")

    nextUrl = request.META.get("HTTP_REFERER", "/")
    return redirect(nextUrl)

@login_required(login_url='/auth/login/')
def updateUser(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            email = request.POST.get("email")

            user = request.user

            if username:
                user.username = username
            if email:
                user.email = email

            user.save()

            messages.success(request, "Perfil atualizado com sucesso!")

        except Exception as e:
            messages.error(request, "Ocorreu um erro ao atualizar perfil")

        return redirect(request.META.get("HTTP_REFERER", "/"))

    messages.error(request, "Método não permitido.")
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required(login_url='/auth/login/')
def changePassword(request):
    if request.method == "POST":
        currentPassword = request.POST.get("current_password")
        newPassword = request.POST.get("new_password")
        confirmPassword = request.POST.get("confirm_password")
        user = request.user

        if not user.check_password(currentPassword):
            messages.error(request, "A senha atual está incorreta.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        if newPassword != confirmPassword:
            messages.error(request, "A senha e a confirmação não coincidem.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        if not newPassword:
            messages.error(request, "A nova senha não pode ser vazia.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        try:
            user.set_password(newPassword)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Senha atualizada com sucesso!")
        except Exception as e:
            messages.error(request, "Ocorreu um erro ao atualizar a senha.")

        return redirect(request.META.get("HTTP_REFERER", "/"))

    messages.error(request, "Método não permitido.")
    return redirect(request.META.get("HTTP_REFERER", "/"))