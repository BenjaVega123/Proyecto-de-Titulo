from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):

    ROLES = (
        ('1', 'Admin'),
        ('2', 'Secretario'),
        ('3', 'Estudiante'),
    )

    def validar_rut(value):
        rut = value.upper()
        rut = rut.replace(".", "")
        rut = rut.replace("-", "")

        rut_numero = rut[:-1]
        dv_ingresado = rut[-1]

        suma = 0
        multiplicador = 2
        for i in range(len(rut_numero)-1, -1, -1):
            suma += int(rut_numero[i]) * multiplicador
            multiplicador += 1
            if multiplicador == 8:
                multiplicador = 2

        resto = suma % 11
        digito_verificador = 11 - resto
        if digito_verificador == 10:
            digito_verificador = 'K'
        elif digito_verificador == 11:
            digito_verificador = '0'

        if str(digito_verificador) != dv_ingresado:
            raise ValidationError("El RUT ingresado no es válido.")

    RUT = models.CharField(max_length=50,null=True,blank=True,unique=True, validators=[validar_rut])
    asking_rol = models.CharField(max_length=50, choices=ROLES, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES,null=True,blank=True)
    telefono = models.CharField(max_length=12,null=True,blank=True)
    carrera = models.CharField(max_length=50, null=True,blank=True)
    nrcs = models.ManyToManyField(to='horarios.NRC', blank=True, related_name='user')
    
    about = models.TextField(max_length=280,null=True,blank=True)
    class Meta:
        """Meta definition for User."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.id) + ' ' + self.username
