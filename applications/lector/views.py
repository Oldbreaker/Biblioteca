from datetime import date
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView

from .models import Prestamo
from .forms import PrestamoForm, MultiplePrestamoForm
# Create your views here.


class RegistrarPrestamo(FormView):
    template_name = 'lector/add_prestamo.html'
    form_class = PrestamoForm
    success_url = '.'

    def form_valid(self, form):
        # creando un objeto pero usando una instancia create
        Prestamo.objects.create(
            lector=form.cleaned_data['lector'],
            libro=form.cleaned_data['libro'],
            prestamo=date.today(),
            devuelto=False
        )
        libro = form.cleaned_data['libro']
        libro.stock = libro.stock - 1
        libro.save()
        # creando un objeto para el save de la información
        # prestamo=Prestamo(
        #     lector=form.cleaned_data['lector'],
        #     libro=form.cleaned_data['libro'],
        #     fecha_prestamo=date.today(),
        #     devuelto=False
        # )
        # prestamo.save()

        return super(RegistrarPrestamo, self).form_valid(form)


class AddPrestamo(FormView):
    template_name = 'lector/add_prestamo.html'
    form_class = PrestamoForm
    success_url = '.'

    def form_valid(self, form):
        obj, created = Prestamo.objects.get_or_create(
            lector=form.cleaned_data['lector'],
            libro=form.cleaned_data['libro'],
            devuelto=False,
            defaults={
                'prestamo': date.today()
            }
        )
        if created:
            return super(AddPrestamo, self).form_valid(form)
        else:
            return HttpResponseRedirect('/')


class AddMultiplePrestamo(FormView):
    template_name = 'lector/add_multiple_prestamo.html'
    form_class = MultiplePrestamoForm
    success_url = '.'

    def form_valid(self, form):
        prestamos = []
        for l in form.cleaned_data['libros']:
            prestamo = Prestamo(
                lector=form.cleaned_data['lector'],
                libro=form.cleaned_data['libro'],
                fecha_prestamo=date.today(),
                devuelto=False
            )
            prestamos.append(prestamo)
        Prestamo.objects.bulk_create(
            prestamos
        )
        return super(AddMultiplePrestamo, self).form_valid(form)
