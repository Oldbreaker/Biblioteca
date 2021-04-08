from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('libros/', views.ListLibros.as_view(), name='libros'),
    path('libros2/', views.ListLibros2.as_view(), name='libros2'),
    path('libros-detalle/<pk>', views.LibroDetailView.as_view(), name='libro-detalle'),
    path('libros-trg/', views.ListLibrosTgr.as_view(), name='libros-trg'),
]
