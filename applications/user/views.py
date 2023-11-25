from django.contrib.auth import login as login_user
from django.contrib.auth import logout
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormView, View, CreateView, DeleteView, UpdateView
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.user.forms import (LoginForm, RegisterForm)
from applications.user.models import User
from applications.carreras.models import Carrera, Ramo
from applications.horarios.models import NRC, HorarioDeNrcs

class LogoutView(View):
    def get(self, request, *arg, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'home'
            )
        )
    
class LoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login_user(self.request, user)

        return super().form_valid(form)

    def get(self, request, *arg, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().get(request, *arg, **kwargs)
    
class RegisterFormView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            
        )
        return HttpResponseRedirect(
            reverse(
                'login'
            )
        )

class HomeSecretarios(LoginRequiredMixin, TemplateView):
    template_name = "home_secretarios.html"

    def dispatch(self, *args, **kwargs):
        # Verifica el rol del usuario antes de mostrar la página
        if self.request.user.rol != '2':
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)

class CarreraSecListView(ListView):
    model = Carrera
    template_name = "carrera_lista_sec.html"
    context_object_name = 'carreras'

class CarreraUpdateView(UpdateView):
    model = Carrera
    template_name = "carrera_updt_sec.html"
    fields = ('__all__')
    success_url=reverse_lazy('carrera-lista-sec')

class CarreraDeleteView(DeleteView):
    model = Carrera
    template_name = "carrera_del_sec.html"
    success_url=reverse_lazy('carrera-lista-sec')

class CarreraCreateView(CreateView):
    model = Carrera
    template_name = "carrera_create_sec.html"
    fields = ('__all__')
    success_url=reverse_lazy('carrera-lista-sec')

class RamosdeCarreraSec(DetailView):
    model = Carrera
    template_name = "ramos_de_carrera_sec.html"

    def get_context_data(self, **kwargs):
        context = super(RamosdeCarreraSec, self).get_context_data(**kwargs)
        codigo = self.request.GET.get('codigo')
        nombre = self.request.GET.get('nombre')

        # Filtra los ramos por la carrera asociada
        ramos = Ramo.objects.filter(carreras=self.object).order_by('semestre')

        # Aplica los filtros adicionales si se proporcionan
        if codigo:
            ramos = ramos.filter(codigo__icontains=codigo)
        if nombre:
            ramos = ramos.filter(nombre__icontains=nombre)

        context['ramos'] = ramos
        return context

class RamoListView(ListView):
    model = Ramo
    template_name = "ramo_lista_sec.html"
    context_object_name = 'ramos'

    def get_queryset(self):
        codigo = self.request.GET.get('codigo')
        nombre = self.request.GET.get('nombre')
        queryset = Ramo.objects.all().order_by('semestre')

        # Filtra los ramos por semestre si se proporciona
        if codigo:
            queryset = queryset.filter(codigo__icontains=codigo)

        # Filtra los ramos por nombre si se proporciona
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        return queryset

class RamoUpdateView(UpdateView):
    model = Ramo
    template_name = "ramo_updt_sec.html"
    fields = ('__all__')
    success_url = reverse_lazy('ramo-lista-sec')

class RamoDeleteView(DeleteView):
    model = Ramo
    template_name = "ramo_del_sec.html"
    success_url = reverse_lazy('ramo-lista-sec')

class RamoCreateView(CreateView):
    model = Ramo
    template_name = "ramo_create_sec.html"
    fields = ('__all__')
    success_url = reverse_lazy('ramo-lista-sec')

class RamoDetailView(DetailView):
    model = Ramo
    template_name = "nrcs_ramos_sec.html"
    context_object_name = "NRCs"

class NRCListView(ListView):
    model = NRC
    template_name = "nrc_lista_sec.html"
    context_object_name = 'NRCs'

    def get_queryset(self):
        nrc_id = self.request.GET.get('nrc_id')
        docentes = self.request.GET.get('docentes')
        queryset = NRC.objects.all()

        # Filtra los ramos por semestre si se proporciona
        if nrc_id:
            queryset = queryset.filter(nrc_id__icontains=nrc_id)

        # Filtra los ramos por nombre si se proporciona
        if docentes:
            queryset = queryset.filter(docentes__nombres__icontains=docentes)

        return queryset

class NRCUpdateView(UpdateView):
    model = NRC
    template_name = "nrc_updt_sec.html"
    fields = ('__all__')
    success_url = reverse_lazy('nrc-lista-sec')

class NRCDeleteView(DeleteView):
    model = NRC
    template_name = "nrc_del_sec.html"
    success_url = reverse_lazy('nrc-lista-sec')

class NRCCreateView(CreateView):
    model = NRC
    template_name = "nrc_create_sec.html"
    fields = ('__all__')
    success_url = reverse_lazy('nrc-lista-sec')

    def form_valid(self, form):
        # Obtener los datos del formulario
        profesor = form.cleaned_data['docentes']
        horarios_seccion = form.cleaned_data['horarios']

        # Verificar si existe alguna sección con los mismos horarios y profesor
        secciones_existente = NRC.objects.filter(
            docentes=profesor,
            horarios__in=horarios_seccion
        )

        if secciones_existente.exists():
            # Si existe una sección con los mismos horarios y profesor, mostrar un mensaje de error
            form.add_error(None, 'Ya existe un NRC con este profesor y los mismos horarios.')
            return self.form_invalid(form)
        else:
            # Si no hay secciones con los mismos horarios y profesor, guarda el formulario normalmente
            return super().form_valid(form)

class HorarioDeNrcsCreateView(CreateView):
    model = HorarioDeNrcs
    template_name = "horario_create_sec.html"
    fields = ('__all__')
    success_url = reverse_lazy('nrc-lista-sec')

class UserUpdate(UpdateView):
    model = User
    template_name = "user_updt.html"
    fields = ('RUT','first_name','last_name','email','asking_rol','telefono','carrera','username')
    success_url = reverse_lazy('home')

class UserDetailView(DetailView):
    model = User
    template_name = "user_det.html"
    context_object_name = "user"
