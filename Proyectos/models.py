from django.db import models
import datetime


class Jornada(models.Model):  # NEF-21
    nombre = models.CharField(max_length=255, null=False)
    fecha = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=255, null=False)
    municipio = models.CharField(max_length=255, null=False)
    localidad = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "Jornada - " + str(self.nombre)
