from django.db import models

class Accesos(models.Model):
    ruta = models.CharField(max_length=255, unique=True)  # Almacena la ruta HTML

    def __str__(self):
        return self.ruta

class Roles(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre del rol
    accesos = models.ManyToManyField(Accesos, related_name="roles")  # Relación M:M con Accesos

    def __str__(self):
        return self.nombre

class Dev(models.Model):
    first_name = models.CharField(max_length=100)  # Nombres
    last_name = models.CharField(max_length=100)   # Apellidos
    username = models.CharField(max_length=100, unique=True)  # Usuario único
    email = models.EmailField(unique=True)  # Correo electrónico
    password = models.CharField(max_length=255)  # Contraseña
    roles = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)  # Un Dev tiene un Rol
    vistapl = models.ForeignKey(Accesos, on_delete=models.SET_DEFAULT, default="rep_dev/vistapl.html")  # Vista por defecto

    def __str__(self):
        return self.username
