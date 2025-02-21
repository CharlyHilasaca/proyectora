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
    roles = models.ForeignKey(Roles, on_delete=models.SET_DEFAULT, default=1)  # Un Dev tiene un Rol
    vistapl = models.ForeignKey(Accesos, on_delete=models.SET_DEFAULT, default="rep_dev/vistapl.html")  # Vista por defecto

    def __str__(self):
        return self.username
    
class Descripcion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Opcion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    opciones = models.ManyToManyField(Opcion, related_name="menus")

    def __str__(self):
        return self.nombre

# 🔹 Relación entre Dev y Descripcion (Cada usuario tiene descripciones únicas)
class DevDescripcion(models.Model):
    dev = models.ForeignKey(Dev, on_delete=models.CASCADE, related_name="descripciones")
    descripcion = models.ForeignKey(Descripcion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("dev", "descripcion")  # Evita que un usuario tenga descripciones repetidas

    def __str__(self):
        return f"{self.dev.username} - {self.descripcion.nombre}"

# 🔹 Relación entre DevDescripcion y Opcion (Cada opción es única dentro de un usuario)
class DevOpcion(models.Model):
    dev_descripcion = models.ForeignKey(DevDescripcion, on_delete=models.CASCADE, related_name="opciones")
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("dev_descripcion", "opcion")  # Evita opciones duplicadas por usuario

    def __str__(self):
        return f"{self.dev_descripcion.dev.username} - {self.opcion.nombre}"