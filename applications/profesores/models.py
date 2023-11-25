from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Profesor(models.Model):
    """Model definition for Profesor."""

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

    # TODO: Define fields here
    rut = models.CharField(max_length=100,unique=True,blank=True,validators=[validar_rut])
    nombres = models.CharField(blank=True, max_length=50)
    apellidos = models.CharField(blank=True, max_length=50)

    class Meta:
        """Meta definition for Profesor."""

        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'

    def __str__(self):
        return str(self.rut) + ' ' + str(self.nombres)

