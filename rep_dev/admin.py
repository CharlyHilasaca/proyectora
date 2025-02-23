from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Accesos)
admin.site.register(Roles)
admin.site.register(Dev)
admin.site.register(Descripcion)
admin.site.register(Opcion)
admin.site.register(DevOpcion)