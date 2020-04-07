from django import forms
from django.utils import timezone
from .models import *
from django.core.exceptions import ValidationError
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class JornadaForm(forms.ModelForm):  # NEF-21
    class Meta:
        model = Jornada
        exclude = []
        fields = [
            'nombre',
            'fecha',
            'estado',
            'municipio',
            'localidad',
        ]
        widgets = {
            'nombre':
                forms.TextInput(attrs={'class': 'form-control'}),
            'estado':
                forms.TextInput(attrs={'class': 'form-control'}),
            'municipio':
                forms.TextInput(attrs={'class': 'form-control'}),
            'localidad':
                forms.TextInput(attrs={'class': 'form-control'}),
            'fecha':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }

        labels = {
            'nombre': 'Nombre de la jornada',
            'fecha': 'Fecha de inicio de la jornada',
            'estado': 'Estado',
            'municipio': 'Municipio',
            'localidad': 'Localidad',
        }
