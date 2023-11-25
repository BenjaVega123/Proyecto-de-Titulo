from django.urls import reverse_lazy
from applications.profesores.models import Profesor
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView

# Create your views here.

class ProfesorListView(ListView):
    model = Profesor
    template_name = "prof_lista_sec.html"
    context_object_name = 'profesores'

    def get_queryset(self):
        rut = self.request.GET.get('rut')
        nombres = self.request.GET.get('nombres')
        apellidos = self.request.GET.get('apellidos')
        queryset = Profesor.objects.all()

        if rut:
            queryset = queryset.filter(rut__icontains=rut)
        if nombres:
            queryset = queryset.filter(nombres__icontains=nombres)
        if apellidos:
            queryset = queryset.filter(apellidos__icontains=apellidos)

        return queryset

class ProfesorUpdateView(UpdateView):
    model = Profesor
    template_name = "prof_updt_sec.html"
    fields = ('__all__')
    success_url = reverse_lazy('prof-lista-sec')

class ProfesorDeleteView(DeleteView):
    model = Profesor
    template_name = "prof_del_sec.html"
    success_url = reverse_lazy('prof-lista-sec')

class ProfesorCreateView(CreateView):
    model = Profesor
    template_name = "prof_create_sec.html"
    fields = ('__all__')
    success_url = reverse_lazy('prof-lista-sec')

class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = "prof_det_sec.html"
    context_object_name = 'profesor'