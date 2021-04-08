from applications.libro.managers import LibroManager, CategoriaManager
from django.db import models
from django.db.models.signals import post_save
from PIL import Image
from applications.autor.models import Autor


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    objects = CategoriaManager()

    def __str__(self):
        return self.nombre + ' - ' + str(self.id)


class Libro(models.Model):
    autor = models.ManyToManyField(Autor)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='categoria_libro')
    titulo = models.CharField(max_length=50)
    fecha = models.DateField('Fecha de lanzamiento')
    portada = models.ImageField(upload_to='portada')
    visitas = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)

    objects = LibroManager()

    def __str__(self):
        return str(self.id) + ' - ' + self.titulo


def optimize_image(sender, instance, **kwargs):
    if instance.portada:
        portada = Image.open(instance.portada.pathh)
        portada.save(instance.portada.path, quality=20, optimize=True)


post_save.connect(optimize_image, sender=Libro)
