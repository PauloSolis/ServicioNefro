from django.contrib import admin
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect


@admin.register(Jornada)  # NEF-31
class JornadaAdmin(admin.ModelAdmin):
    actions = None
    form = JornadaForm

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Proyectos:jornadas_detail',
                        kwargs={'pk': obj.id}))

    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(JornadaAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
