from django import forms
from .models import *


class BeneficiarioForm(forms.ModelForm):  # NEF-29
    class Meta:
        model = Beneficiario
        SEXO = [(True, 'Hombre'), (False, 'Mujer')]
        exclude = []

        choices = (('0', 'Ninguna'), ('1', 'Diabetes'), ('2', 'Hipertensión'), ('3', 'Ambas'),)

        widgets = {
            'apellido_paterno':
                forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno':
                forms.TextInput(attrs={'class': 'form-control'}),
            'nombre':
                forms.TextInput(
                    attrs={'class': 'form-control'}),
            'sexo':
                forms.RadioSelect(choices=SEXO,
                                  attrs={'class': 'form-check-input', 'required': 'true'}),
            'fecha_nacimiento':
                forms.DateInput(format='%Y-%m-%d',
                                attrs={'type': 'date', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]*', 'required': True}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]*'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'escolaridad': forms.Select(attrs={'class': 'form-control'}, choices=Beneficiario.ESCOLARIDADES),
            'activo_laboralmente':
                forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nucleo_familiar':
                forms.TextInput(attrs={'class': 'form-control'}),
            'vivienda_propia':
                forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'afroamericano':
                forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_registro':
                forms.DateInput(format='%Y-%m-%d',
                                attrs={'type': 'date',
                                       'class': 'form-control'}),
            'diabetico_hipertenso':
                forms.RadioSelect(choices=choices),
            'nota':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),
            'jornada':
                forms.TextInput(attrs={'class': 'form-control'}),

        }

        labels = {
            'apellido_paterno': 'Apellido paterno',
            'apellido_materno': 'Apellido materno',
            'nombre': 'Nombre',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'telefono': 'Teléfono',
            'celular': 'Celular',
            'correo': 'Correo electrónico',
            'activo_laboralmente': 'Activo laboralmente',
            'nucleo_familiar': 'Núcleo familar',
            'vivienda_propia': 'Vivienda propia',
            'afroamericano': 'Origen afroamericano',
            'fecha_registro': 'Fecha de registro',
            'diabetico_hipertenso': 'Enfermedad crónica',
            'nota': 'Nota',
            'jornada': 'Jornada'
        }


class AntecedentesForm(forms.ModelForm):  # NEF-29

    class Meta(object):

        model = Antecedentes
        exclude = []
        widgets = {
            'enfermedad_cardio_abuelo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_cardio_padre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_cardio_madre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_cardio_hermanos':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hta_abuelo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hta_padre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hta_madre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hta_hermanos':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetes_abuelo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetes_padre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetes_madre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetes_hermanos':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislipidemias_abuelo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislipidemias_padre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislipidemias_madre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislipidemias_hermanos':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obesidad_abuelo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obesidad_padre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obesidad_madre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obesidad_hermanos':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_cerebro_abuelo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_cerebro_padre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_cerebro_madre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_cerebro_hermanos':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_renal_abuelo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_renal_padre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_renal_madre':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_renal_hermanos':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'drogadiccion':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'intervencion_quirurgica':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'intervencion_hospitalaria':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_cardiovascular':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tabaquismo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infeccion_urinaria':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sedentarismo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alcoholismo':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'actividiad_fisica':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'enfermedad_cardio_abuelo': 'Enfermedad cardiovascular abuelo',
            'enfermedad_cardio_padre': 'Enfermedad cardiovascular padre',
            'enfermedad_cardio_madre': 'Enfermedad cardiovascular madre',
            'enfermedad_cardio_hermanos': 'Enfermedad cardiovascular hermanos',
            'hta_abuelo': 'HTA abuelo',
            'hta_padre': 'HTA padre',
            'hta_madre': 'HTA madre',
            'hta_hermanos': 'HTA hermanos',
            'diabetes_abuelo': 'Diabetes abuelo',
            'diabetes_padre': 'Diabetes padre',
            'diabetes_madre': 'Diabetes madre',
            'diabetes_hermanos': 'Diabetes hermanos',
            'dislipidemias_abuelo': 'Dislipidemias abuelo',
            'dislipidemias_padre': 'Dislipidemias padre',
            'dislipidemias_madre': 'Dislipidemias madre',
            'dislipidemias_hermanos': 'Dislipidemias hermanos',
            'obesidad_abuelo': 'Obesidad abuelo',
            'obesidad_padre': 'Obesidad padre',
            'obesidad_madre': 'Obesidad madre',
            'obesidad_hermanos': 'Obesidad hermanos',
            'enfermedad_cerebro_abuelo': 'Enfermedad cerebro abuelo',
            'enfermedad_cerebro_padre': 'Enfermedad cerebro padre',
            'enfermedad_cerebro_madre': 'Enfermedad cerebro madre',
            'enfermedad_cerebro_hermanos': 'Enfermedad cerebro hermanos',
            'enfermedad_renal_abuelo': 'Enfermedad renal abuelo',
            'enfermedad_renal_padre': 'Enfermedad renal padre',
            'enfermedad_renal_madre': 'Enfermedad renal madre',
            'enfermedad_renal_hermanos': 'Enfermedad renal hermanos',
            'drogadiccion': 'Drogadiccion',
            'intervencion_quirurgica': 'Intervencion quirurgica',
            'intervencion_hospitalaria': 'Intervencion hospitalaria',
            'enfermedad_cardiovascular': 'Enfermedad cardiovascular',
            'tabaquismo': 'Tabaquismo',
            'infeccion_urinaria': 'Infeccion urinaria',
            'sedentarismo': 'Sedentarismo',
            'alcoholismo': 'Alcoholismo',
            'actividiad_fisica': 'Actividiad fisica'
        }
