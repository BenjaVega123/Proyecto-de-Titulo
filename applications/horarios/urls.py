from django.urls import path
from applications.horarios.views import *

urlpatterns = [
    path('obtener-calendario/',Calendario.as_view(),name='obtener-calendario'),
    path('calendario/',mostrar_calendario,name='calendario'),
    path('agregar-nrc/<int:nrc>/',agregar_nrc,name='agregar-nrc'),
    path('user-updt-nrcs/<int:pk>/',UserEstudentUpdateView.as_view(),name='user-updt-nrcs')
]