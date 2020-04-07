from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import *
from django.urls import *
from Beneficiarios.models import *
from .models import *
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import date
from .forms import *
import sweetify
from sweetify.views import SweetifySuccessMixin
from django.core.serializers import serialize
from django.db.models import ProtectedError


class JornadaView(PermissionRequiredMixin, TemplateView):  # NEF-26
    permission_required = "Proyectos.view_jornada"
    model = Jornada
    template_name = "Proyectos/jornadas_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jornadas = Jornada.objects.all()
        context['jornada'] = jornadas
        return context


class JornadaDetailView(PermissionRequiredMixin, DetailView):  # NEF-27
    permission_required = "Proyectos.view_jornada"
    model = Jornada
    template_name = "Proyectos/jornadas_detail.html"

    def get_context_data(self, **kwargs):
        context = super(JornadaDetailView, self).get_context_data(**kwargs)
        id = self.kwargs["pk"]
        jornada = Jornada.objects.get(id=id)
        beneficiarios = len(Beneficiario.objects.filter(jornada=id))
        context["jornada"] = jornada
        context["beneficiario"] = beneficiarios
        if beneficiarios != 0:
            context['vacio'] = False
        else:
            context['vacio'] = True
        return context


class JornadasList(PermissionRequiredMixin, TemplateView):
    permission_required = "Proyectos.view_jornada"
    template_name = "Proyectos/jornadas_list.html"


class JornadasListJson(PermissionRequiredMixin, BaseDatatableView):  # NEF-34
    permission_required = "Proyectos.view_jornada"
    model = Jornada

    def render_column(self, row, column):
        if column == 'nombre':
            return '<a href=/jornadas/' + str(row.id) + '>' + row.nombre + '</a>'
        elif column == 'fecha':
            return row.fecha
        elif column == 'estado':
            return row.estado
        elif column == 'municipio':
            return row.municipio
        elif column == 'localidad':
            return row.localidad
        elif column == 'beneficiarios':
            beneficiarios = len(Beneficiario.objects.filter(jornada=row.id))
            return beneficiarios
        else:
            return super(JornadasListJson, self).render_column(row, column)


class JornadaCreate(PermissionRequiredMixin, CreateView):  # NEF-21
    permission_required = "Proyectos.add_jornada"
    model = Jornada
    form_class = JornadaForm

    def form_valid(self, form):
        form.save()
        return super(JornadaCreate, self).form_valid(form)

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse_lazy('Proyectos:jornadas')


class JornadaDelete(PermissionRequiredMixin, DeleteView):  # NEF-23
    permission_required = "Proyectos.delete_jornada"
    model = Jornada
    success_url = reverse_lazy('Proyectos:jornadas')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            redirect(success_url)
        return HttpResponseRedirect(success_url)
