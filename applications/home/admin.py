from django.contrib import admin
from .models import Cliente, Empleados

admin.site.register(Empleados)
admin.site.register(Cliente)
