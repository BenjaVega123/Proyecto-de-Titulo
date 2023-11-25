from django.urls import path
from applications.profesores.views import *

urlpatterns = [
    path('prof-lista-sec/',ProfesorListView.as_view(),name='prof-lista-sec'),
    path('prof-updt-sec/<int:pk>/',ProfesorUpdateView.as_view(),name='prof-updt-sec'),
    path('prof-del-sec/<int:pk>/',ProfesorDeleteView.as_view(),name='prof-del-sec'),
    path('prof-create-sec/',ProfesorCreateView.as_view(),name='prof-create-sec'),
    path('prof-det-sec/<int:pk>/',ProfesorDetailView.as_view(),name='prof-det-sec'),
]