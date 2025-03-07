import os
import uuid
from datetime import datetime
from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.cache import never_cache

# MODELOS

class Accesos(models.Model):
    ruta = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.ruta

class Roles(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    accesos = models.ManyToManyField(Accesos, related_name="roles")
    
    def __str__(self):
        return self.nombre

class Dev(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    roles = models.ForeignKey(Roles, on_delete=models.SET_DEFAULT, default="Admin Dev")
    vistapl = models.ForeignKey(Accesos, on_delete=models.SET_DEFAULT, default="rep_dev/ds_rep_dev/index_ds_dev.html")
    
    def __str__(self):
        return self.username

class Descripcion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Opcion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    clase = models.CharField(max_length=100, null=True, blank=True)  # Nuevo campo que acepta valores nulos
    descripcion = models.ForeignKey(Descripcion, on_delete=models.CASCADE, related_name="opciones")  # Relación con Descripción

    def __str__(self):
        return self.nombre

class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    opciones = models.ManyToManyField(Opcion, related_name="menus")
    
    def __str__(self):
        return self.nombre

class DevOpcion(models.Model):
    dev = models.ForeignKey(Dev, on_delete=models.CASCADE, related_name="opciones")
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("dev", "opcion")
    
    def __str__(self):
        return f"{self.dev.username} - {self.opcion.nombre}"
    
def get_unique_image_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{unique_id}_{timestamp}.{ext}"
    return os.path.join('rep_dev/static/rep_dev/images/', filename)

class Contech(models.Model):
    nametech = models.CharField(max_length=100, unique=True)
    imgtech = models.ImageField(upload_to=get_unique_image_path)  # Usa la función personalizada
    classct = models.CharField(max_length=100, default='content-tech hidden')
    classit = models.CharField(max_length=100, default='img-tech')
    
    def __str__(self):
        return self.nametech
    
    @property
    def imgtech_url(self):
        # Devuelve la ruta de la imagen a partir del segundo slash
        return '/'.join(self.imgtech.url.split('/')[2:])