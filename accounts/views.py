import os
import time
import hashlib
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from .models import UserImage, WifiData
from logs.services import logError

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
            ext = os.path.splitext(img.name)[1]

            hash_name = hashlib.sha256(
                (str(time.time()) + img.name).encode("utf-8")
            ).hexdigest()[:20]
            img.name = f"{hash_name}{ext}"

            with transaction.atomic():
                existing = UserImage.objects.filter(user=request.user).first()
                if existing:
                    existing.image.delete(save=False)
                    existing.delete()

                UserImage.objects.create(user=request.user, image=img)

            messages.success(request, "Foto de perfil salva com sucesso!")

        except Exception as e:
            logError("update_accounts_profile_image_accounts_view", {
                "step": "exception",
                "error": str(e),
            })
            messages.error(request, f"Erro ao salvar foto de perfil")

    elif request.method == "POST":
        messages.error(request, "Nenhuma imagem enviada!")

    nextUrl = request.META.get("HTTP_REFERER", "/")
    return redirect(nextUrl)

@login_required(login_url='/auth/login/')
def updateUser(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
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
            logError("update_accounts_view", {
                "step": "exception",
                "error": str(e),
            })
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
            with transaction.atomic():
                user.set_password(newPassword)
                user.save()
                update_session_auth_hash(request, user)
            messages.success(request, "Senha atualizada com sucesso!")

        except Exception as e:
            logError("change_password_accounts_view", {
                "step": "exception",
                "error": str(e),
            })
            messages.error(request, "Ocorreu um erro ao atualizar a senha.")

        return redirect(request.META.get("HTTP_REFERER", "/"))

    messages.error(request, "Método não permitido.")
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required(login_url='/auth/login/')
def updateWifi(request):
    if request.method == "POST":
        ssid = request.POST.get("ssid")
        password = request.POST.get("password", "")
        is_public = request.POST.get("is_public") == "on"

        if not ssid:
            messages.error(request, "O SSID é obrigatório.")
            return redirect("controllers_list")

        try:
            with transaction.atomic():
                wifi_data, created = WifiData.objects.get_or_create(
                    user=request.user,
                    ssid=ssid,
                    defaults={
                        "password": password if not is_public else None,
                        "is_public": is_public,
                    }
                )

                if not created:
                    wifi_data.password = password if not is_public else None
                    wifi_data.is_public = is_public
                    wifi_data.save()

            if created:
                messages.success(request, f"Rede Wi-Fi '{ssid}' cadastrada com sucesso!")
            else:
                messages.success(request, f"Rede Wi-Fi '{ssid}' atualizada com sucesso!")

        except Exception as e:
            logError("update_wifi_view", {
                "step": "exception",
                "error": str(e),
                "user_id": request.user.id,
                "ssid": ssid,
                "is_public": is_public,
            })
            messages.error(request, "Erro ao salvar a rede Wi-Fi.")

        return redirect("controllers_list")

    messages.error(request, "Método não permitido.")
    return redirect("controllers_list")