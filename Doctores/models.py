from django.db import models
from django.core.validators import *
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
import uuid



# Create your models here.

class Evaluacion(models.Model):
    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'

    nombre = models.CharField(max_length=255)
    fecha = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.nombre + str(self.fecha)


class Formulario(models.Model):
    class Meta:
        verbose_name = 'Capacitación'
        verbose_name_plural = 'Capacitaciones'
    labels = {
        'p1': 'Número de personas diabéticas e hipertensas que atiende usted mensualmente: ',
        'p2': '¿Cuáles son las metas de tratamiento de la nefropatía diabética?',
        'p3': '¿Qué porcentaje de pacientes con Hipertensión Arterial se estima presenta Nefropatía Hipertensiva como causa de Enfermedad Renal Crónica?',
        'p4': 'Por lo general, la mortalidad anual ajustada de los pacientes que dependen de hemodiálisis tiende a ser:',
        'p5': '¿Cuál de las siguientes es la causa principal de muerte en los pacientes que dependen de diálisis?',
        'p6': 'Cuando se sospecha de un daño del riñón, ¿cuáles estudios debe realizarse el paciente?',
        'p7': 'Cuales enfermedades conllevan a enfermedad renal crónica de manera más frecuente:',
        'p8': 'En qué momento debe ser derivado un paciente con disminución de la función renal al Nefrólogo: ',
        'p9': 'Porque es importante ajustar las dosis de medicamentos en la ERC: ',
        'p10': 'En relación al paciente Urémico cual es la opción correcta',
        'p11': '¿Qué es un trasplante renal?',
        'p12': '¿Qué cantidad de proteína que se recomienda para pacientes sin terapia sustitutiva? ',
        'p13': '¿Qué cantidad de proteína que se recomienda para pacientes en diálisis peritoneal?',
        'p14': '¿Qué cantidad de proteína que se recomienda para pacientes en hemodiálisis?',
        'p15': 'Las fuentes de qué elementos se deben cuidar en el paciente con enfermedad renal:',
        'p16': 'La recomendación de la cantidad de líquido que debe tomar un paciente con ERC es: ',
        'p17': '¿Cuáles son las razones psicológicas que hacen que las personas con ERC no se adhieran al tratamiento?',
        'p18': '¿Qué entendemos por "dar malas noticias"?',
        'p19': '¿Cuáles son los dos principios que el equipo médico necesita identificar para proporcionar información?',
        'p20': 'Mencione 5 barreras de la comunicación en la relación médico-paciente',
    }

    choices_2 = {1: 'A', 2: 'B', 3: 'C', 4: 'D', -1: 'E'}#
    choices_3 = {-1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}#
    choices_4 = {1: 'A', -1: 'B', 3: 'C', 4: 'D', 5: 'E'}#
    choices_5 = {1: 'A', 2: 'B', -1: 'C', 4: 'D', 5: 'E'}#
    choices_6 = {1: 'A', 2: 'B', 3: 'C', -1: 'D'}#
    choices_7 = {1: 'A', 2: 'B', 3: 'C', -1: 'D'}#
    choices_8 = {1: 'A', -1: 'B', 3: 'C'}#
    choices_9 = {1: 'A', -1: 'B', 3: 'C'}#
    choices_10 = {1: 'A', 2: 'B', -1: 'C'}#
    choices_11 = {1: 'A', 2: 'B', -1: 'C'}
    choices_12 = {1: 'A', -1: 'B', 3: 'C'}
    choices_13 = {-1: 'A', 2: 'B', 3: 'C'}
    choices_14 = {1: 'A', 2: 'B', -1: 'C'}
    choices_15 = {-1: 'A', 2: 'B', 3: 'C'}
    choices_16 = {-1: 'A', 2: 'B', 3: 'C'}
    choices_17 = {1: 'A', 2: 'B', -1: 'C'}
    choices_18 = {1: 'A', 2: 'B', -1: 'C'}#
    choices_19 = {1: 'A', -1: 'B', 3: 'C'}#
    choices_20 = {-1: 'A', 2: 'B', 3: 'C'}#


    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    periodo = models.BooleanField(default=False)
    p1 = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    p2 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p3 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p4 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p5 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p6 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p7 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p8 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p9 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p10 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p11 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p12 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p13 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p14 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p15 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p16 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p17 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p18 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p19 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)
    p20 = models.IntegerField(validators=[MaxValueValidator(9)], default=-1)

    def __str__(self):
        return str(self.evaluacion) + str(self.id)
