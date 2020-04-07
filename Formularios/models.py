from django.db import models
from Beneficiarios.models import *
from Proyectos.models import *
import datetime
from django.core.validators import *
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


def get_uuid():
    return uuid.uuid1().hex


class Evidencia(models.Model):  # NEF-99
    beneficiario = models.ForeignKey(Beneficiario, verbose_name='Beneficiario', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha de creación', default=timezone.now)
    fecha_subida = models.DateTimeField(verbose_name='Fecha de subida', null=True)
    nombre = models.TextField(max_length=255, blank=False)
    descripcion = models.TextField(verbose_name='Descripción', max_length=1024, blank=True)
    urn = models.TextField(max_length=255, unique=True, null=True, default=get_uuid)
    existe = models.BooleanField(default=False)


class QuimicaSanguineaManager(models.Manager):  # NEF-69

    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class QuimicaSanguinea(models.Model):  # NEF-66, NEF-68, NEF-69

    class Meta:
        verbose_name = 'Química Sanguínea'
        verbose_name_plural = 'Química Sanguínea'

    beneficiario = models.ForeignKey(Beneficiario, verbose_name='Paciente', on_delete=models.CASCADE)
    fecha_creacion = models.DateField(verbose_name='Fecha de Creación', default=datetime.date.today)
    fecha = models.DateField(verbose_name='Fecha del Estudio', default=datetime.date.today)
    doctor = models.CharField(verbose_name='Doctor', max_length=180)
    metodo = models.CharField(verbose_name='Método', max_length=100)

    glucosa = models.DecimalField(verbose_name='Glucosa', max_digits=5, decimal_places=2,
                                  validators=[MinValueValidator(0)])
    max_glucosa = models.DecimalField(verbose_name='Glucosa Máximo', max_digits=5, decimal_places=2,
                                      validators=[MinValueValidator(0)])
    min_glucosa = models.DecimalField(verbose_name='Glucosa Mínimo', max_digits=5, decimal_places=2,
                                      validators=[MinValueValidator(0)])
    comentario_glucosa = models.TextField(verbose_name='Glucosa Comentarios', max_length=255, null=True, blank=True)
    max_glucosa.default = 100
    min_glucosa.default = 70

    urea = models.DecimalField(verbose_name='Urea', max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    max_urea = models.DecimalField(verbose_name='Urea Máximo', max_digits=5, decimal_places=2,
                                   validators=[MinValueValidator(0)])
    min_urea = models.DecimalField(verbose_name='Urea Mínimo', max_digits=5, decimal_places=2,
                                   validators=[MinValueValidator(0)])
    comentario_urea = models.TextField(verbose_name='Urea Comentarios', max_length=255, null=True, blank=True)
    max_urea.default = 45
    min_urea.default = 15

    bun = models.DecimalField(verbose_name='Bun', max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    max_bun = models.DecimalField(verbose_name='Bun Máximo', max_digits=5, decimal_places=2,
                                  validators=[MinValueValidator(0)])
    min_bun = models.DecimalField(verbose_name='Bun Mínimo', max_digits=5, decimal_places=2,
                                  validators=[MinValueValidator(0)])
    comentario_bun = models.TextField(verbose_name='Bun Comentarios', max_length=255, null=True, blank=True)
    max_bun.default = 21
    min_bun.default = 7

    creatinina = models.DecimalField(verbose_name='Creatinina', max_digits=5, decimal_places=2,
                                     validators=[MinValueValidator(0)])
    max_creatinina_h = models.DecimalField(verbose_name='Creatinina Máximo Hombres', max_digits=5, decimal_places=2,
                                           validators=[MinValueValidator(0)])
    min_creatinina_h = models.DecimalField(verbose_name='Creatinina Mínimo Hombres', max_digits=5, decimal_places=2,
                                           validators=[MinValueValidator(0)])
    max_creatinina_m = models.DecimalField(verbose_name='Creatinina Máximo Mujeres', max_digits=5, decimal_places=2,
                                           validators=[MinValueValidator(0)])
    min_creatinina_m = models.DecimalField(verbose_name='Creatinina Mínimo Mujeres', max_digits=5, decimal_places=2,
                                           validators=[MinValueValidator(0)])
    comentario_creatinina = models.TextField(verbose_name='Creatinina Comentarios', max_length=255, null=True,
                                             blank=True)
    activo = models.BooleanField(null=False, default=True)
    objects = QuimicaSanguineaManager()
    max_creatinina_h.default = 1.2
    min_creatinina_h.default = 0.7
    max_creatinina_m.default = 1
    min_creatinina_m.default = 0.5

    acido_urico = models.DecimalField(verbose_name='Ácido Úrico', max_digits=5, decimal_places=2,
                                      validators=[MinValueValidator(0)], blank=True, null=True, default=None)
    max_acido_urico_h = models.DecimalField(verbose_name='Ácido Úrico Máximo Hombres', max_digits=5, decimal_places=2,
                                            validators=[MinValueValidator(0)])
    min_acido_urico_h = models.DecimalField(verbose_name='Ácido Úrico Mínimo Hombres', max_digits=5, decimal_places=2,
                                            validators=[MinValueValidator(0)])
    max_acido_urico_m = models.DecimalField(verbose_name='Ácido Úrico Máximo Mujeres', max_digits=5, decimal_places=2,
                                            validators=[MinValueValidator(0)])
    min_acido_urico_m = models.DecimalField(verbose_name='Ácido Úrico Mínimo Mujeres', max_digits=5, decimal_places=2,
                                            validators=[MinValueValidator(0)])
    comentario_acido_urico = models.TextField(verbose_name='Ácido Úrico Comentarios', max_length=255, null=True,
                                              blank=True)

    max_acido_urico_h.default = 7.0
    min_acido_urico_h.default = 3.4
    max_acido_urico_m.default = 6.0
    min_acido_urico_m.default = 2.4

    activo = models.BooleanField(null=False, default=True)
    usado_para_estadificacion = models.BooleanField(null=False, default=False)

    objects = QuimicaSanguineaManager()

    metodo.default = "Colorimétrico"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ma = Microalbuminuria.objects.filter(beneficiario=self.beneficiario.id)
        latest_clasification = Clasificacion.objects.filter(beneficiario=self.beneficiario.id)

        if ma.exists() and self.activo:
            ma = ma.latest('id')
            if clasification(self.beneficiario, self, ma):
                if latest_clasification.exists():
                    latest_clasification = latest_clasification.latest('id')
                    latest_clasification.activo = False
                    latest_clasification.save()

    def __str__(self):
        return str(self.beneficiario) + " - Química Sanguínea " + str(self.id)

    def delete(self, *args, **kwargs):
        Clasificacion.objects.filter(id_qs=self.id).delete()
        self.activo = False
        self.save()


class MicroalbuminuriaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class Microalbuminuria(models.Model):  # NEF-74

    class Meta:
        verbose_name = 'Microalbuminuria'
        verbose_name_plural = 'Microalbuminuria'

    beneficiario = models.ForeignKey(Beneficiario, on_delete='CASCADE')
    fecha = models.DateField(default=datetime.date.today)
    metodo = models.CharField(max_length=100)
    doctor = models.CharField(max_length=180)
    micro_albumina = models.DecimalField()
    micro_albumina.max_digits = 5
    micro_albumina.decimal_places = 2
    micro_albumina.validators = [MinValueValidator(0)]
    micro_albumina_min = models.DecimalField()
    micro_albumina_min.max_digits = 5
    micro_albumina_min.decimal_places = 2
    micro_albumina_min.validators = [MinValueValidator(0)]
    micro_albumina_min.default = 0
    micro_albumina_max = models.DecimalField()
    micro_albumina_max.max_digits = 5
    micro_albumina_max.decimal_places = 2
    micro_albumina_max.validators = [MinValueValidator(0)]
    micro_albumina_max.default = 30
    micro_albumina_comentario = models.CharField(max_length=255, null=True)
    micro_albumina_comentario.blank = True
    creatinina = models.DecimalField()
    creatinina.max_digits = 5
    creatinina.decimal_places = 2
    creatinina.validators = [MinValueValidator(0)]
    creatinina_min = models.DecimalField()
    creatinina_min.max_digits = 5
    creatinina_min.decimal_places = 2
    creatinina_min.validators = [MinValueValidator(0)]
    creatinina_min.default = 10
    creatinina_max = models.DecimalField()
    creatinina_max.max_digits = 5
    creatinina_max.decimal_places = 2
    creatinina_max.validators = [MinValueValidator(0)]
    creatinina_max.default = 300
    creatinina_comentario = models.CharField(max_length=255, null=True)
    creatinina_comentario.blank = True
    relacion = models.DecimalField()
    relacion.max_digits = 5
    relacion.decimal_places = 2
    relacion.validators = [MinValueValidator(0)]
    relacion_normal_min = models.DecimalField()
    relacion_normal_min.max_digits = 5
    relacion_normal_min.decimal_places = 2
    relacion_normal_min.validators = [MinValueValidator(0)]
    relacion_normal_min.default = 0
    relacion_normal_max = models.DecimalField()
    relacion_normal_max.max_digits = 5
    relacion_normal_max.decimal_places = 2
    relacion_normal_max.validators = [MinValueValidator(0)]
    relacion_normal_max.default = 30
    relacion_anormal_min = models.DecimalField()
    relacion_anormal_min.max_digits = 5
    relacion_anormal_min.decimal_places = 2
    relacion_anormal_min.validators = [MinValueValidator(0)]
    relacion_anormal_min.default = 30
    relacion_anormal_max = models.DecimalField()
    relacion_anormal_max.max_digits = 5
    relacion_anormal_max.decimal_places = 2
    relacion_anormal_max.validators = [MinValueValidator(0)]
    relacion_anormal_max.default = 50
    relacion_anormal_alta_min = models.DecimalField()
    relacion_anormal_alta_min.max_digits = 5
    relacion_anormal_alta_min.decimal_places = 2
    relacion_anormal_alta_min.validators = [MinValueValidator(0)]
    relacion_anormal_alta_min.default = 50
    relacion_anormal_alta_max = models.DecimalField()
    relacion_anormal_alta_max.max_digits = 5
    relacion_anormal_alta_max.decimal_places = 2
    relacion_anormal_alta_max.validators = [MinValueValidator(0)]
    relacion_anormal_alta_max.default = 300
    metodo.default = "Inmunoensayo enzimático"
    fecha_creacion = models.DateField(default=datetime.date.today)

    activo = models.BooleanField(null=False, default=True)
    usado_para_estadificacion = models.BooleanField(null=False, default=False)

    objects = MicroalbuminuriaManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        qs = QuimicaSanguinea.objects.filter(beneficiario=self.beneficiario.id)

        latest_clasification = Clasificacion.objects.filter(beneficiario=self.beneficiario.id)
        if qs.exists() and self.activo:
            qs = qs.latest('id')
            if clasification(self.beneficiario, qs, self):
                if latest_clasification.exists():
                    latest_clasification = latest_clasification.latest('id')
                    latest_clasification.activo = False
                    latest_clasification.save()

    def delete(self):
        Clasificacion.objects.filter(id_ma=self.id).delete()
        self.activo = False
        self.save()

    def __str__(self):
        return str(self.beneficiario) + " - Microalbuminuria " + str(self.id)


class HemoglobinaGlucosiladaManager(models.Manager):  # NEF-73
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class HemoglobinaGlucosilada(models.Model):  # NEF-70

    class Meta:
        verbose_name = 'Hemoglobina Glucosilada'
        verbose_name_plural = 'Hemoglobina Glucosilada'

    beneficiario = models.ForeignKey(Beneficiario, on_delete='CASCADE')
    fecha = models.DateField(default=datetime.date.today)
    fecha_captura = models.DateField(default=datetime.date.today)
    metodo = models.CharField(max_length=100)
    doctor = models.CharField(max_length=180)
    comentario = models.CharField(max_length=1000, null=True, blank=True)
    hemoglobina_glucosilada = models.DecimalField()
    hemoglobina_glucosilada.max_digits = 5
    hemoglobina_glucosilada.decimal_places = 2
    hemoglobina_glucosilada.validators = [MinValueValidator(1)]
    max_no_diabetico = models.DecimalField()
    max_no_diabetico.max_digits = 5
    max_no_diabetico.decimal_places = 2
    max_no_diabetico.validators = [MinValueValidator(0)]
    min_no_diabetico = models.DecimalField()
    min_no_diabetico.max_digits = 5
    min_no_diabetico.decimal_places = 2
    min_no_diabetico.validators = [MinValueValidator(0)]

    max_diabetico_no_cont = models.DecimalField()
    max_diabetico_no_cont.max_digits = 5
    max_diabetico_no_cont.decimal_places = 2
    max_diabetico_no_cont.validators = [MinValueValidator(0)]
    min_diabetico_no_cont = models.DecimalField()
    min_diabetico_no_cont.max_digits = 5
    min_diabetico_no_cont.decimal_places = 2
    min_diabetico_no_cont.validators = [MinValueValidator(0)]

    max_diabetico_cont = models.DecimalField()
    max_diabetico_cont.max_digits = 5
    max_diabetico_cont.decimal_places = 2
    max_diabetico_cont.validators = [MinValueValidator(0)]
    min_diabetico_cont = models.DecimalField()
    min_diabetico_cont.max_digits = 5
    min_diabetico_cont.decimal_places = 2
    min_diabetico_cont.validators = [MinValueValidator(0)]

    activo = models.BooleanField(null=False, default=True)
    objects = HemoglobinaGlucosiladaManager()

    def delete(self):
        self.activo = False
        self.save()

    def __str__(self):
        return str(self.beneficiario) + " - Hemoglobina Glucosilada " + str(self.id)


class GlucosaCapilarManager(models.Manager):  # NEF-83
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class GlucosaCapilar(models.Model):  # NEF-80

    class Meta:
        verbose_name = 'Glucosa Capilar'
        verbose_name_plural = 'Glucosa Capilar'

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=datetime.date.today)
    fecha = models.DateField(default=datetime.date.today)
    doctor = models.CharField(max_length=180)
    metodo = models.CharField(max_length=100)

    glucosa = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    min = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    max = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    comentario = models.TextField(max_length=1000, null=True, blank=True)
    min.default = 70
    max.default = 100

    activo = models.BooleanField(null=False, default=True)
    objects = GlucosaCapilarManager()

    def delete(self):
        self.activo = False
        self.save()

    def __str__(self):
        return str(self.beneficiario) + " - Glucosa Capilar " + str(self.id)


class FactorDeRiesgoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class FactorDeRiesgo(models.Model):  # NEF-30

    class Meta:
        verbose_name = 'Factor de Riesgo'
        verbose_name_plural = 'Factor de Riesgo'

    labels = {  # NEF-154
        'fecha': 'Fecha de realización:',
        'p_1': '1. ¿Sus padres, hermanos o hermanas, padecen alguna enfermedad \
         crónica como diabetes o hipertensión?',
        'p_1_cual': '1.1. ¿Cuál?',
        'p_2': '2. ¿Padece diabetes mellitus?',
        'p_2_2': '2.1 ¿Ha tenido cifras de glucosa mayor a 140 en ayunas? ',
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
    choices_1 = {3: 'SÍ',
                 0: 'NO',
                 1: 'LO DESCONOCE', }
    choices_2 = {4: 'SÍ',
                 0: 'NO', }
    choices_3 = {2: 'SÍ',
                 0: 'NO',
                 1: 'LO DESCONOCE', }
    choices_4 = {1: '(1 a 2)',
                 2: '(3 a 5)',
                 3: '(más de 5)',
                 0: 'NINGUNO', }
    choices_5 = {2: 'SÍ',
                 0: 'NO', }
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=datetime.date.today)
    fecha = models.DateField(default=datetime.date.today)
    p_1 = models.IntegerField(validators=[MinValueValidator(0)])
    p_1_cual = models.CharField(max_length=75, null=True, blank=True)
    p_2 = models.IntegerField(validators=[MinValueValidator(0)])
    p_2_2 = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    p_3 = models.IntegerField(validators=[MinValueValidator(0)])
    p_3_2 = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    p_4 = models.IntegerField(validators=[MinValueValidator(0)])
    p_5 = models.IntegerField(validators=[MinValueValidator(0)])
    p_6 = models.IntegerField(validators=[MinValueValidator(0)])
    p_7 = models.IntegerField(validators=[MinValueValidator(0)])
    p_8 = models.IntegerField(validators=[MinValueValidator(0)])
    p_8_2 = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    p_9 = models.IntegerField(validators=[MinValueValidator(0)])
    p_10 = models.IntegerField(validators=[MinValueValidator(0)])
    p_11 = models.IntegerField(validators=[MinValueValidator(0)])
    p_12 = models.IntegerField(validators=[MinValueValidator(0)])
    comentario = models.TextField(max_length=1000, null=True, blank=True)
    resultado = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    activo = models.BooleanField(null=False, default=True)
    objects = FactorDeRiesgoManager()

    @property
    def interpretacion(self):
        if self.resultado <= 10:
            return "BAJO RIESGO"
        elif self.resultado >= 11 and self.resultado <= 19:
            return "MODERADO RIESGO"
        elif self.resultado >= 20:
            return "ALTO RIESGO"

    def save(self, *args, **kwargs):
        p_2_2 = 0
        p_3_2 = 0
        p_8_2 = 0
        if self.p_2 == 3:
            p_2_2 = self.p_2_2
        if self.p_3 == 3:
            p_3_2 = self.p_3_2
        if self.p_8 == 2:
            p_8_2 = self.p_8_2
        self.resultado = self.p_1 + self.p_2 + self.p_3 + self.p_4 + self.p_5 + self.p_6 + self.p_7 + self.p_8 + \
            self.p_9 + self.p_10 + self.p_11 + self.p_12 + p_2_2 + p_3_2 + p_8_2
        super().save(*args, **kwargs)

    def delete(self):
        self.activo = False
        self.save()


class Clasificacion(models.Model):  # NEF-94 NEF-95

    class Meta:
        verbose_name = 'Clasificación'
        verbose_name_plural = 'Clasificación'

    beneficiario = models.ForeignKey(Beneficiario, on_delete='CASCADE')
    categoria_gfr_estimada = models.CharField(max_length=3)
    gfr_estimada = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    categoria_gfr = models.CharField(max_length=3)
    gfr = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    categoria_alb = models.CharField(max_length=2)
    albumina = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    id_qs = models.ForeignKey(QuimicaSanguinea, on_delete='CASCADE')
    id_ma = models.ForeignKey(Microalbuminuria, on_delete='CASCADE')
    fecha = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete='CASCADE', null=True, blank=True)
    activo = models.BooleanField(default=False)

    @property
    def color(self):
        if self.discrepancia:
            return "gray"
        return Clasificacion.get_color(self.categoria_gfr, self.categoria_alb)

    @property
    def color_gfr(self):
        return Clasificacion.get_color(self.categoria_gfr, self.categoria_alb)

    @property
    def color_gfr_estimada(self):
        return Clasificacion.get_color(self.categoria_gfr_estimada, self.categoria_alb)

    @property
    def discrepancia(self):
        return self.categoria_gfr != self.categoria_gfr_estimada

    def get_color(gfr, alb):
        if (gfr == "G1" or gfr == "G2") and alb == "A1":
            return "low-risk"
        if alb == "A2" and (gfr == "G2" or gfr == "G1") or \
                (gfr == "G3a" and alb == "A1"):
            return "increased-risk"
        if alb == "A3" and (gfr == "G2" or gfr == "G1") or \
                (gfr == "G3a" and alb == "A2") or \
                (gfr == "G3b" and alb == "A1"):
            return "high-risk"
        if alb == "A3" and (gfr == "G3a" or gfr == "G3b") or \
                (alb == "A2" and (gfr == "G3b" or gfr == "G4")) or \
                (gfr == "G4" and alb == "A1"):
            return "very-high-risk"
        return "ultra-high-risk"


class TamizajeNutricionalManager(models.Manager):  # NEF-65
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class TamizajeNutricional(models.Model):  # NEF-62

    class Meta:
        verbose_name = 'Tamizaje Nutricional'
        verbose_name_plural = 'Tamizaje Nutricional'

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=datetime.date.today)
    fecha = models.DateField(default=datetime.date.today)
    presion_sistolica = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], default=120)
    presion_diastolica = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], default=80)
    peso = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    talla = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    circunferencia_brazo = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    pliegue_bicipital = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    pliegue_tricipital = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    imc = models.DecimalField(max_digits=6, decimal_places=3, validators=[MinValueValidator(0)], default=0)
    comentario = models.TextField(max_length=1000, null=True, blank=True)

    activo = models.BooleanField(null=False, default=True)
    objects = TamizajeNutricionalManager()

    def save(self, *args, **kwargs):
        tamizaje = TamizajeNutricional.objects.filter(beneficiario=self.beneficiario.id)
        if tamizaje.exists():
            tamizaje = tamizaje.latest("id")
            if self.talla is None:
                self.talla = tamizaje.talla
            if self.circunferencia_brazo is None:
                self.circunferencia_brazo = tamizaje.circunferencia_brazo
            if self.pliegue_bicipital is None:
                self.pliegue_bicipital = tamizaje.pliegue_bicipital
            if self.pliegue_tricipital is None:
                self.pliegue_tricipital = tamizaje.pliegue_tricipital
        if self.talla is not None and self.circunferencia_brazo is not None:
            self.imc = round(float(self.peso) / (float(self.talla) * float(self.talla)), 3)
        super().save(*args, **kwargs)

    def delete(self):
        self.activo = False
        self.save()

    def __str__(self):
        return str(self.beneficiario) + " - Tamizaje Nutricional " + str(self.id)


class MalnutricionInflamacionManager(models.Manager):   # NEF-53
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class MalnutricionInflamacion(models.Model):  # NEF-50

    class Meta:
        verbose_name = 'Malnutrición-Inflamación'
        verbose_name_plural = 'Malnutrición-Inflamación'

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=datetime.date.today)
    fecha = models.DateField(default=datetime.date.today)
    porcentaje_perdida_peso = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    perdida_peso = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0)])
    ingesta_alimentaria = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    gastrointestinales = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    incapacidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comorbilidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    peso = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    talla = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    imc_valor = models.DecimalField(max_digits=6, decimal_places=3, validators=[MinValueValidator(0)], default=0)
    imc_puntos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], default=0)
    grasa_subcutanea = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    perdida_muscular = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    edema = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    albumina = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    fijacion_hierro = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    resultado = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(41)], default=0)
    comentario = models.TextField(max_length=1000, null=True, blank=True)

    activo = models.BooleanField(null=False, default=True)
    objects = MalnutricionInflamacionManager()

    @property
    def interpretacion(self):
        if self.resultado == 0:
            return "A- Estado Nutricional Normal"
        elif self.resultado >= 1 and self.resultado <= 9:
            return "B-  Desnutrición Leve"
        elif self.resultado >= 10 and self.resultado <= 19:
            return "C- Desnutrición Moderada"
        elif self.resultado >= 20 and self.resultado <= 29:
            return "D- Desnutrición Grave"
        elif self.resultado >= 30:
            return "E- Desnutrición Gravísima"

    def save(self, *args, **kwargs):
        self.resultado = round(self.porcentaje_perdida_peso +
                               self.ingesta_alimentaria +
                               self.gastrointestinales +
                               self.incapacidad +
                               self.comorbilidad +
                               self.grasa_subcutanea +
                               self.perdida_muscular +
                               self.edema +
                               self.albumina +
                               self.fijacion_hierro +
                               self.imc_puntos, 0)
        super().save(*args, **kwargs)

    def delete(self):
        self.activo = False
        self.save()

    def __str__(self):
        return str(self.beneficiario) + " - Malnutrición Inflamación " + str(self.id)


class AdherenciaTratamientoManager(models.Manager):   # NEF-61
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class AdherenciaTratamiento(models.Model):  # NEF-58

    class Meta:
        verbose_name = 'Adherencia al Tratamiento'
        verbose_name_plural = 'Adherencia al Tratamiento'

    labels = {
        'fecha': 'Fecha de realización:',
        'p1': ' toma los medicamentos en el horario establecido',
        'p2': ' se toma todas las dosis indicadas',
        'p3': ' cumple las indicaciones relacionadas con la dieta',
        'p4': ' asiste a las consultas de seguimiento programadas',
        'p5': ' acomoda sus horarios de medicación, a las actividades de su vida diaria',
        'p6': ' usted y su médico, deciden de manera conjunta, el tratamiento a seguir',
        'p7': ' cumple el tratamiento sin supervisión de su familia o amigos',
        'p8': ' lleva a cabo el tratamiento sin realizar grandes esfuerzos',
        'p9': ' utiliza recordatorios que faciliten la realización del tratamiento',
        'p10': ' tiene la posibilidad de manifestar su aceptación del tratamiento que ha prescripto su médico',
        'p11': '11. ¿Crees que hay algo que interfiera al empezar o realizar un tratamiento médico?',
        'p12': '12. ¿Cómo crees que te apoya tu familia en una enfermedad?',
        'p13': '13. ¿Quién es la persona que más te apoya?',
        'p14': '14. Metas programadas:',
        'p15': '15. Red familiar:',
        'p16': '16. Estado emocional:',
        'p17': '17. Área social:',
        'observaciones': 'Observaciones:'
    }
    choices_1 = {5: 'Siempre', 4: 'Casi siempre', 3: 'A veces', 2: 'Casi nunca', 1: 'Nunca'}
    choices_2 = {3: 'Sí', 2: 'Parcialmente', 1: 'No'}
    choices_3 = {5: 'Siempre', 4: 'Excelente', 3: 'Buena', 2: 'Regular', 1: 'Mala'}

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.date.today)
    fecha_creacion = models.DateField(default=datetime.date.today)
    p1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p3 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p4 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p5 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p6 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p7 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p8 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p9 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p10 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    p11 = models.TextField(max_length=255)
    p12 = models.TextField(max_length=255)
    p13 = models.TextField(max_length=255)

    p14 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p14_comentario = models.TextField(max_length=255, null=True, blank=True)
    p15 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p15_comentario = models.TextField(max_length=255, null=True, blank=True)
    p16 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p16_comentario = models.TextField(max_length=255, null=True, blank=True)
    p17 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    p17_comentario = models.TextField(max_length=255, null=True, blank=True)

    observaciones = models.TextField(max_length=1000, null=True, blank=True)
    resultado = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    activo = models.BooleanField(null=False, default=True)
    objects = AdherenciaTratamientoManager()

    def delete(self):
        self.activo = False
        self.save()

    @property
    def interpretacion(self):
        if self.resultado >= 0 and self.resultado <= 10:
            return "Rechazo"
        elif self.resultado >= 11 and self.resultado <= 20:
            return "Negación"
        elif self.resultado >= 21 and self.resultado <= 30:
            return "Modificación"
        elif self.resultado >= 31 and self.resultado <= 40:
            return "Aceptación"
        elif self.resultado >= 41:
            return "Adherencia"

    def save(self, *args, **kwargs):
        self.resultado = self.p1 + self.p2 + self.p3 + self.p4 + self.p5 + \
            self.p6 + self.p7 + self.p8 + self.p9 + self.p10
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.beneficiario) + " - Adherencia al tratamiento " + str(self.id)


class EscalaHamiltonManager(models.Manager):   # NEF-57
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class EscalaHamilton(models.Model):  # NEF-54

    class Meta:
        verbose_name = 'Escala de Hamilton'
        verbose_name_plural = 'Escala de Hamilton'

    labels = {
        'fecha': 'Fecha de realización:',
        'p1': ' 1. Humor deprimido (tristeza, depresión, desamparo, inutilidad):',
        'p2': ' 2. Sensación de culpabilidad:',
        'p3': ' 3. Idea de suicidio:',
        'p4': ' 4. Insomnio precoz:',
        'p5': ' 5. Insomnio medio:',
        'p6': ' 6. Insomnio tardío:',
        'p7': ' 7. Problemas en el trabajo y actividades:',
        'p8': ' 8. Inhibición (lentitud de pensamiento y de palabra; empeoramiento:'
              ' de la concentración; actividad motora disminuida):',
        'p9': ' 9. Agitación:',
        'p10': ' 10. Ansiedad psíquica:',
        'p11': ' 11. Ansiedad somática: signos o síntomas somáticos concomitantes de la ansiedad:',
        'p12': ' 12. Síntomas somáticos gastrointestinales:',
        'p13': ' 13. Síntomas somáticos generales:',
        'p14': ' 14. Síntomas genitales como pérdida de la líbido y trastornos menstruales:',
        'p15': ' 15. Hipocondría:',
        'p16': ' 16. Estado emocional:',
        'p17': ' 17. Insight (conciencia de enfermedad):',
        'observaciones': 'Observaciones:',
        'resultado': 'Resultado',
        'puntos': 'Puntos'
    }

    choices_1 = {0: 'Ausente', 1: 'Estas sensaciones se indican solo al ser preguntados.', 2: 'Estas sensaciones se relatan oral y espontáneamente.',
                 3: 'Sensaciones no comunicadas verbalmente, sino por la expresión facial, postura, voz o tendencia al llanto.',
                 4: 'El pacientemanifiesta estas sensaciones en su conunicación verbal y no verbal de forma espontánea.'}
    choices_2 = {0: 'Ausente', 1: 'Se culpa a sí mismo, cree haber decepcionado a la gente.',
                 2: 'Ideas de culpabilidad, o meditación sobre errores pasados o malas acciones.',
                 3: 'La enfermedad actual es un castigo. Ideas delirantes de culpabilidad.',
                 4: 'Oye voces acusatorias o de denuncia y/o experimenta alucinaciones visuales amenazadoras.'}
    choices_3 = {0: 'Ausente', 1: 'Le parece que la vida no merece la pena ser vivida.',
                 2: 'Desearía estar muerto o tiene pensamientos sobre la posibilidad de morirse.',
                 3: 'Ideas o amenazas de suicidio.', 4: 'Intentos de suicidio.'}
    choices_4 = {0: 'Ausente', 1: 'Dificultades ocasionales para dormirse, por ejemplo más de media hora.',
                 2: 'Dificultades para dormirse cada noche.'}
    choices_5 = {0: 'Ausente', 1: 'El paciente se queja de estar inquieto durante la noche.',
                 2: 'Está despierto durante la noche; cualquier ocasión de levantarse de la cama se puntúa como '
                    '2, excepto si está justificada (orinar, tomar o dar medicación…).'}
    choices_6 = {0: 'Ausente', 1: 'Se despierta a primeras horas de la madrugada pero vuelve a dormirse.',
                 2: 'No puede volver a dormirse si se levanta de la cama.'}
    choices_7 = {0: 'Ausente', 1: 'Ideas y sentimientos de incapacidad. Fatiga o debilidad relacionadas con '
                 'su trabajo, actividad o aficiones.',
                 2: 'Pérdida de interés en su actividad, aficiones o trab'
                 'ajo, manifestado directamente por el enfermo o indirectamente por desatención, indecisión y vacil'
                 'ación.',
                 3: 'Disminución del tiempo dedicado a actividades o descenso en la productividad.',
                 4: 'Dejó de trabajar por la presente enfermedad.'}
    choices_8 = {0: 'Palabra y pensamiento normales.', 1: 'Ligero retraso en el diálogo.',
                 2: 'Evidente retraso en el diálogo.', 3: 'Diálogo difícil.', 4: 'Torpeza absoluta.'}
    choices_9 = {0: 'Ninguna', 1: '"Juega" con sus manos, cabellos, etc.', 2: 'Se retuerce las manos, se'
                    ' muerde las uñas, los labios, se tira de los cabellos, etc.'}
    choices_10 = {0: 'No hay dificultad.', 1: 'Tensión subjetiva e irritabilidad.', 2: 'Preocupación por'
                     ' pequeñas cosas.',
                  3: 'Actitud aprensiva aparente en la expresión o en el habla.',
                  4: 'Terrores expresados sin preguntarle.'}
    choices_11 = {0: 'Ausente', 1: 'Ligera', 2: 'Moderada', 3: 'Grave', 4: 'Incapacitante'}
    choices_12 = {0: 'Ninguno', 1: 'Pérdida del apetito, pero come sin necesidad de que lo estimulen. Sensac'
                     'ión de pesadez en el abdomen.',
                  2: 'Dificultad en comer si no se le insiste. Solicita o nece'
                     'sita laxantes o medicación intestinal o para sus síntomas gastrointestinales.'}
    choices_13 = {0: 'Ninguno', 1: 'Pesadez en la extremidades, espalda o cabeza. Dorsalgias, cefalalgias, m'
                     'ialgias. Fatigabilidad y pérdida de energía.',
                  2: 'Cualquiera de los síntomas anteriores se '
                     'puntúa como 2 si está muy bien definido.'}
    choices_14 = {0: 'Ausentes', 1: 'Débiles.', 2: 'Graves', 3: 'Incapacitantes'}
    choices_15 = {0: 'No la hay.', 1: 'Preocupado de sí mismo (corporalmente).',
                  2: 'Preocupado por su salud.',
                  3: 'Se lamenta constantemente. Solicita ayudas, etc.',
                  4: 'Ideas delirantes hipocondríacas.'}
    choices_16 = {0: 'Pérdida de peso inferior a 500 g por semana (de promedio).',
                  1: 'Pérdida de peso de más de 500 g por semana (de promedio).',
                  2: 'Pérdida de peso de más de 1 kg por semana (de promedio).'}
    choices_17 = {0: 'Se da cuenta de que está deprimido y enfermo.', 1: 'Se da cuenta de su enfermedad pero'
                     ' atribuye la causa a la mala alimentación, clima, exceso de trabajo, virus, etc.',
                  2: 'Niega estar enfermo.'}

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.date.today)
    fecha_creacion = models.DateField(default=datetime.date.today)

    p1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p3 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p4 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p5 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p6 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p7 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p8 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p9 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p10 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p11 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p12 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p13 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p14 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p15 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p16 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    p17 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)

    observaciones = models.TextField(max_length=1000, null=True, blank=True)
    resultado = models.IntegerField(null=True)
    puntos = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    activo = models.BooleanField(null=False, default=True)
    objects = EscalaHamiltonManager()

    def delete(self):
        self.activo = False
        self.save()

    def save(self, *args, **kwargs):
        self.puntos = self.p1 + self.p2 + self.p3 + self.p4 + self.p5 + \
            self.p6 + self.p7 + self.p8 + self.p9 + self.p10 + self.p11 + \
            self.p12 + + self.p13 + self.p14 + self.p15 + self.p16 + self.p17
        super().save(*args, **kwargs)

    @property
    def interpretacion(self):
        self.resultado = self.puntos
        if self.resultado >= 0 and self.resultado <= 7:
            return "No deprimido"
        elif self.resultado >= 8 and self.resultado <= 13:
            return "Depresión ligera/menor"
        elif self.resultado >= 14 and self.resultado <= 18:
            return "Depresión moderada"
        elif self.resultado >= 19 and self.resultado <= 22:
            return "Depresión severa"
        elif self.resultado >= 23:
            return "Depresión muy severa"

    def __str__(self):
        return str(self.beneficiario) + " - Escala de Hamilton " + str(self.id)


class ConsultaMedicaManager(models.Manager):    # NEF-46
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class ConsultaMedica(models.Model):  # NEF-46

    class Meta:
        verbose_name = 'Consulta Médica'
        verbose_name_plural = 'Consulta Médica'

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=datetime.date.today)
    peso = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    talla = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])

    imc = models.DecimalField(verbose_name='IMC', max_digits=6, decimal_places=3, validators=[MinValueValidator(0)])
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    frecuencia_cardiaca = models.IntegerField(validators=[MinValueValidator(0)])
    frecuencia_respiratoria = models.IntegerField(validators=[MinValueValidator(0)])
    especificaciones = models.TextField(max_length=1000, null=True, blank=True)
    analisis_enfermedad = models.TextField(max_length=1000, null=True, blank=True)
    plan = models.TextField(max_length=1000, null=True, blank=True)
    tratamiento = models.TextField(max_length=1000, null=True, blank=True)
    observaciones = models.TextField(max_length=1000, null=True, blank=True)

    presion_sistolica = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], default=120)
    presion_diastolica = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], default=80)

    activo = models.BooleanField(null=False, default=True)
    objects = ConsultaMedicaManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        enfermedades(self.beneficiario, self)

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    def __str__(self):
        return str(self.beneficiario) + " - Consulta Médica " + str(self.id)


def gfr_estimada(qs):
    today = date.today()
    beneficiario = Beneficiario.objects.get(id=qs.beneficiario.id)
    edad = beneficiario.edad
    gfr = 175 * (float(qs.creatinina)**(-1.154)) * (edad**(-0.203))
    if not beneficiario.sexo:
        gfr = gfr * 0.742
    if beneficiario.afroamericano:
        gfr = gfr * 1.212
    return gfr


def gfr_ckd_epi(qs):
    today = date.today()
    born = Beneficiario.objects.get(id=qs.beneficiario.id).fecha_nacimiento
    edad = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    if qs.beneficiario.sexo:
        k = 0.9
        a = -0.411
    else:
        k = 0.7
        a = -0.329
    gfr = 141 * (min(float(qs.creatinina) / k, 1) ** a) * (max(float(qs.creatinina) / k, 1) ** (-1.209)) * (
        0.993 ** edad)
    if not qs.beneficiario.sexo:
        gfr = gfr * 1.018
    if qs.beneficiario.afroamericano:
        gfr = gfr * 1.159
    return gfr


def gfr_clasification(gfr):
    if gfr >= 90:
        return "G1"
    elif 60 <= gfr < 90:
        return "G2"
    elif 45 <= gfr < 60:
        return "G3a"
    elif 30 <= gfr < 45:
        return "G3b"
    elif 15 <= gfr < 30:
        return "G4"
    elif gfr < 15:
        return "G5"
    return "SC"


def albumina_clasification(albumina):
    if albumina < 30:
        return "A1"
    elif 30 <= albumina <= 300:
        return "A2"
    elif albumina > 300:
        return "A3"
    return "SC"

def enfermedades(beneficiario, consulta):
    if consulta.presion_sistolica >= 140 and consulta.presion_diastolica >= 90:
        if beneficiario.diabetico_hipertenso == 1 or beneficiario.diabetico_hipertenso == 3:
            beneficiario.diabetico_hipertenso = 3
            beneficiario.save()
        else:
            beneficiario.diabetico_hipertenso = 2
            beneficiario.save()
    else:
        pass

def clasification(beneficiario, qs, ma):
    if not qs.usado_para_estadificacion and not ma.usado_para_estadificacion:
        # TODO -> agregar la diferencia de fechas como parametro... no mayor a X dias
        qs.usado_para_estadificacion = True
        ma.usado_para_estadificacion = True
        qs.save()
        ma.save()
        gfr_estimada_aux = gfr_estimada(qs)
        gfr = gfr_ckd_epi(qs)
        categoria_gfr_estimada = gfr_clasification(gfr_estimada_aux)
        categoria_gfr = gfr_clasification(gfr)
        if(gfr<60):
            beneficiario.de_seguimiento = True
            beneficiario.save()
        albumina = ma.micro_albumina
        categoria_alb = albumina_clasification(albumina)
        activo = True
        aux = Clasificacion.objects.create(beneficiario=beneficiario,
                                        categoria_gfr_estimada=categoria_gfr_estimada,
                                        gfr_estimada=gfr_estimada_aux,
                                        categoria_gfr=categoria_gfr,
                                        gfr=gfr,
                                        categoria_alb=categoria_alb,
                                        albumina=albumina,
                                        id_qs=qs,
                                        id_ma=ma,
                                        activo=activo,
                                        fecha=date.today(),
                                        usuario=None)
        return True
    return False


class EvaluacionPlaticasManager(models.Manager):   # NEF-61
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class EvaluacionPlaticas(models.Model):  # NEF-58

    class Meta:
        verbose_name = 'Evaluación de platicas'
        verbose_name_plural = 'Evaluaciones de platicas'

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
    choices_1 = {0: 'Verdadero', 1: 'Falso'}
    choices_2 = {0: 'Verdadero', 1: 'Falso'}
    choices_3 = {1: 'Verdadero', 0: 'Falso'}
    choices_4 = {1: 'Verdadero', 0: 'Falso'}
    choices_5 = {1: 'Verdadero', 0: 'Falso'}
    choices_6 = {1: 'Sí ', 0: 'No'}
    choices_7 = {1: 'Sí ', 0: 'No'}
    choices_8 = {1: 'Sí ', 0: 'No'}
    choices_9 = {0: 'Evitar consultas ', 1: 'Platicar con los vecinos', 2: 'Preguntar al médico sin miedo'}
    choices_10 = {0: 'Disfrutar de la vida', 1: 'Las pérdidas significativas en la vida', 2: 'Ganar salud'}
    choices_11 = {1: 'Familia, medicos y sociedad integrados ', 0: 'Servicios de salud', 2: 'Apoyos de gobierno'}

    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.date.today)
    fecha_creacion = models.DateField(default=datetime.date.today)
    p1 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p2 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p3 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p4 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p5 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p6 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p7 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p8 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p9 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p10 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)
    p11 = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(5)], default=1)

    activo = models.BooleanField(null=False, default=True)
    objects = EvaluacionPlaticasManager()

    def delete(self):
        self.activo = False
        self.save()

    def __str__(self):
        return str(self.id) + " - Evaluación de platicas " + str(self.id)


class NotasManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class Notas(models.Model):

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=datetime.date.today)
    nota = models.TextField(max_length=6000)

    activo = models.BooleanField(null=False, default=True)
    objects = NotasManager()

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

    def __str__(self):
        return str(self.beneficiario) + " - Nota " + str(self.id)



class RegistroMensualManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class RegistroMensual(models.Model):

    class Meta:
        verbose_name = 'Hoja de registro mensual'
        verbose_name_plural = 'Hojas de registro mensual'

    labels = {
        'fecha': 'Fecha de realización:',
        'p1': 'Médica:',
        'p2': 'Nutricional:',
        'p3': 'Estilo de vida:',
        'observaciones': 'Observaciones:'
    }
    choices_1 = {2: 'Sí', 0: 'No', 1: 'Parcialmente'}

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.date.today)
    fecha_creacion = models.DateField(default=datetime.date.today)

    p1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    p2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    p3 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    observaciones = models.TextField(max_length=1000, null=True, blank=True)
    resultado = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    activo = models.BooleanField(null=False, default=True)
    objects = RegistroMensualManager()

    def delete(self):
        self.activo = False
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.resultado = self.p1+self.p2+self.p3
        super().save(*args, **kwargs)

    @property
    def interpretacion(self):
        if self.resultado >= 0 and self.resultado <= 2:
            return "Mala"
        elif self.resultado > 2 and self.resultado <= 4:
            return "Regular"
        elif self.resultado > 4:
            return "Buena"

    def __str__(self):
        return str(self.beneficiario) + " - Hoja de registro mensual " + str(self.id)