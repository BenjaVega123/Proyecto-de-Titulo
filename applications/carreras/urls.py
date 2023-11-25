from django.urls import path
from applications.carreras.views import *

urlpatterns = [
    path('carreras/',CarreraListView.as_view(),name='lista_carreras'),
    path('ramos/',RamoListView.as_view(),name='lista_ramos'),
    path('ramosdecarrera/<pk>/',RamosdeCarrera.as_view(),name='lista_ramos_carrera'),
    path('',HomeView.as_view(),name='home'),
    path('nrcsderamo/<pk>/',RamoDetailView.as_view(),name='lista_nrcs_ramo'),
    path('ramos/detalles/<pk>/',Ramo2DetailView.as_view(),name='ramo-detalle'),
    path('tyc/',TyC.as_view(),name='tyc')
]