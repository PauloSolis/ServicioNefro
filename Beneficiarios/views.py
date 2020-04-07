from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models.expressions import RawSQL
from .models import *
from .forms import *
from Formularios.models import *
from Formularios.forms import *
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Max
from datetime import date
from django.contrib.auth.mixins import PermissionRequiredMixin
import sweetify
from sweetify.views import SweetifySuccessMixin
from chartjs.views.lines import BaseLineChartView



class BeneficiariosNew(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-29
    permission_required = ('Beneficiarios.add_beneficiario')
    model = Beneficiario
    form_class = BeneficiarioForm
    success_message = "Registro existoso"
    sweetify_options = {
        'buttons': False,
        'timer': 1500,
        'allowOutsideClick': True,
        'confirmButtonText': 'OK',
        'icon': 'success',
        'closeModal': False,
        'text': " "
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jornada'] = get_object_or_404(Jornada, pk=self.kwargs.pop('id_jornada'))
        return context

    def form_valid(self, form):
        form.save()
        return super(BeneficiariosNew, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario', args=[self.object.id])


class BeneficiariosDetailView(PermissionRequiredMixin, DetailView):  # NEF-35, NEF-31
    permission_required = "Beneficiarios.view_beneficiario"
    model = Beneficiario

    def get_context_data(self, **kwargs):
        context = super(BeneficiariosDetailView, self).get_context_data(**kwargs)
        id = self.kwargs["pk"]
        antecedentes = Antecedentes.objects.filter(beneficiario=id)
        context["antecedentes"] = antecedentes if len(antecedentes) > 0 else None

        clasificacion = Clasificacion.objects.filter(beneficiario=id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        quimica_sanguinea = QuimicaSanguinea.objects.filter(beneficiario=id).order_by('-id')
        context["quimica_sanguinea"] = quimica_sanguinea[0] if len(quimica_sanguinea) > 0 else None

        microalbuminuria = Microalbuminuria.objects.filter(beneficiario=id).order_by('-id')
        context["microalbuminuria"] = microalbuminuria[0] if len(microalbuminuria) > 0 else None

        hemoglobina_glucosilada = HemoglobinaGlucosilada.objects.filter(beneficiario=id).order_by('-id')
        context["hemoglobina_glucosilada"] = hemoglobina_glucosilada[0] if len(hemoglobina_glucosilada) > 0 else None

        glucosa_capilar = GlucosaCapilar.objects.filter(beneficiario=id).order_by('-id')
        context["glucosa_capilar"] = glucosa_capilar[0] if len(glucosa_capilar) > 0 else None

        tamizaje_nutricional = TamizajeNutricional.objects.filter(beneficiario=id).order_by('-id')
        context["tamizaje_nutricional"] = tamizaje_nutricional[0] if len(tamizaje_nutricional) > 0 else None

        adherencia_Tratamiento = AdherenciaTratamiento.objects.filter(beneficiario=id).order_by('-id')
        context["adherencia_Tratamiento"] = adherencia_Tratamiento[0] if len(adherencia_Tratamiento) > 0 else None

        malnutricion_inflamacion = MalnutricionInflamacion.objects.filter(beneficiario=id).order_by('-id')
        context["malnutricion_inflamacion"] = \
            malnutricion_inflamacion[0] if len(malnutricion_inflamacion) > 0 else None

        factor_de_riesgo = FactorDeRiesgo.objects.filter(beneficiario=id).order_by('-id')
        context["factor_de_riesgo"] = factor_de_riesgo[0] if len(factor_de_riesgo) > 0 else None

        escala_hamilton = EscalaHamilton.objects.filter(beneficiario=id).order_by('-id')
        context["escala_hamilton"] = escala_hamilton[0] if len(escala_hamilton) > 0 else None

        consulta_medica = ConsultaMedica.objects.filter(beneficiario=id).order_by('-id')
        context["consulta_medica"] = consulta_medica[0] if len(consulta_medica) > 0 else None

        nota = Notas.objects.filter(beneficiario=id).order_by('-id')
        context["nota"] = nota[0] if len(nota) > 0 else None

        registro_mensual = RegistroMensual.objects.filter(beneficiario=id).order_by('-id')
        context["registro_mensual"] = registro_mensual[0] if len(registro_mensual) > 0 else None
        return context


class BeneficiariosList(PermissionRequiredMixin, TemplateView):  # NEF-34
    permission_required = "Beneficiarios.view_beneficiario"
    template_name = 'Beneficiarios/beneficiarios_list.html'


class BeneficiariosListJson(PermissionRequiredMixin, BaseDatatableView):  # NEF-34
    permission_required = "Beneficiarios.view_beneficiario"
    model = Beneficiario

    def render_column(self, row, column):
        if column == 'edad':
            today = date.today()
            born = Beneficiario.objects.get(id=row.id).fecha_nacimiento
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        elif column == 'nombre':
            return '<a href=/beneficiarios/' + str(row.id) + '>' + row.nombre + '</a>'
        elif column == 'apellido_paterno':
            return '<a href=/beneficiarios/' + str(row.id) + '>' + row.apellido_paterno + '</a>'
        elif column == 'apellido_materno':
            return '<a href=/beneficiarios/' + str(row.id) + '>' + row.apellido_materno + '</a>'
        elif column == 'sexo':
            return 'Hombre' if row.sexo else 'Mujer'
        elif column == 'de_seguimiento':
            return '<span class="fas fa-tag">' if row.de_seguimiento else 'No'
        elif column == 'clasificacion':
            clasificacion = Clasificacion.objects.filter(beneficiario=row.id)
            if clasificacion.exists():
                clasificacion = clasificacion.latest('id')
                clasificacion_html = '<div class="circle-sm mr-2 ' + clasificacion.color + '-bg"></div>'
                if clasificacion.discrepancia:
                    clasificacion_html += ('<span>(%s, %s) %s</span> ' %
                                           (clasificacion.categoria_gfr,
                                            clasificacion.categoria_gfr_estimada,
                                            clasificacion.categoria_alb))
                else:
                    clasificacion_html += \
                        '<span>' + clasificacion.categoria_gfr + ' ' + clasificacion.categoria_alb + '</span>'
                return clasificacion_html
            else:
                return 'Sin datos'
        elif column == 'activo':
            if row.activo:
                return '<a href=/beneficiarios/' + str(row.id) + '>' + "Activo" + '</a>'
            else:
                return '<a href=/beneficiarios/' + str(row.id) + '>' + "Inactivo" + '</a>'
        else:
            return super(BeneficiariosListJson, self).render_column(row, column)

    def filter_queryset(self, qs):  # NEF-39
        qs = super().filter_queryset(qs)

        categoria = self.request.GET.get('categoria', None)
        jornada = self.request.GET.get('jornada', None)
        # TODO: Change to QuerySet so the limit is applied before retrieving the latest ids.
        if categoria:
            if categoria == 'discrepancia':
                qs = qs.filter(id__in=RawSQL('''select cb.beneficiario_id as id
                                                from (select beneficiario_id, MAX(id) as id
                                                from "Formularios_clasificacion" group by beneficiario_id) as cb,
                                                "Formularios_clasificacion" as cc where cb.id = cc.id
                                                and cc.categoria_gfr <> cc.categoria_gfr_estimada''', []))
            elif categoria == 'Sin datos':
                qs = Beneficiario.objects.filter(clasificacion=None)
            else:
                qs = qs.filter(id__in=RawSQL('''select cb.beneficiario_id as id
                                                from (select beneficiario_id, MAX(id) as id
                                                from "Formularios_clasificacion" group by beneficiario_id) as cb,
                                                "Formularios_clasificacion" as cc where cb.id = cc.id
                                                and cc.categoria_gfr = cc.categoria_gfr_estimada and
                                                cc.categoria_gfr LIKE %s''', [categoria + '%']))

        if jornada:
            qs = qs.filter(jornada=jornada)
        return qs


class AntecedentesNew(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-29
    permission_required = ('Formularios.add_antecedente')
    model = Antecedentes
    success_message = "Registro existoso para %(beneficiario)s"
    sweetify_options = {
        'buttons': False,
        'timer': 1500,
        'allowOutsideClick': True,
        'confirmButtonText': 'OK',
        'icon': 'success',
        'closeModal': False,
        'text': " "
    }
    form_class = AntecedentesForm

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def get_context_data(self, **kwargs):
        context = super(AntecedentesNew, self).get_context_data(**kwargs)
        context['beneficiario'] = Beneficiario.objects.get(id=self.kwargs['id'])
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'])
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def dispatch(self, request, *args, **kwargs):
        self.beneficiario = get_object_or_404(Beneficiario, pk=kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        form.instance.beneficiario = self.beneficiario
        form.save()
        return super(AntecedentesNew, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario', args=[self.object.beneficiario.id])


class BeneficiariosRecordView(PermissionRequiredMixin, DetailView):  # NEF-36
    permission_required = "Beneficiarios.view_beneficiario"
    model = Beneficiario
    template_name = 'Beneficiarios/beneficiario_record.html'

    def get_context_data(self, **kwargs):
        context = super(BeneficiariosRecordView, self).get_context_data(**kwargs)
        id = self.kwargs["pk"]
        antecedentes = Antecedentes.objects.filter(beneficiario=id)
        context["antecedentes"] = antecedentes if len(antecedentes) > 0 else None

        factor_de_riesgo = FactorDeRiesgo.objects.filter(beneficiario=id).order_by('-id')
        context["factor_de_riesgo"] = factor_de_riesgo[0] if len(factor_de_riesgo) > 0 else None

        clasificacion = Clasificacion.objects.filter(beneficiario=id).order_by('-id')
        context["clasification"] = clasificacion if len(clasificacion) > 0 else None
        context["clasificacion"] = clasificacion[0] if len(clasificacion) > 0 else None

        tamizaje_nutricional = TamizajeNutricional.objects.filter(beneficiario=id).order_by('-id')
        context["tamizaje_nutricional"] = tamizaje_nutricional if len(tamizaje_nutricional) > 0 else None

        quimica_sanguinea = QuimicaSanguinea.objects.filter(beneficiario=id).order_by('-id')
        context["quimica_sanguinea"] = quimica_sanguinea if len(quimica_sanguinea) > 0 else None

        microalbuminuria = Microalbuminuria.objects.filter(beneficiario=id).order_by('-id')
        context["microalbuminuria"] = microalbuminuria if len(microalbuminuria) > 0 else None

        hemoglobina_glucosilada = HemoglobinaGlucosilada.objects.filter(beneficiario=id).order_by('-id')
        context["hemoglobina_glucosilada"] = hemoglobina_glucosilada if len(hemoglobina_glucosilada) > 0 else None

        glucosa_capilar = GlucosaCapilar.objects.filter(beneficiario=id).order_by('-id')
        context["glucosa_capilar"] = glucosa_capilar if len(glucosa_capilar) > 0 else None

        consulta_medica = ConsultaMedica.objects.filter(beneficiario=id).order_by('-id')
        context["consulta_medica"] = consulta_medica if len(consulta_medica) > 0 else None

        adherencia_Tratamiento = AdherenciaTratamiento.objects.filter(beneficiario=id).order_by('-id')
        context["adherencia_Tratamiento"] = adherencia_Tratamiento if len(adherencia_Tratamiento) > 0 else None

        escala_hamilton = EscalaHamilton.objects.filter(beneficiario=id).order_by('-id')
        context["escala_hamilton"] = escala_hamilton if len(escala_hamilton) > 0 else None

        malnutricion_inflamacion = MalnutricionInflamacion.objects.filter(beneficiario=id).order_by('-id')
        context["malnutricion_inflamacion"] = \
            malnutricion_inflamacion if len(malnutricion_inflamacion) > 0 else None

        notas = Notas.objects.filter(beneficiario=id).order_by('-id')
        context["notas"] = notas if len(notas) > 0 else None

        registro_mensual = RegistroMensual.objects.filter(beneficiario=id).order_by('-id')
        context["registro_mensual"] = registro_mensual if len(registro_mensual) > 0 else None

        #context['form'] = MalnutricionInflamacionForm

        return context



class rEstJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = Clasificacion

    def get_labels(self):
        id = self.kwargs["pk"]   
        clasificacion = Clasificacion.objects.filter(beneficiario=id)
        aux = []
        aux.append('Inicio')
        for e in clasificacion:
            aux.append(e.categoria_gfr)
        aux.append('Fin')
        return aux

    def get_providers(self):
        return ["Nivel"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        clasificacion = Clasificacion.objects.filter(beneficiario=id)
        level = [] 
        level.append(0)
        for e in clasificacion:
            cat = e.categoria_gfr
            if cat == 'G1':
                level.append(1)
            elif cat == 'G2':
                level.append(2)
            elif cat == 'G3a':
                level.append(2.8)
            elif cat == 'G3b':
                level.append(3.2)
            elif cat == 'G4':
                level.append(4)
            elif cat == 'G5':
                level.append(5)
        return [level]


class rTamJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = TamizajeNutricional

    def get_labels(self):
        id = self.kwargs["pk"]   
        tamizaje_nutricional = TamizajeNutricional.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in tamizaje_nutricional:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Sistólica", "Diastólica", "Peso", "Talla","Brazo","Bicipital","Tricipital", "IMC"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        tamizaje_nutricional = TamizajeNutricional.objects.filter(beneficiario=id).order_by('id')

        presion_sistolica = [] 
        presion_diastolica = [] 
        peso = [] 
        talla = [] 
        circunferencia_brazo = [] 
        pliegue_bicipital = [] 
        pliegue_tricipital = [] 
        imc = [] 
        
        presion_sistolica.append(0)
        presion_diastolica.append(0)
        peso.append(0)
        talla.append(0)
        circunferencia_brazo.append(0)
        pliegue_bicipital.append(0)
        pliegue_tricipital.append(0)
        imc.append(0)
        
        for e in tamizaje_nutricional:
            presion_sistolica.append(e.presion_sistolica)
            presion_diastolica.append(e.presion_diastolica)
            peso.append(e.peso)
            talla.append(e.talla)
            circunferencia_brazo.append(e.circunferencia_brazo)
            pliegue_bicipital.append(e.pliegue_bicipital)
            pliegue_tricipital.append(e.pliegue_tricipital)
            imc.append(e.imc)
        return [
            presion_sistolica,
            presion_diastolica,
            peso,
            talla,
            circunferencia_brazo,
            pliegue_bicipital,
            pliegue_tricipital,
            imc
        ]


class rQuiJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = QuimicaSanguinea

    def get_labels(self):
        id = self.kwargs["pk"]   
        quimica_sanguinea = QuimicaSanguinea.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in quimica_sanguinea:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Glucosa", "Urea", "Bun", "Creatinina","Ácido Úrico"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        quimica_sanguinea = QuimicaSanguinea.objects.filter(beneficiario=id).order_by('id')

        glucosa = [] 
        urea = [] 
        bun = [] 
        creatinina = [] 
        acido_urico = [] 

        glucosa.append(0)
        urea.append(0)
        bun.append(0)
        creatinina.append(0)
        acido_urico.append(0)
        
        for e in quimica_sanguinea:
            glucosa.append(e.glucosa)
            urea.append(e.urea)
            bun.append(e.bun)
            creatinina.append(e.creatinina)
            acido_urico.append(e.acido_urico)
        return [
            glucosa,
            urea,
            bun,
            creatinina,
            acido_urico
        ]
    

class rMicJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = Microalbuminuria

    def get_labels(self):
        id = self.kwargs["pk"]   
        micro_albuminuria = Microalbuminuria.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in micro_albuminuria:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Micro albumina", "Creatinina", "Relación"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        micro_albuminuria = Microalbuminuria.objects.filter(beneficiario=id).order_by('id')

        albumina = []
        creatinina = [] 
        relacion = [] 

        albumina.append(0)
        creatinina.append(0)
        relacion.append(0)
        
        for e in micro_albuminuria:
            albumina.append(e.micro_albumina)
            creatinina.append(e.creatinina)
            relacion.append(e.relacion)
        return [
            albumina,
            creatinina,
            relacion
        ]    

class rHemJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = HemoglobinaGlucosilada

    def get_labels(self):
        id = self.kwargs["pk"]   
        hemoglobina_glucosilada = HemoglobinaGlucosilada.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in hemoglobina_glucosilada:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Hemoglobina glucosilada"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        hemoglobina_glucosilada = HemoglobinaGlucosilada.objects.filter(beneficiario=id).order_by('id')

        hemoglobina = []

        hemoglobina.append(0)
        
        for e in hemoglobina_glucosilada:
            hemoglobina.append(e.hemoglobina_glucosilada)
        return [
            hemoglobina
        ]
    

class rGluJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = GlucosaCapilar

    def get_labels(self):
        id = self.kwargs["pk"]   
        glucosa_capilar = GlucosaCapilar.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in glucosa_capilar:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Glucosa"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        glucosa_capilar = GlucosaCapilar.objects.filter(beneficiario=id).order_by('id')

        glucosa = []

        glucosa.append(0)
        
        for e in glucosa_capilar:
            glucosa.append(e.glucosa)
        return [
            glucosa
        ]


class rConJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = ConsultaMedica

    def get_labels(self):
        id = self.kwargs["pk"]   
        consulta_medica = ConsultaMedica.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in consulta_medica:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Peso", "Talla", "IMC", "Temperatura", "Frecuencia cardiaca", "Frecuencia respiratoria", "Presión"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        consulta_medica = ConsultaMedica.objects.filter(beneficiario=id).order_by('id')

        peso = []
        talla = []
        imc = []
        temperatura = []
        card = []
        resp = []
        presion = []
        
        peso.append(0)
        talla.append(0)
        imc.append(0)
        temperatura.append(0)
        card.append(0)
        resp.append(0)
        presion.append(0)
        
        for e in consulta_medica:
            peso.append(e.peso)
            talla.append(e.talla)
            imc.append(e.imc)
            temperatura.append(e.temperatura)
            card.append(e.frecuencia_cardiaca)
            resp.append(e.frecuencia_respiratoria)
            presion.append(e.presion_sistolica/e.presion_diastolica)
        return [
            peso,
            talla,
            imc,
            temperatura,
            card,
            resp,
            presion
        ]
    

class rAdhJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = AdherenciaTratamiento

    def get_labels(self):
        id = self.kwargs["pk"]   
        adherencia_Tratamiento = AdherenciaTratamiento.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in adherencia_Tratamiento:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Resultado"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        adherencia_Tratamiento = AdherenciaTratamiento.objects.filter(beneficiario=id).order_by('id')

        resultado = []

        resultado.append(0)
        
        for e in adherencia_Tratamiento:
            resultado.append(e.resultado)
        return [
            resultado
        ]


class rHamJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = EscalaHamilton

    def get_labels(self):
        id = self.kwargs["pk"]   
        escala_hamilton = EscalaHamilton.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in escala_hamilton:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Resultado"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        escala_hamilton = EscalaHamilton.objects.filter(beneficiario=id).order_by('id')

        resultado = []

        resultado.append(0)
        
        for e in escala_hamilton:
            resultado.append(e.puntos)
        return [
            resultado
        ]


class rMalJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = MalnutricionInflamacion

    def get_labels(self):
        id = self.kwargs["pk"]   
        malnutricion_inflamacion = MalnutricionInflamacion.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in malnutricion_inflamacion:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Resultado"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        malnutricion_inflamacion = MalnutricionInflamacion.objects.filter(beneficiario=id).order_by('id')

        resultado = []

        resultado.append(0)
        
        for e in malnutricion_inflamacion:
            resultado.append(e.resultado)
        return [
            resultado
        ]


class rRegJSON(PermissionRequiredMixin, BaseLineChartView):
    permission_required = "Beneficiarios.view_beneficiario"
    model = RegistroMensual

    def get_labels(self):
        id = self.kwargs["pk"]   
        registro_mensual = RegistroMensual.objects.filter(beneficiario=id)
        aux = []
        aux.append('Aplicación #')
        i = 1
        for e in registro_mensual:
            aux.append(i)
            i += 1
        return aux

    def get_providers(self):
        return ["Resultado"]

    def get_data(self): 
        id = self.kwargs["pk"]   
        registro_mensual = RegistroMensual.objects.filter(beneficiario=id).order_by('id')

        resultado = []

        resultado.append(0)
        
        for e in registro_mensual:
            resultado.append(e.resultado)
        return [
            resultado
        ]

    
