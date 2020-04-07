from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.admin.models import LogEntry
from django.urls import *


# Register your models here.
@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin): 
    actions = None
    form = FormularioForm
    exclude = ()

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse_lazy('Doctores:evaluaciones'))

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Doctores:evaluaciones'))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(FormularioAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin): 
    actions = None
    exclude = ()

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse_lazy('Doctores:evaluaciones'))
        
    def response_change(self, request, obj):
        return redirect(reverse_lazy('Doctores:evaluaciones'))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(EvaluacionAdmin, self).changeform_view(request, object_id, extra_context=extra_context)