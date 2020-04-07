from django import forms
from django.utils import timezone
from .models import *
from django.core.exceptions import ValidationError
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class EvidenciaForm(forms.ModelForm):  # NEF-99
    class Meta:
        model = Evidencia
        tipo = forms.CharField()
        size = forms.IntegerField(validators=[MinValueValidator(1)])
        exclude = ['urn', 'fecha_creacion', 'fecha_subida', 'existe', 'usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                                 'placeholder': 'Ingresa una descripción...'}),
        }

        labels = {
            'nombre': 'Nombre de la evidencia:',
            'descripcion': 'Descripción:'
        }


class QuimicaSanguineaForm(forms.ModelForm):  # NEF-66
    class Meta:
        model = QuimicaSanguinea
        exclude = []
        fields = [
            'beneficiario',
            'fecha',
            'doctor',
            'metodo',

            'glucosa',
            'max_glucosa',
            'min_glucosa',
            'comentario_glucosa',

            'urea',
            'max_urea',
            'min_urea',
            'comentario_urea',

            'bun',
            'max_bun',
            'min_bun',
            'comentario_bun',

            'creatinina',
            'max_creatinina_h',
            'min_creatinina_h',
            'max_creatinina_m',
            'min_creatinina_m',
            'comentario_creatinina',

            'acido_urico',
            'max_acido_urico_h',
            'min_acido_urico_h',
            'max_acido_urico_m',
            'min_acido_urico_m',
            'comentario_acido_urico'
        ]
        widgets = {
            'fecha':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'doctor':
                forms.TextInput(attrs={'class': 'form-control'}),
            'metodo':
                forms.TextInput(attrs={'class': 'form-control'}),

            'glucosa':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'max_glucosa':
                forms.NumberInput(attrs={'class': 'form-control maximo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'min_glucosa':
                forms.NumberInput(attrs={'class': 'form-control minimo ',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'comentario_glucosa':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),

            'urea':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'max_urea':
                forms.NumberInput(attrs={'class': 'form-control  maximo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'min_urea':
                forms.NumberInput(attrs={'class': 'form-control minimo ',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'comentario_urea':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),

            'bun':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'max_bun':
                forms.NumberInput(attrs={'class': 'form-control maximo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'min_bun':
                forms.NumberInput(attrs={'class': 'form-control minimo ',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'comentario_bun':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),

            'creatinina':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'max_creatinina_h':
                forms.NumberInput(attrs={'class': 'form-control  maximo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'min_creatinina_h':
                forms.NumberInput(attrs={'class': 'form-control minimo ',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'max_creatinina_m':
                forms.NumberInput(attrs={'class': 'form-control maximo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'min_creatinina_m':
                forms.NumberInput(attrs={'class': 'form-control minimo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'comentario_creatinina':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),
            'acido_urico':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'max_acido_urico_h':
                forms.NumberInput(attrs={'class': 'form-control  maximo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'min_acido_urico_h':
                forms.NumberInput(attrs={'class': 'form-control minimo ',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'max_acido_urico_m':
                forms.NumberInput(attrs={'class': 'form-control maximo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'min_acido_urico_m':
                forms.NumberInput(attrs={'class': 'form-control minimo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'comentario_acido_urico':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),
        }
        labels = {
            'fecha': 'Fecha del estudio:',
            'doctor': 'Doctor:',
            'metodo': 'Método:',

            'glucosa': 'Glucosa:',
            'max_glucosa': 'Max:',
            'min_glucosa': 'Min:',
            'comentario_glucosa': 'Comentario:',

            'urea': 'Urea:',
            'max_urea': 'Max:',
            'min_urea': 'Min:',
            'comentario_urea': 'Comentario:',

            'bun': 'Bun:',
            'max_bun': 'Max:',
            'min_bun': 'Min:',
            'comentario_bun': 'Comentario:',

            'creatinina': 'Creatinina:',
            'max_creatinina_h': 'Max:',
            'min_creatinina_h': 'Min:',
            'max_creatinina_m': 'Max:',
            'min_creatinina_m': 'Min:',
            'comentario_creatinina': 'Comentario:',

            'acido_urico': 'Ácido Úrico:',
            'max_acido_urico_h': 'Max:',
            'min_acido_urico_h': 'Min:',
            'max_acido_urico_m': 'Max:',
            'min_acido_urico_m': 'Min:',
            'comentario_acido_urico': 'Comentario:',
        }


class MicroalbuminuriaForm(forms.ModelForm):  # NEF-74
    class Meta:
        model = Microalbuminuria
        fields = [
            'beneficiario',
            'fecha',
            'metodo',
            'doctor',
            'micro_albumina',
            'micro_albumina_min',
            'micro_albumina_max',
            'micro_albumina_comentario',
            'creatinina',
            'creatinina_min',
            'creatinina_max',
            'creatinina_comentario',
            'relacion',
            'relacion_normal_min',
            'relacion_normal_max',
            'relacion_anormal_min',
            'relacion_anormal_max',
            'relacion_anormal_alta_min',
            'relacion_anormal_alta_max'
        ]
        widgets = {
            'fecha':
                forms.DateInput(format='%Y-%m-%d',
                                attrs={'type': 'date', 'class':
                                       'form-control'}),
            'metodo':
                forms.TextInput({"class": "form-control",
                                 "oninput": "this.className"}),
            'doctor':
                forms.TextInput({"class": "form-control",
                                 "oninput": "this.className"}),
            'micro_albumina':
                forms.NumberInput({"class": "form-control",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'micro_albumina_min':
                forms.NumberInput({"class": "form-control minimo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'micro_albumina_max':
                forms.NumberInput({"class": "form-control maximo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'micro_albumina_comentario':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class':
                                      'form-control',
                                      'placeholder':
                                          'Ingresa un comentario...'}),
            'creatinina':
                forms.NumberInput({"class": "form-control",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'creatinina_min':
                forms.NumberInput({"class": "form-control minimo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'creatinina_max':
                forms.NumberInput({"class": "form-control maximo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'creatinina_comentario':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class':
                                      'form-control',
                                      'placeholder':
                                          'Ingresa un comentario...'}),
            'relacion':
                forms.NumberInput({"class": "form-control",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'relacion_normal_min':
                forms.NumberInput({"class": "form-control minimo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'relacion_normal_max':
                forms.NumberInput({"class": "form-control maximo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'relacion_anormal_min':
                forms.NumberInput({"class": "form-control minimo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'relacion_anormal_max':
                forms.NumberInput({"class": "form-control maximo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'relacion_anormal_alta_min':
                forms.NumberInput({"class": "form-control minimo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
            'relacion_anormal_alta_max':
                forms.NumberInput({"class": "form-control maximo",
                                   "oninput": "this.className",
                                   "min": "0", "max": "999"}),
        }
        labels = {
            'fecha': "Fecha",
            'metodo': "Método",
            'doctor': "Doctor",
            'micro_albumina': "Micro Albúmina",
            'creatinina': "Creatinina",
            'relacion': "Relación Micro Albúmina - Creatinina",
            'relacion_normal_min': 'Relación normal - valor mínimo',
            'relacion_normal_max': 'Relación normal - valor máximo',
            'relacion_anormal_min': 'Relación anormal - valor mínimo',
            'relacion_anormal_max': 'Relación anormal - valor máximo',
            'relacion_anormal_alta_min': 'Relación anormal alta - valor mínimo',
            'relacion_anormal_alta_max': 'Relación anormal alta - valor máximo',
        }


class HemoglobinaGlucosiladaForm(forms.ModelForm):  # NEF-70
    class Meta:
        model = HemoglobinaGlucosilada
        fields = [
            'beneficiario',
            'fecha_captura',
            'metodo',
            'doctor',
            'comentario',
            'hemoglobina_glucosilada',
            'max_no_diabetico',
            'min_no_diabetico',
            'max_diabetico_cont',
            'min_diabetico_cont',
            'max_diabetico_no_cont',
            'min_diabetico_no_cont',
        ]
        widgets = {
            'fecha_captura':
                forms.DateInput(format='%Y-%m-%d',
                                attrs={'type': 'date',
                                       'class': 'form-control'}),
            'metodo':
                forms.TextInput({"class": "form-control",
                                 "oninput": "this.className"}),
            'doctor':
                forms.TextInput({"class": "form-control",
                                 "oninput": "this.className"}),
            'comentario':
                forms.Textarea(attrs={'required': False, 'rows': '2',
                                      'class': 'form-control',
                                      'placeholder':
                                          'Ingresa un comentario...'}),
            'hemoglobina_glucosilada':
                forms.NumberInput({"class": "form-control",
                                   "oninput": "this.className",
                                   "max": "100"}),
            'max_no_diabetico':
                forms.NumberInput({"class": "form-control maximo",
                                   "oninput": "this.className",
                                   "min": "0",
                                   "max": "100",
                                   "value": 5.1}),
            'min_no_diabetico':
                forms.NumberInput({"class": "form-control minimo",
                                   "oninput": "this.className",
                                   "min": "0",
                                   "max": "100",
                                   "value": 4.0}),
            'max_diabetico_cont':
                forms.NumberInput({"class": "form-control maximo",
                                   "oninput": "this.className",
                                   "min": "0",
                                   "max": "100",
                                   "value": 7.0}),
            'min_diabetico_cont':
                forms.NumberInput({"class": "form-control minimo",
                                   "oninput": "this.className",
                                   "min": "0",
                                   "max": "100",
                                   "value": 5.2}),
            'max_diabetico_no_cont':
                forms.NumberInput({"class": "form-control maximo",
                                   "oninput": "this.className",
                                   "min": "0",
                                   "max": "100",
                                   "value": 9.0}),
            'min_diabetico_no_cont':
                forms.NumberInput({"class": "form-control minimo",
                                   "oninput": "this.className",
                                   "min": "0",
                                   "max": "100",
                                   "value": 7.1})
        }

        labels = {
            'beneficiario': 'Beneficiario',
            'fecha_captura': 'Fecha de captura',
            'metodo': 'Método',
            'doctor': 'Médico',
            'comentario': 'Comentarios',
            'hemoglobina_glucosilada': 'Resultado Hemoglobina Glucosilada',
            'max_no_diabetico': 'Máximo no diabético',
            'min_no_diabetico': 'Mínimo no diabético',
            'max_diabetico_cont': 'Máximo diabético controlado',
            'min_diabetico_cont': 'Mínimo diabético controlado',
            'max_diabetico_no_cont': 'Máximo diabético descontrolado',
            'min_diabetico_no_cont': 'Mínimo diabético descontrolado',
        }


class GlucosaCapilarForm(forms.ModelForm):  # NEF-80
    class Meta:
        model = GlucosaCapilar
        exclude = []
        fields = [
            'beneficiario',
            'fecha',
            'doctor',
            'metodo',

            'glucosa',
            'max',
            'min',
            'comentario'
        ]
        widgets = {
            'fecha':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            # forms.SelectDateWidget(, attrs={'class': 'form-control'}),
            'doctor':
                forms.TextInput(attrs={'class': 'form-control'}),
            'metodo':
                forms.TextInput(attrs={'class': 'form-control'}),

            'glucosa':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'max':
                forms.NumberInput(attrs={'class': 'form-control maximo',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'min':
                forms.NumberInput(attrs={'class': 'form-control minimo ',
                                         'oninput': 'this.className',
                                         'min': '0', "max": "999"}),
            'comentario':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),
        }
        labels = {
            'fecha': 'Fecha del estudio:',
            'doctor': 'Doctor:',
            'metodo': 'Método:',

            'glucosa': 'Glucosa:',
            'max': 'Max:',
            'min': 'Min:',
            'comentario_glucosa': 'Comentario:',
        }


class FactorDeRiesgoForm(forms.ModelForm):  # NEF-30
    class Meta:
        model = FactorDeRiesgo
        exclude = [
        ]
        fields = [
            'beneficiario',
            'fecha',
            'p_1',
            'p_1_cual',
            'p_2',
            'p_2_2',
            'p_3',
            'p_3_2',
            'p_4',
            'p_5',
            'p_6',
            'p_7',
            'p_8',
            'p_8_2',
            'p_9',
            'p_10',
            'p_11',
            'p_12',
            'comentario'
        ]

        choices_1 = (('3', 'SÍ'), ('0', 'NO'), ('1', 'LO DESCONOCE'),)
        choices_2 = (('4', 'SÍ'), ('0', 'NO'),)
        choices_3 = (('2', 'SÍ'), ('0', 'NO'), ('1', 'LO DESCONOCE'),)
        choices_4 = (('1', '(1 a 2)'), ('2', '(3 a 5)'), ('3', '(más de 5)'), ('0', 'NINGUNO'),)
        choices_5 = (('2', 'SÍ'), ('0', 'NO'),)

        widgets = {
            'fecha':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'p_1':
                forms.RadioSelect(choices=choices_1),
            'p_2':
                forms.RadioSelect(choices=choices_1),
            'p_2_2':
                forms.RadioSelect(choices=choices_2),
            'p_3':
                forms.RadioSelect(choices=choices_1),
            'p_3_2':
                forms.RadioSelect(choices=choices_2, attrs={'required': False}),
            'p_4':
                forms.RadioSelect(choices=choices_1),
            'p_5':
                forms.RadioSelect(choices=choices_3),
            'p_6':
                forms.RadioSelect(choices=choices_3),
            'p_7':
                forms.RadioSelect(choices=choices_3),
            'p_8':
                forms.RadioSelect(choices=choices_5),
            'p_8_2':
                forms.RadioSelect(choices=choices_4),
            'p_9':
                forms.RadioSelect(choices=choices_5),
            'p_10':
                forms.RadioSelect(choices=choices_5),
            'p_11':
                forms.RadioSelect(choices=choices_5),
            'p_12':
                forms.RadioSelect(choices=choices_5),
            'comentario':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),
            'p_1_cual':
                forms.TextInput(attrs={'class': 'form-control mx-sm-3'}),
        }
        labels = {
            'fecha': 'Fecha de realización:',
            'p_1': '1. ¿Sus padres, hermanos o hermanas, padecen alguna enfermedad \
             crónica como diabetes o hipertensión?',
            'p_1_cual': '   ¿Cuál?',
            'p_2': '2. ¿Padece diabetes mellitus?',
            'p_2_2': '2.1. ¿Ha tenido cifras de glucosa mayor a 140 en ayunas? ',
            'p_3': '3. ¿Ha sido o actualmente está siendo tratado por presión arterial alta?',
            'p_3_2': '3.1. ¿Ha tenido cifras de presión arterial mayores a 130/80?',
            'p_4': '4. ¿Tiene algún familiar que padezca ERC, es decir con tratamiento \
             de diálisis peritoneal o hemodiálisis?',
            'p_5': '5. ¿Regularmente se auto medica con analgésicos de venta libre como \
            ibuprofeno, naproxeno, aspirinas, etc.?',
            'p_6': '6. ¿Ha padecido de litiasis renal (piedras en los riñones)?',
            'p_7': '7. ¿Padece sobrepeso u obesidad?',
            'p_8': '8. ¿Consume refrescos?',
            'p_8_2': '8.1. ¿Cuántos por semana?',
            'p_9': '9. ¿Agrega sal a sus alimentos en la mesa?',
            'p_10': '10. ¿Actualmente fuma o ha fumado en el pasado por más de diez años?',
            'p_11': '11. ¿Ingiere frecuentemente bebidas alcohólicas (una vez a la semana)?',
            'p_12': '12. ¿Ha padecido de episodios de tristeza?',
            'comentario': 'Comentario:',
        }


class MalnutricionInflamacionForm(forms.ModelForm):  # NEF-50
    class Meta:
        model = MalnutricionInflamacion
        exclude = []
        fields = [
            'beneficiario',
            'peso',
            'talla',
            'imc_valor',
            'imc_puntos',
            'fecha',
            'porcentaje_perdida_peso',
            'perdida_peso',
            'ingesta_alimentaria',
            'gastrointestinales',
            'incapacidad',
            'comorbilidad',
            'grasa_subcutanea',
            'perdida_muscular',
            'edema',
            'albumina',
            'fijacion_hierro',
            'comentario',
        ]
        widgets = {
            'fecha':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'perdida_peso':
                forms.NumberInput(attrs={'class': 'form-control minimo ',
                                         'oninput': 'this.className',
                                         'min': '0',
                                         'max': '99.9'}),
            'porcentaje_perdida_peso':
                forms.RadioSelect(choices=[(1, 'Ninguna'), (2, 'Menor a 5%'), (3, '5-10%'), (4, '10-15%'),
                                           (5, 'Mayor a 15.2%')]),
            'ingesta_alimentaria':
                forms.RadioSelect(choices=[(1, 'Ninguna'), (2, 'Dieta sólida insuficiente'),
                                           (3, 'Dieta líquida o moderada'), (4, 'Dieta líquida hipocalórica'),
                                           (5, 'Ayuno')]),
            'gastrointestinales':
                forms.RadioSelect(choices=[(1, 'Ninguna'), (2, 'Nauseas'), (3, 'Vómitos o síntomas moderados'),
                                           (4, 'Diarrea')]),
            'incapacidad':
                forms.RadioSelect(choices=[(1, 'Ninguna o mejoría'), (2, 'Dificultad para deambulación'),
                                           (3, 'Dificultad con act. normales'), (4, 'Actividad leve'),
                                           (5, 'Silla de ruedas')]),
            'comorbilidad':
                forms.RadioSelect(choices=[(1, '<= 1 año y sin comorbilidad'), (2, '1 a 4 años o com. leve'),
                                           (3, '>= 4 años y com. grave'), (4, 'En cama o silla de ruedas')]),
            'grasa_subcutanea':
                forms.RadioSelect(choices=[(0, 'Ninguna'), (1, 'Leve'), (2, 'Moderada'), (3, 'Grave')]),
            'perdida_muscular':
                forms.RadioSelect(choices=[(0, 'Ninguna'), (1, 'Leve'), (2, 'Moderada'), (3, 'Grave')]),
            'edema':
                forms.RadioSelect(choices=[(0, 'Ninguna'), (1, 'Leve'), (2, 'Moderada'), (3, 'Grave')]),
            'albumina':
                forms.RadioSelect(choices=[(0, '>4.0 g/dL'), (1, '3.5-3.9 g/dL'), (2, '3.0-3.4 g/dL'),
                                           (3, '<3.0 g/dL')]),
            'fijacion_hierro':
                forms.RadioSelect(choices=[(0, '>250mg/dL y transferrina>200mg/dL'),
                                           (1, '200-249mg/dL y transferrina 170-200mg/dL'),
                                           (2, '150-199mg/dL y transferrina 140-170mg/dL'),
                                           (3, '<150mg/dL y transferrina <140mg/dL')]),
            'comentario':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),
        }
        labels = {
            'fecha': 'Fecha del estudio:',
            'porcentaje_perdida_peso': 'Pérdida de peso (últimos 6 meses):',
            'ingesta_alimentaria': 'Cambio en la ingesta alimentaria:',
            'gastrointestinales': 'Síntomas gastrointestinales (presentes durante 2 semanas):',
            'incapacidad': 'Incapacidad funcional (relacionada con el estado nutricional):',
            'comorbilidad': 'Comorbilidad (tiempo en diálisis):',
            'grasa_subcutanea': 'Reservas disminuidas de grasa subcutánea (bíceps, tríceps, pecho):',
            'perdida_muscular': 'Signos de pérdida muscular:',
            'edema': 'Signos de edema / ascitis:',
            'albumina': 'Albumina',
            'fijacion_hierro': 'Capacidad total de fijación de hierro:',
        }


class TamizajeNutricionalForm(forms.ModelForm):  # NEF-62
    class Meta:
        model = TamizajeNutricional
        fields = [
            'beneficiario',
            'fecha',
            'presion_sistolica',
            'presion_diastolica',
            'peso',
            'talla',
            'circunferencia_brazo',
            'pliegue_bicipital',
            'pliegue_tricipital',
            'comentario',
        ]
        widgets = {
            'fecha':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            # forms.SelectDateWidget(, attrs={'class': 'form-control'}),
            'presion_sistolica':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999'}),
            'presion_diastolica':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999'}),

            'peso':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'talla':
                forms.NumberInput(attrs={'required': False, 'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'circunferencia_brazo':
                forms.NumberInput(attrs={'required': False, 'class': 'form-control ',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'pliegue_bicipital':
                forms.NumberInput(attrs={'required': False, 'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'pliegue_tricipital':
                forms.NumberInput(attrs={'required': False, 'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'comentario':
                forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                      'placeholder': 'Ingresa un comentario...'}),
        }

        labels = {
            'fecha': 'Fecha:',
            'peso': 'Peso:',
            'talla': 'Talla:',
            'presion_sistolica': 'Presión sistólica',
            'presion_diastolica': 'Presión diastólica',
            'circunferencia_brazo': 'Circunferencia de brazo:',
            'pliegue_bicipital': 'Pliegue bicipital:',
            'pliegue_tricipital': 'Pliegue tricipital:',
            'comentario': 'Comentario:'
        }


class AdherenciaTratamientoForm(forms.ModelForm):  # NEF-58
    class Meta:
        model = AdherenciaTratamiento
        fields = [
            'beneficiario',
            'fecha',
            'p1',
            'p2',
            'p3',
            'p4',
            'p5',
            'p6',
            'p7',
            'p8',
            'p9',
            'p10',
            'p11',
            'p12',
            'p13',
            'p14',
            'p14_comentario',
            'p15',
            'p15_comentario',
            'p16',
            'p16_comentario',
            'p17',
            'p17_comentario',
            'observaciones'
        ]

        choices_1 = (('5', 'Siempre'), ('4', 'Casi siempre'), ('3', 'A veces'), ('2', 'Casi nunca'), ('1', 'Nunca'))
        choices_2 = (('3', 'Sí'), ('1', 'No'), ('2', 'Parcialmente'))
        choices_3 = (('4', 'Excelente'), ('3', 'Buena'), ('2', 'Regular'), ('1', 'Mala'))

        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'p1': forms.RadioSelect(choices=choices_1),
            'p2': forms.RadioSelect(choices=choices_1),
            'p3': forms.RadioSelect(choices=choices_1),
            'p4': forms.RadioSelect(choices=choices_1),
            'p5': forms.RadioSelect(choices=choices_1),
            'p6': forms.RadioSelect(choices=choices_1),
            'p7': forms.RadioSelect(choices=choices_1),
            'p8': forms.RadioSelect(choices=choices_1),
            'p9': forms.RadioSelect(choices=choices_1),
            'p10': forms.RadioSelect(choices=choices_1),

            'p11': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                         'placeholder': 'Escribe tu respuesta...'}),
            'p12': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                         'placeholder': 'Escribe tu respuesta...'}),
            'p13': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                         'placeholder': 'Escribe tu respuesta...'}),

            'p14': forms.RadioSelect(choices=choices_2),
            'p14_comentario': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                                    'placeholder': 'Escribe tu respuesta...'}),
            'p15': forms.RadioSelect(choices=choices_3),
            'p15_comentario': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                                    'placeholder': 'Escribe tu respuesta...'}),
            'p16': forms.RadioSelect(choices=choices_3),
            'p16_comentario': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                                    'placeholder': 'Escribe tu respuesta...'}),
            'p17': forms.RadioSelect(choices=choices_3),
            'p17_comentario': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                                    'placeholder': 'Escribe tu respuesta...'}),

            'observaciones': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                                   'placeholder': 'Escribe tu respuesta...'}),
        }
        labels = {
            'fecha': 'Fecha:',
            'p1': '1. Toma los medicamentos en el horario establecido',
            'p2': '2. Se toma todas las dosis indicadas',
            'p3': '3. Cumple las indicaciones relacionadas con la dieta',
            'p4': '4. Asiste a las consultas de seguimiento programadas',
            'p5': '5. Acomoda sus horarios de medicación, a las actividades de su vida diaria',
            'p6': '6. Usted y su médico, deciden de manera conjunta, el tratamiento a seguir',
            'p7': '7. Cumple el tratamiento sin supervisión de su familia o amigos',
            'p8': '8. Lleva a cabo el tratamiento sin realizar grandes esfuerzos',
            'p9': '9. Utiliza recordatorios que faciliten la realización del tratamiento',
            'p10': '10. Tiene la posibilidad de manifestar su aceptación del tratamiento que ha prescripto su médico',
            'p11': '1. ¿Crees que hay algo que interfiera al empezar o realizar un tratamiento médico?',
            'p12': '2. ¿Cómo crees que te apoya tu familia en una enfermedad?',
            'p13': '3. ¿Quién es la persona que más te apoya?',
            'p14': 'Metas programadas:',
            'p15': 'Red familiar:',
            'p16': 'Estado emocional:',
            'p17': 'Área social:',
            'p14_comentario': 'Comentario',
            'p15_comentario': 'Comentario',
            'p16_comentario': 'Comentario',
            'p17_comentario': 'Comentario',
            'observaciones': 'Observaciones:'
        }


class EscalaHamiltonForm(forms.ModelForm):  # NEF-54
    class Meta:
        model = EscalaHamilton
        fields = [
            'beneficiario',
            'fecha',
            'p1',
            'p2',
            'p3',
            'p4',
            'p5',
            'p6',
            'p7',
            'p8',
            'p9',
            'p10',
            'p11',
            'p12',
            'p13',
            'p14',
            'p15',
            'p16',
            'p17',
            'observaciones',
        ]

        choices_1 = (('0', 'Ausente'), ('1', 'Estas sensaciones se indican solo al ser preguntados.'),
                     ('2', 'Estas sensaciones se relatan oral y espontáneamente.'), ('3', 'Sensaciones no comunicadas v'
                                                                                          'erbalmente, sino por la expresión facial, postura, voz o tendencia al llanto.'), ('4', 'El pacien'
                                                                                                                                                                                  'te manifiesta estas sensaciones en su conunicación verbal y no verbal de forma espontánea.'))
        choices_2 = (('0', 'Ausente'), ('1', 'Se culpa a sí mismo, cree haber decepcionado a la gente.'),
                     ('2', 'Ideas de culpabilidad, o meditación sobre errores pasados o malas acciones.'),
                     ('3', 'La enfermedad actual es un castigo. Ideas delirantes de culpabilidad.'),
                     ('4', 'Oye voces acusatorias o de denuncia y/o experimenta alucinaciones visuales amenazadoras.'))
        choices_3 = (('0', 'Ausente'), ('1', 'Le parece que la vida no merece la pena ser vivida.'),
                     ('2', 'Desearía estar muerto o tiene pensamientos sobre la posibilidad de morirse.'),
                     ('3', 'Ideas o amenazas de suicidio.'), ('4', 'Intentos de suicidio.'))
        choices_4 = (('0', 'Ausente'), ('1', 'Dificultades ocasionales para dormirse, por ejemplo más de media hora.'),
                     ('2', 'Dificultades para dormirse cada noche.'))
        choices_5 = (('0', 'Ausente'), ('1', 'El paciente se queja de estar inquieto durante la noche.'),
                     ('2', 'Está despierto durante la noche; cualquier ocasión de levantarse de la cama se puntúa como '
                           '2, excepto si está justificada (orinar, tomar o dar medicación…).'))
        choices_6 = (('0', 'Ausente'), ('1', 'Se despierta a primeras horas de la madrugada pero vuelve a dormirse.'),
                     ('2', 'No puede volver a dormirse si se levanta de la cama.'))
        choices_7 = (('0', 'Ausente'), ('1', 'Ideas y sentimientos de incapacidad. Fatiga o debilidad relacionadas con '
                                             'su trabajo, actividad o aficiones.'), ('2', 'Pérdida de interés en su actividad, aficiones o trab'
                                                                                          'ajo, manifestado directamente por el enfermo o indirectamente por desatención, indecisión y vacil'
                                                                                          'ación.'), ('3', 'Disminución del tiempo dedicado a actividades o descenso en la productividad.'),
                     ('4', 'Dejó de trabajar por la presente enfermedad.'))
        choices_8 = (('0', 'Palabra y pensamiento normales.'), ('1', 'Ligero retraso en el diálogo.'),
                     ('2', 'Evidente retraso en el diálogo.'), ('3', 'Diálogo difícil.'), ('4', 'Torpeza absoluta.'))
        choices_9 = (('0', 'Ninguna'), ('1', '"Juega" con sus manos, cabellos, etc.'), ('2', 'Se retuerce las manos, se'
                                                                                             ' muerde las uñas, los labios, se tira de los cabellos, etc.'))
        choices_10 = (('0', 'No hay dificultad.'), ('1', 'Tensión subjetiva e irritabilidad.'), ('2', 'Preocupación por'
                                                                                                      ' pequeñas cosas.'), ('3', 'Actitud aprensiva aparente en la expresión o en el habla.'),
                      ('4', 'Terrores expresados sin preguntarle.'))
        choices_11 = (('0', 'Ausente'), ('1', 'Ligera'), ('2', 'Moderada'), ('3', 'Grave'), ('4', 'Incapacitante'))
        choices_12 = (('0', 'Ninguno'), ('1', 'Pérdida del apetito, pero come sin necesidad de que lo estimulen. Sensac'
                                              'ión de pesadez en el abdomen.'), ('2', 'Dificultad en comer si no se le insiste. Solicita o nece'
                                                                                      'sita laxantes o medicación intestinal o para sus síntomas gastrointestinales.'))
        choices_13 = (('0', 'Ninguno'), ('1', 'Pesadez en la extremidades, espalda o cabeza. Dorsalgias, cefalalgias, m'
                                              'ialgias. Fatigabilidad y pérdida de energía.'), ('2', 'Cualquiera de los síntomas anteriores se '
                                                                                                     'puntúa como 2 si está muy bien definido.'))
        choices_14 = (('0', 'Ausentes'), ('1', 'Débiles.'), ('2', 'Graves'), ('3', 'Incapacitantes'))
        choices_15 = (('0', 'No la hay.'), ('1', 'Preocupado de sí mismo (corporalmente).'),
                      ('2', 'Preocupado por su salud.'),
                      ('3', 'Se lamenta constantemente. Solicita ayudas, etc.'),
                      ('4', 'Ideas delirantes hipocondríacas.'))
        choices_16 = (('0', 'Pérdida de peso inferior a 500 g por semana (de promedio).'),
                      ('1', 'Pérdida de peso de más de 500 g por semana (de promedio).'),
                      ('2', 'Pérdida de peso de más de 1 kg por semana (de promedio).'))
        choices_17 = (('0', 'Se da cuenta de que está deprimido y enfermo.'), ('1', 'Se da cuenta de su enfermedad pero'
                                                                                    ' atribuye la causa a la mala alimentación, clima, exceso de trabajo, virus, etc.'),
                      ('2', 'Niega estar enfermo.'))

        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'p1': forms.RadioSelect(choices=choices_1),
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

            'observaciones': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                                   'placeholder': 'Escribe tu observación...'}),
        }
        labels = {
            'fecha': 'Fecha:',
            'p1': ' 1. Humor deprimido (tristeza, depresión, desamparo, inutilidad)',
            'p2': ' 2. Sensación de culpabilidad',
            'p3': ' 3. Idea de suicidio',
            'p4': ' 4. Insomnio precoz',
            'p5': ' 5. Insomnio medio',
            'p6': ' 6. Insomnio tardío',
            'p7': ' 7. Problemas en el trabajo y actividades',
            'p8': ' 8. Inhibición (lentitud de pensamiento y de palabra; empeoramiento'
                  ' de la concentración; actividad motora disminuida)',
            'p9': ' 9. Agitación',
            'p10': ' 10. Ansiedad psíquica',
            'p11': ' 11. Ansiedad somática: signos o síntomas somáticos concomitantes de la ansiedad',
            'p12': ' 12. Síntomas somáticos gastrointestinales',
            'p13': ' 13. Síntomas somáticos generales',
            'p14': ' 14. Síntomas genitales como pérdida de la líbido y trastornos menstruales',
            'p15': ' 15. Hipocondría',
            'p16': '16. Estado emocional:',
            'p17': ' 17. Insight (conciencia de enfermedad)',
            'observaciones': 'Observaciones:',
        }


class ConsultaMedicaForm(forms.ModelForm):
    class Meta:
        model = ConsultaMedica
        fields = [
            'beneficiario',
            'fecha_creacion',
            'peso',
            'talla',
            'imc',
            'frecuencia_cardiaca',
            'frecuencia_respiratoria',
            'temperatura',
            'especificaciones',
            'analisis_enfermedad',
            'plan',
            'tratamiento',
            'observaciones',
            'presion_sistolica',
            'presion_diastolica',
        ]
        widgets = {
            'fecha_creacion':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),

            'peso':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999'}),
            'talla':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999'}),

            'imc':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'presion_sistolica':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999'}),
            'presion_diastolica':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999'}),
            'frecuencia_cardiaca':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'frecuencia_respiratoria':
                forms.NumberInput(attrs={'class': 'form-control ',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'temperatura':
                forms.NumberInput(attrs={'class': 'form-control',
                                         'oninput': 'this.className',
                                         'min': '0', 'max': '999.99'}),
            'especificaciones':
                forms.Textarea(attrs={'required': False, 'rows': '3', 'class': 'form-control',
                                      'placeholder': 'Comentario sobre paciente diagnosticado'}),
            'analisis_enfermedad':
                forms.Textarea(attrs={'required': False, 'rows': '3',
                                      'class': 'form-control', 'placeholder': 'Escribe tu comentarios...'}),
            'plan':
                forms.Textarea(attrs={'required': False, 'rows': '3',
                                      'class': 'form-control', 'placeholder': '¿Cuál es el plan?'}),
            'tratamiento':
                forms.Textarea(attrs={'required': False, 'rows': '3',
                                      'class': 'form-control', 'placeholder': '¿Cuál es el tratamiento?'}),
            'observaciones':
                forms.Textarea(attrs={'required': False, 'rows': '3',
                                      'class': 'form-control', 'placeholder': 'Escribe tu observación...'}),
        }

        labels = {
            'peso': 'Peso',
            'talla': 'Talla',
            'imc': 'IMC',
            'frecuencia_cardiaca': 'Frecuencia Cardiaca',
            'frecuencia_respiratoria': 'Frecuencia Respiratoria',
            'temperatura': 'Temperatura',
            'especificaciones': 'Especificaciones del paciente',
            'analisis_enfermedad': 'Análisis de la enfermedad renal',
            'plan': 'Plan',
            'tratamiento': 'Tratamiento',
            'observaciones': 'Observaciones',
            'presion_sistolica': 'Presión sistólica',
            'presion_diastolica': 'Presión diastólica'
        }


class EvaluacionPlaticasForm(forms.ModelForm):  # NEF-58
    class Meta:
        model = EvaluacionPlaticas
        fields = [
            'jornada',
            'fecha',
            'p1',
            'p2',
            'p3',
            'p4',
            'p5',
            'p6',
            'p7',
            'p8',
            'p9',
            'p10',
            'p11',
        ]

        choices_1 = (('0', 'Verdadero'), ('1', 'Falso'))
        choices_2 = (('0', 'Verdadero'), ('1', 'Falso'))
        choices_3 = (('1', 'Verdadero'), ('0', 'Falso'))
        choices_4 = (('1', 'Verdadero'), ('0', 'Falso'))
        choices_5 = (('1', 'Verdadero'), ('0', 'Falso'))
        choices_6 = (('1', 'Sí '), ('0', 'No'))
        choices_7 = (('1', 'Sí '), ('0', 'No'))
        choices_8 = (('1', 'Sí '), ('0', 'No'))
        choices_9 = (('0', 'Evitar consultas '), ('1', 'Platicar con los vecinos'),
                     ('2', 'Preguntar al médico sin miedo'))
        choices_10 = (('0', 'Disfrutar de la vida'), ('1', 'Las pérdidas significativas en la vida'),
                      ('2', 'Ganar salud'))
        choices_11 = (('1', 'Familia, medicos y sociedad integrados'), ('0', 'Servicios de salud'),
                      ('2', 'Apoyos de gobierno'))

        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'p1': forms.RadioSelect(choices=choices_1),
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
        }
        labels = {
            'fecha': 'Fecha de realización:',
            'p1': ' 1. El único trabajo de los riñones es eliminar los desechos y el líquido adicional del cuerpo.',
            'p2': ' 2. Las personas con diabetes o presión arterial alta, tienen mayor riesgo de contraer enfermedad renal crónica.',
            'p3': ' 3. La detección temprana y tratamiento de la enfermedad renal crónica, con frecuencia puede evitar su empeoramiento.',
            'p4': ' 4. La enfermedad renal crónica se puede detectar mediante análisis simples de sangre y orina.',
            'p5': ' 5. La mejor manera para saber la capacidad y la fase de funcionamiento de los riñones es conocer el índice de filtración glomerular (IFG).',
            'p6': ' 1. ¿Disminuir el consumo de sal, es bueno para el cuidado de los riñones?',
            'p7': ' 2. ¿El aumento de consumo de frutas y verduras, ayudan a prevenir la Enfermedad Renal Crónica?',
            'p8': ' 3. ¿Se recomienda beber de dos a dos y medio litros de agua natural al día?',
            'p9': ' 1. ¿Que necesito para entender el diagnóstico?',
            'p10': ' 2. ¿Que es el duelo?',
            'p11': ' 3. ¿Que son las redes de apoyo?',
        }


class NotaForm(forms.ModelForm):
    class Meta:
        model = Notas
        fields = [
            'beneficiario',
            'fecha_creacion',
            'nota',
        ]
        widgets = {
            'fecha_creacion':
                forms.DateInput(format='%Y-%m-%d', attrs={'type': 'hidden',
                                                          'class': 'form-control'}),
            'nota':
                forms.Textarea(attrs={'required': True, 'rows': '12',
                                      'class': 'form-control', 'placeholder': 'Escribe tu nota...'}),
        }

        labels = {
            'nota': 'Nota'
        }


class RegistroMensualForm(forms.ModelForm):  # NEF-58
    class Meta:
        model = RegistroMensual
        fields = [
            'beneficiario',
            'fecha',
            'p1',
            'p2',
            'p3',
            'observaciones'
        ]

        choices_1 = (('2', 'Sí'), ('0', 'No'), ('1', 'Parcialmente'))

        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'p1': forms.RadioSelect(choices=choices_1),
            'p2': forms.RadioSelect(choices=choices_1),
            'p3': forms.RadioSelect(choices=choices_1),
            'observaciones': forms.Textarea(attrs={'required': False, 'rows': '2', 'class': 'form-control',
                                                   'placeholder': 'Escribe tu respuesta...'}),
        }    
        labels = {
            'fecha': 'Fecha:',
            'p1': 'Médica:',
            'p2': 'Nutricional:',
            'p3': 'Estilo de vida:',
            'observaciones': 'Observaciones:'
        }