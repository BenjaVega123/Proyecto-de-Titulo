from django.db import models
from applications.profesores.models import Profesor
# Create your models here.

class HorarioDeNrcs(models.Model):
    """Model definition for MODELNAME."""

    # TODO: Define fields here
    DIA_CHOICES = (
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    )
    
    dia = models.CharField(max_length=10, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
    
    def __str__(self):
        return str(self.dia) + ' de ' + str(self.hora_inicio) + ' a ' + str(self.hora_termino)



class NRC(models.Model):
    ramo_pertenece = models.ForeignKey(to='carreras.Ramo',on_delete=models.CASCADE)
    nrc_id = models.IntegerField(unique=True, blank=True, null=True)
    horarios = models.ManyToManyField(HorarioDeNrcs, blank=True)
    docentes = models.ForeignKey(Profesor,on_delete=models.CASCADE,null=True, related_name='secciones')

    def save(self, *args, **kwargs):
        # Asocia la sección con el ramo al que pertenece
        super(NRC, self).save(*args, **kwargs)
        self.ramo_pertenece.nrcs.add(self)
        
    def __str__(self):
        return str(self.nrc_id) + ' ' + str(self.ramo_pertenece)