from django import forms
from django.utils import timezone
from .models import *
from django.core.exceptions import ValidationError
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class FormularioForm(forms.ModelForm):  # NEF-70
    class Meta:
        model = Formulario

        fields = '__all__'

        PERIODO = [(True, 'Finalización'), (False, 'Inicio')]

        choices_2 = ((1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (-1, 'E'))
        choices_3 = ((-1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'))
        choices_4 = ((1, 'A'), (-1, 'B'), (3, 'C'), (4, 'D'), (5, 'E'))
        choices_5 = ((1, 'A'), (2, 'B'), (-1, 'C'), (4, 'D'), (5, 'E'))
        choices_6 = ((1, 'A'), (2, 'B'), (3, 'C'), (-1, 'D'))
        choices_7 = ((1, 'A'), (2, 'B'), (3, 'C'), (-1, 'D'))
        choices_8 = ((1, 'A'), (-1, 'B'), (3, 'C'))
        choices_9 = ((1, 'A'), (-1, 'B'), (3, 'C'))
        choices_10 = ((1, 'A'), (2, 'B'), (-1, 'C'))
        choices_11 = ((1, 'A'), (2, 'B'), (-1, 'C'))
        choices_12 = ((1, 'A'), (-1, 'B'), (3, 'C'))
        choices_13 = ((-1, 'A'), (2, 'B'), (3, 'C'))
        choices_14 = ((1, 'A'), (2, 'B'), (-1, 'C'))
        choices_15 = ((-1, 'A'), (2, 'B'), (3, 'C'))
        choices_16 = ((-1, 'A'), (2, 'B'), (3, 'C'))
        choices_17 = ((1, 'A'), (2, 'B'), (-1, 'C'))
        choices_18 = ((1, 'A'), (2, 'B'), (-1, 'C'))
        choices_19 = ((1, 'A'), (-1, 'B'), (3, 'C'))
        choices_20 = ((-1, 'A'), (2, 'B'), (3, 'C'))

        widgets = {
            'periodo':
                forms.RadioSelect(choices=PERIODO,
                                  attrs={'class': 'form-check-input', 'required': 'true'}),
            'p2': forms.RadioSelect(choices=choices_2),
            'p3': forms.RadioSelect(choices=choices_3),
            'p4': forms.RadioSelect(choices=choices_4),
            'p5': forms.RadioSelect(choices=choices_5),
            'p6': forms.RadioSelect(choices=choices_6),
            'p7': forms.RadioSelect(choices=choices_7),
            'p8': forms.RadioSelect(choices=choices_8),
            'p9': forms.RadioSelect(choices=choices_9),
            'p10': forms.RadioSelect(choices=choices_10),
            'p11': forms.RadioSelect(choices=choices_11),
            'p12': forms.RadioSelect(choices=choices_12),
            'p13': forms.RadioSelect(choices=choices_13),
            'p14': forms.RadioSelect(choices=choices_14),
            'p15': forms.RadioSelect(choices=choices_15),
            'p16': forms.RadioSelect(choices=choices_16),
            'p17': forms.RadioSelect(choices=choices_17),
            'p18': forms.RadioSelect(choices=choices_18),
            'p19': forms.RadioSelect(choices=choices_19),
            'p20': forms.RadioSelect(choices=choices_20),
        }

        labels = {
            'p1': 'Número de personas diabéticas e hipertensas que atiende usted mensualmente',
            'p2': '¿Cuáles son las metas de tratamiento de la nefropatía diabética?',
            'p3': '¿Qué porcentaje de pacientes con Hipertensión Arterial se estima presenta Nefropatía Hipertensiva como causa de Enfermedad Renal Crónica?',
            'p4': 'Por lo general, la mortalidad anual ajustada de los pacientes que dependen de hemodiálisis tiende a ser',
            'p5': '¿Cuál de las siguientes es la causa principal de muerte en los pacientes que dependen de diálisis?',
            'p6': 'Cuando se sospecha de un daño del riñón, ¿cuáles estudios debe realizarse el paciente?',
            'p7': 'Cuales enfermedades conllevan a enfermedad renal crónica de manera más frecuente',
            'p8': 'En qué momento debe ser derivado un paciente con disminución de la función renal al Nefrólogo',
            'p9': 'Porque es importante ajustar las dosis de medicamentos en la ERC',
            'p10': 'En relación al paciente Urémico cual es la opción correcta',
            'p11': '¿Qué es un trasplante renal?',
            'p12': '¿Qué cantidad de proteína que se recomienda para pacientes sin terapia sustitutiva?',
            'p13': '¿Qué cantidad de proteína que se recomienda para pacientes en diálisis peritoneal?',
            'p14': '¿Qué cantidad de proteína que se recomienda para pacientes en hemodiálisis?',
            'p15': 'Las fuentes de qué elementos se deben cuidar en el paciente con enfermedad renal',
            'p16': 'La recomendación de la cantidad de líquido que debe tomar un paciente con ERC es',
            'p17': '¿Cuáles son las razones psicológicas que hacen que las personas con ERC no se adhieran al tratamiento?',
            'p18': '¿Qué entendemos por "dar malas noticias"?',
            'p19': '¿Cuáles son los dos principios que el equipo médico necesita identificar para proporcionar información?',
            'p20': 'Mencione 5 barreras de la comunicación en la relación médico-paciente',
        }


class EvaluacionForm(forms.ModelForm):  # NEF-21
    class Meta:
        model = Evaluacion
        exclude = []
        fields = [
            'nombre',
            'fecha',
        ]
        widgets = {
            'nombre':
                forms.TextInput(attrs={'class': 'form-control'}),
            'fecha':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }

        labels = {
            'nombre': 'Nombre de la evaluacion',
            'fecha': 'Fecha de inicio de la evaluacion',
        }
