from django.db import models
from django.contrib.auth.models import User

class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="profile/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem de {self.user.username} ({self.id})"

class WifiData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wifi_data")
    ssid = models.CharField(max_length=100)
    password = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        tipo = "Pública" if self.is_public else "Privada"
        return f"{self.ssid} - {tipo} ({self.user.username})"