from django.db import models
from django.db.models.signals import post_delete
from applications.libro.models import Libro

from .managers import PrestamoManager


class Lector(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=50)
    edad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre + ' ' + self.apellidos


class Prestamo(models.Model):
    libro = models.ForeignKey(
        Libro, on_delete=models.CASCADE, related_name='libro_prestamo')
    lector = models.ForeignKey(Lector, on_delete=models.CASCADE)
    prestamo = models.DateField('fecha_prestamo')
    devolucion = models.DateField(
        'fecha_devolucion', blank=True, null=True)
    devuelto = models.BooleanField(default=False)

    objects = PrestamoManager()

    def save(self, *args,  **kwargs):
        self.libro.stock = self.libro.stock - 1
        self.libro.save()
        super(Prestamo, self).save(*args, **kwargs)

    def __str__(self):
        return self.libro.titulo


def update_libro_stock(sender, instance, **kwargs):
    # actualizando el stok si se elimina un prestamo

    instance.libro.stock = instance.libro.stock + 1
    instance.libro.save()


post_delete.connect(update_libro_stock, sender=Prestamo)
