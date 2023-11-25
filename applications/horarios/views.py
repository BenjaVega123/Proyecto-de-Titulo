from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import View, UpdateView
from applications.horarios.models import NRC
from applications.user.models import User


class Calendario(View):
    
    def get(self, request, *args, **kwargs):
        dias_mapping = {
        'Lunes': '1',
        'Martes': '2',
        'Miércoles': '3',
        'Jueves': '4',
        'Viernes': '5',
        'Sábado': '6',
        'Domingo': '0'
        }
        nrcs_actuales = [None]
        if request.user.is_authenticated:
            nrcs_actuales = request.user.nrcs.all()
        eventos = []
        for seccion in nrcs_actuales:
            # Obtiene los horarios asociados a esta sección para el día actual
            horarios_seccion = seccion.horarios.all()
            for horario in horarios_seccion:
                dia_fullcalendar = dias_mapping.get(horario.dia, '')  # Obtener el equivalente en inglés
                eventos.append({
                    'title': str(seccion.ramo_pertenece)+ ' NRC: ' +str(seccion.nrc_id)+ ' Docente: ' +str(seccion.docentes.nombres),
                    'daysOfWeek': [dia_fullcalendar],  # FullCalendar espera una lista de días en inglés
                    'startTime': horario.hora_inicio.strftime('%H:%M'),
                    'endTime': horario.hora_termino.strftime('%H:%M')
                        })

        return JsonResponse(eventos, safe=False)

def mostrar_calendario(request):
    return render(request, 'calendario.html')

def agregar_nrc(request, nrc):
    try:
        nrc_a_agregar = NRC.objects.get(nrc_id=nrc)
        horarios_de_user = [NRC.horarios.all() for NRC in request.user.nrcs.all()]
        for horario in nrc_a_agregar.horarios.all():
            for horario_usuario in horarios_de_user:
                for horario_existente in horario_usuario:
                    if (horario.dia == horario_existente.dia and
                            ((horario.hora_inicio >= horario_existente.hora_inicio and
                              horario.hora_inicio < horario_existente.hora_termino) or
                             (horario.hora_termino > horario_existente.hora_inicio and
                              horario.hora_termino <= horario_existente.hora_termino))):
                        redirect_url = reverse('calendario')
                        return JsonResponse({'message':'Error: El horario de este NRC coincide con otro NRC de tu calendario', 'redirect_url': redirect_url}, status=400)
        
        if nrc_a_agregar in request.user.nrcs.all():
            redirect_url = reverse('calendario')
            return JsonResponse({'message':'ERROR: Ya tienes este NRC agregado', 'redirect_url': redirect_url}, status=400)
        else:
            request.user.nrcs.add(nrc_a_agregar)
            redirect_url = reverse('calendario')
            return JsonResponse({'message': 'NRC agregado exitosamente.', 'redirect_url': redirect_url})
    except NRC.DoesNotExist:
        return JsonResponse({'error': 'NRC no encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
class UserEstudentUpdateView(UpdateView):
    model = User
    template_name = "user_updt_nrcs.html"
    fields = ('nrcs',)
    success_url = reverse_lazy('calendario')

