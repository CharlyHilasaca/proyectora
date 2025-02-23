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
    roles = models.ForeignKey(Roles, on_delete=models.SET_DEFAULT, default="default_role")
    vistapl = models.ForeignKey(Accesos, on_delete=models.SET_DEFAULT, default="rep_dev/vistapl.html")
    
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