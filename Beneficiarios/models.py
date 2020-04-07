from django.db import models
from django.utils import timezone
from datetime import date
from Proyectos.models import *


class Beneficiario(models.Model):  # NEF-29
    NINGUNA = 'NO'
    PRIMARIA_TRUNCA = 'PRIT'
    PRIMARIA_TERMINADA = 'PRI'
    SECUNDARIA_TRUNCA = 'SECT'
    SECUNDARIA_TERMINADA = 'SEC'
    PREPARATORIA_TRUNCA = 'PRET'
    PREPARATORIA_TERMINADA = 'PRE'
    LICENCIATURA_TRUNCA = 'LICT'
    LICENCIATURA_TERMINADA = 'LIC'
    POSGRADO = 'POS'

    ESCOLARIDADES = (
        (NINGUNA, 'Ninguna'),
        (PRIMARIA_TRUNCA, 'Primaria trunca'),
        (PRIMARIA_TERMINADA, 'Primaria terminada'),
        (SECUNDARIA_TRUNCA, 'Secundaria trunca'),
        (SECUNDARIA_TERMINADA, 'Secundaria terminada'),
        (PREPARATORIA_TRUNCA, 'Preparatoria trunca'),
        (PREPARATORIA_TERMINADA, 'Preparatoria terminada'),
        (LICENCIATURA_TRUNCA, 'Licenciatura trunca'),
        (LICENCIATURA_TERMINADA, 'Licenciatura terminada'),
        (POSGRADO, 'Posgrado'),
    )

    NINGUNA_ENF = 0
    DIABETES = 1
    HIPERTENSION = 2
    AMBAS = 3

    ENFERMEDADES = (
        (NINGUNA_ENF, 'Ni diabetes ni hipertensión'),
        (DIABETES, 'Diabetes'),
        (HIPERTENSION, 'Hipertensión'),
        (AMBAS, 'Diabetes e hipertensión'),
    )

    fecha_registro = models.DateTimeField(default=timezone.now)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(blank=True, max_length=255)
    nombre = models.CharField(max_length=255)
    sexo = models.BooleanField()
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(blank=True, max_length=10)
    celular = models.CharField(blank=True, max_length=10)
    correo = models.EmailField(blank=True, max_length=255)
    activo_laboralmente = models.BooleanField(default=False)
    nucleo_familiar = models.CharField(blank=True, max_length=255)
    vivienda_propia = models.BooleanField(default=False)
    afroamericano = models.BooleanField(default=False)
    escolaridad = models.CharField(max_length=4, choices=ESCOLARIDADES,
                                   default=NINGUNA)
    diabetico_hipertenso = models.IntegerField(default=0)
    nota = models.CharField(max_length=255, blank=True, null=True)
    jornada = models.ForeignKey(Jornada, on_delete=models.PROTECT, null=True)
    edad_inicial = models.IntegerField(blank=True, null=True)
    de_seguimiento = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    causa_baja = models.TextField(blank=True, null=True,max_length=6000)

    @property
    def edad(self):
        today = date.today()
        born = self.fecha_nacimiento
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @property
    def edad_ini(self):
        today = self.fecha_registro
        born = self.fecha_nacimiento
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @property
    def escuela(self):
        nombre = dict(self.ESCOLARIDADES)
        return nombre[self.escolaridad]

    @property
    def enfermedad(self):
        enf = dict(self.ENFERMEDADES)
        return enf[self.diabetico_hipertenso]

    def save(self, *args, **kwargs):
        self.edad_inicial = self.edad_ini
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre + " " + self.apellido_paterno


class Antecedentes(models.Model):
    beneficiario = models.OneToOneField(Beneficiario, on_delete=models.CASCADE, primary_key=True,)
    enfermedad_cardio_abuelo = models.BooleanField(default=False)
    enfermedad_cardio_padre = models.BooleanField(default=False)
    enfermedad_cardio_madre = models.BooleanField(default=False)
    enfermedad_cardio_hermanos = models.BooleanField(default=False)
    hta_abuelo = models.BooleanField(default=False)
    hta_padre = models.BooleanField(default=False)
    hta_madre = models.BooleanField(default=False)
    hta_hermanos = models.BooleanField(default=False)
    diabetes_abuelo = models.BooleanField(default=False)
    diabetes_padre = models.BooleanField(default=False)
    diabetes_madre = models.BooleanField(default=False)
    diabetes_hermanos = models.BooleanField(default=False)
    dislipidemias_abuelo = models.BooleanField(default=False)
    dislipidemias_padre = models.BooleanField(default=False)
    dislipidemias_madre = models.BooleanField(default=False)
    dislipidemias_hermanos = models.BooleanField(default=False)
    obesidad_abuelo = models.BooleanField(default=False)
    obesidad_padre = models.BooleanField(default=False)
    obesidad_madre = models.BooleanField(default=False)
    obesidad_hermanos = models.BooleanField(default=False)
    enfermedad_cerebro_abuelo = models.BooleanField(default=False)
    enfermedad_cerebro_padre = models.BooleanField(default=False)
    enfermedad_cerebro_madre = models.BooleanField(default=False)
    enfermedad_cerebro_hermanos = models.BooleanField(default=False)
    enfermedad_renal_abuelo = models.BooleanField(default=False)
    enfermedad_renal_padre = models.BooleanField(default=False)
    enfermedad_renal_madre = models.BooleanField(default=False)
    enfermedad_renal_hermanos = models.BooleanField(default=False)
    drogadiccion = models.BooleanField(default=False)
    intervencion_quirurgica = models.BooleanField(default=False)
    intervencion_hospitalaria = models.BooleanField(default=False)
    enfermedad_cardiovascular = models.BooleanField(default=False)
    tabaquismo = models.BooleanField(default=False)
    infeccion_urinaria = models.BooleanField(default=False)
    sedentarismo = models.BooleanField(default=False)
    alcoholismo = models.BooleanField(default=False)
    actividiad_fisica = models.BooleanField(default=False)
