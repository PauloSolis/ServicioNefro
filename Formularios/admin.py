from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import *
from django.shortcuts import redirect
from .forms import *
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.admin.models import LogEntry
from django.urls import *


@admin.register(LogEntry)
class BitacoraCambios(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# Register your models here.
@admin.register(QuimicaSanguinea)
class QuimicaSanguineaAdmin(admin.ModelAdmin):  # NEF-68, NEF-69
    actions = None
    exclude = ('beneficiario', 'fecha_creacion', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:vqs', kwargs={'quimicaSanguinea': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(QuimicaSanguineaAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(Microalbuminuria)
class MicroalbuminuriaAdmin(admin.ModelAdmin):  # NEF-78
    actions = None
    form = MicroalbuminuriaForm
    exclude = ('beneficiario', 'fecha_creacion', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_microalbuminuria', kwargs={'microalbuminuria': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(MicroalbuminuriaAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(HemoglobinaGlucosilada)
class HemoglobinaGlucosiladaAdmin(admin.ModelAdmin):
    actions = None
    form = HemoglobinaGlucosiladaForm
    exclude = ('beneficiario', 'fecha_captura', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_hemoglobinaglucosilada',
                                     kwargs={'hemoglobinaglucosilada': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(HemoglobinaGlucosiladaAdmin, self).changeform_view(request, object_id,
                                                                        extra_context=extra_context)


@admin.register(GlucosaCapilar)
class GlucosaCapilarAdmin(admin.ModelAdmin):  # NEF-82
    actions = None
    form = GlucosaCapilarForm
    exclude = ('beneficiario', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_glucosacapilar', kwargs={'glucosacapilar': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(GlucosaCapilarAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(FactorDeRiesgo)
class FactorDeRiesgoAdmin(admin.ModelAdmin):  # NEF-592 NEF-153
    actions = None
    form = FactorDeRiesgoForm
    exclude = ('beneficiario', 'fecha_creacion', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_factorderiesgo', kwargs={'factorderiesgo': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(FactorDeRiesgoAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(TamizajeNutricional)
class TamizajeNutricionalAdmin(admin.ModelAdmin):
    actions = None
    form = TamizajeNutricionalForm
    exclude = ('beneficiario', 'fecha', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_tamizajenutricional', kwargs={'tamizajenutricional': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(TamizajeNutricionalAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(MalnutricionInflamacion)
class MalnutricionInflamacionAdmin(admin.ModelAdmin):  # NEF-52
    actions = None
    form = MalnutricionInflamacionForm
    exclude = ('beneficiario', 'fecha_creacion', 'resultado', 'imc_valor', 'imc_puntos', 'talla', 'peso', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_malnutricioninflamacion',
                                     kwargs={'malnutricioninflamacion': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(MalnutricionInflamacionAdmin, self).changeform_view(request, object_id,
                                                                         extra_context=extra_context)


@admin.register(Clasificacion)
class ClasificacionAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EscalaHamilton)
class EscalaHamiltonAdmin(admin.ModelAdmin):  # NEF-56
    actions = None
    form = EscalaHamiltonForm
    exclude = ('beneficiario', 'fecha_creacion', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_escalahamilton',
                                     kwargs={'escalaHamilton': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(EscalaHamiltonAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(ConsultaMedica)
class ConsultaMedicaAdmin(admin.ModelAdmin):  # NEF-48
    actions = None
    exclude = ('beneficiario', 'fecha_creacion', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_consultamedica', kwargs={'consultamedica': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(ConsultaMedicaAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(AdherenciaTratamiento)
class EscalaAdherenciaAdmin(admin.ModelAdmin):  # NEF-60
    actions = None
    form = AdherenciaTratamientoForm
    exclude = ('beneficiario', 'fecha_creacion', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(EscalaAdherenciaAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):  # NEF-60
    actions = None
    form = EvidenciaForm
    exclude = ('beneficiario', 'fecha_creacion', 'fecha_subida', 'urn', 'existe', 'usuario')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(EvidenciaAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(EvaluacionPlaticas)
class EvaluacionPlaticasAdmin(admin.ModelAdmin):  # NEF-60
    actions = None
    form = EvaluacionPlaticasForm

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse_lazy('Proyectos:jornadas_detail', kwargs={'pk': obj.jornada.id}))

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Proyectos:jornadas_detail', kwargs={'pk': obj.jornada.id}))

@admin.register(Notas)
class NotasAdmin(admin.ModelAdmin):  # NEF-48
    actions = None
    exclude = ('beneficiario', 'fecha_creacion', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_notas', kwargs={'nota': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(NotasAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

@admin.register(RegistroMensual)
class RegistroMensualAdmin(admin.ModelAdmin):  # NEF-60
    actions = None
    form = RegistroMensualForm
    exclude = ('beneficiario', 'fecha_creacion', 'activo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Formularios:view_registromensual', kwargs={'registromensual': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(RegistroMensualAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
