from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 50, verbose_name="Nombre")
    email = models.CharField(max_length=60, unique=True , verbose_name="Correo Electronico")
    password = models.CharField(max_length = 50, verbose_name = "Contraseña")
    created_at = models.DateField(auto_now_add = True, verbose_name = "Creado el")
    update_at = models.DateField(auto_now=True, verbose_name = "Actualizado el")
    