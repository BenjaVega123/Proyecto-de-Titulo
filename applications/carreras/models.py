from django.db import models
# Create your models here.

class Ramo(models.Model):

    nrcs = models.ManyToManyField(to='horarios.NRC', blank=True)
    nombre = models.CharField(max_length=100,blank=True)
    creditos = models.PositiveIntegerField(blank=True)
    profesores = models.ManyToManyField(to='profesores.Profesor' ,blank=True, related_name='ramos')
    carreras = models.ManyToManyField('Carrera', blank=True, related_name='ramos')
    codigo = models.CharField(max_length=8, blank=True, null=True,unique=True)
    prerrequisito = models.ManyToManyField('self',blank=True)
    correquisito = models.ManyToManyField('self',blank=True)
    semestre = models.IntegerField(blank=True, null=True)


    class Meta:
        """Meta definition for Ramo."""

        verbose_name = 'Ramo'
        verbose_name_plural = 'Ramos'

    def __str__(self):
        return str(self.codigo) + ' ' + str(self.nombre)


class Carrera(models.Model):
    """Model definition for Carrera."""

    # TODO: Define fields here
    nombre = models.CharField(max_length=100)
    semestres_totales = models.PositiveIntegerField()


    class Meta:
        """Meta definition for Carrera."""

        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'

    def __str__(self):
        return str(self.id) + ' ' + str(self.nombre)