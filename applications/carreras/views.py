from django.shortcuts import render
from applications.carreras.models import *
from applications.horarios.models import *
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

class CarreraListView(ListView):
    model = Carrera
    template_name = "carreras_lista.html"
    context_object_name = 'carreras'

class RamoListView(ListView):
    model = Ramo
    template_name = "ramos_lista.html"
    context_object_name = 'ramos'

    def get_queryset(self):
        semestre = self.request.GET.get('semestre')
        nombre = self.request.GET.get('nombre')
        queryset = Ramo.objects.all().order_by('semestre')

        # Filtra los ramos por semestre si se proporciona
        if semestre:
            queryset = queryset.filter(semestre=semestre)

        # Filtra los ramos por nombre si se proporciona
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        return queryset

class RamosdeCarrera(DetailView):
    model = Carrera
    template_name = "ramos_de_carrera.html"
    context_object_name = "carrera"

    def get_context_data(self, **kwargs):
        context = super(RamosdeCarrera, self).get_context_data(**kwargs)
        semestre = self.request.GET.get('semestre')
        nombre = self.request.GET.get('nombre')

        # Filtra los ramos por la carrera asociada
        ramos = Ramo.objects.filter(carreras=self.object).order_by('semestre')

        # Aplica los filtros adicionales si se proporcionan
        if semestre:
            ramos = ramos.filter(semestre=semestre)
        if nombre:
            ramos = ramos.filter(nombre__icontains=nombre)

        context['ramos'] = ramos
        return context

class HomeView(TemplateView):
    template_name = "home.html"

class RamoDetailView(DetailView):
    model = Ramo
    template_name = "NRCS_DE_RAMOS.html"
    context_object_name = "NRCs"

class Ramo2DetailView(DetailView):
    model = Ramo
    template_name = "ramos_detalles.html"
    context_object_name = 'ramo'

class TyC(TemplateView):
    template_name = "TyC.html"
