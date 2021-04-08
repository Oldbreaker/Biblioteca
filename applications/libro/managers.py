import datetime
from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Count
from django.contrib.postgres.search import TrigramSimilarity


class LibroManager(models.Manager):
    # manager para el modelo Autor
    def listar_libros(self, kword):
        resultado = self.filter(
            titulo__icontains=kword,
            fecha__range=('2000-01-01', '2020-12-30')
        )
        return resultado

    def listar_libros2(self, kword, fecha1, fecha2):
        date1 = datetime.datetime.strptime(fecha1, "%Y-%m-%d")
        date2 = datetime.datetime.strptime(fecha2, "%Y-%m-%d")
        resultado = self.filter(
            titulo__icontains=kword,
            fecha__range=(date1, date2)
        ).order_by('fecha')
        return resultado

    def listar_libros_categoria(self, categoria):
        return self.filter(categoria__id=categoria).order_by('titulo')

    def add_autor_libro(self, libro_id, autor):
        libro = self.get(id=libro_id)
        libro.autor.add(autor)
        return libro

    def libros_num_prestamos(self):
        resultado = self.aggregate(
            num_prestamos=Count('libro_prestamo')
        )
        return resultado

    def listar_libros_trg(self, kword):
        if kword:
            resultado = self.filter(
                titulo__trigram_similar=kword,
            )
            return resultado
        else:
            return self.all()[:10]


class CategoriaManager(models.Manager):
    """ managers para el mopdelo autor"""

    def categoria_por_autor(self, autor):
        return self.filter(categoria_libro__autor__id=autor).distinct()

    def listar_categoria_libros(self):
        resultado = self.annotate(
            num_libros=Count("categoria_libro")
        )
        for r in resultado:
            print('*************')
            print(r, r.num_libros)
        return resultado
