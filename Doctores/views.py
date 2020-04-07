from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http import *
from django.urls import *
from Beneficiarios.models import *
from Formularios.models import *
from Proyectos.models import *
from .models import *
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import date
import sweetify
from sweetify.views import SweetifySuccessMixin
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.db.models import Avg, Min, Max
from .forms import *
import sweetify
from sweetify.views import SweetifySuccessMixin
from django.core.serializers import serialize
from django.db.models import ProtectedError

# Create your views here.


class ReportesView(PermissionRequiredMixin, TemplateView):  # NEF-206
    permission_required = ('Reportes.view_reportes')
    model = Evaluacion
    template_name = "Reportes/reportes_view_doc.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formularios"] = Formulario.objects.all()
        context["evaluaciones"] = Evaluacion.objects.all()

        return context


class ReportesEvaluacionView(PermissionRequiredMixin, TemplateView):  # NEF-206, NEF-207, NEF-208
    permission_required = ('Reportes.view_reportes')
    model = Evaluacion
    template_name = "Reportes/reportes_view_doc.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formularios"] = Formulario.objects.all()
        context["evaluaciones"] = Evaluacion.objects.all()
        evaluacion = self.kwargs.pop(
            'evaluacion')
        context["evaluacion"] = get_object_or_404(Evaluacion, pk=evaluacion)
        if context["evaluacion"]:

            formularios = Formulario.objects.filter(evaluacion=evaluacion)

            context["p_minimo"] = formularios.aggregate(Min('p1'))["p1__min"]
            context["p_maximo"] = formularios.aggregate(Max('p1'))["p1__max"]

            context["p_promedio"] = formularios.aggregate(Avg('p1'))["p1__avg"]


            formularios_inicial = formularios.filter(periodo=False).values(
                'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 'p19', 'p20')


            context["evaluacion_inicial"] = formularios_inicial
            context["evaluacion_inicial_count"] = formularios_inicial.count()

            formularios_final = formularios.filter(periodo=True).values(
                'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p17', 'p18', 'p19', 'p20')


            context["evaluacion_final"] = formularios_final
            context["evaluacion_final_count"] = formularios_final.count()

            context["correctas_inicial"], context["incorrectas_inicial"] = evaluate_data(formularios_inicial)
            context["correctas_final"], context["incorrectas_final"]  = evaluate_data(formularios_final)

        return context


def evaluate_data(datos):
    correct = []
    incorrect = []
    for formulario in datos:
        zippend((correct, incorrect), evaluate_questions(formulario))
    res_correct = [sum(x) for x in zip(*correct)]
    res_incorrect = [sum(x) for x in zip(*incorrect)]
    return res_correct, res_incorrect

def evaluate_questions(formulario):
    correct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    incorrect = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    current = 0
    for question in formulario.values():
        if question == -1:
            correct[current] += 1
        else:
            incorrect[current] += 1
        current += 1
        current = current%20
    
    return correct, incorrect

def zippend(lists, values):
  assert len(lists) == len(values)
  for l,v in zip(lists, values):
    l.append(v)


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


class EvaluacionesList(PermissionRequiredMixin, TemplateView):
    permission_required = "Doctores.view_evaluacion"
    template_name = "Doctores/evaluaciones_list.html"


class EvaluacionesListJson(PermissionRequiredMixin, BaseDatatableView):  # NEF-34
    permission_required = "Doctores.view_evaluacion"
    model = Evaluacion

    def render_column(self, row, column):
        if column == 'nombre':
            return '<a href=/capacitaciones/evaluacion/' + str(row.id) + '>' + row.nombre + '</a>'
        elif column == 'fecha':
            return row.fecha
        elif column == 'editar':
            return '<a href=/admin/Doctores/evaluacion/' + str(row.id) +'/change/ > <i class="far fa-edit"></i> </a>'
        else:
            return super(EvaluacionesListJson, self).render_column(row, column)


class EvaluacionCreate(PermissionRequiredMixin, CreateView):  # NEF-21
    permission_required = "Doctores.add_evaluacion"
    model = Evaluacion
    form_class = EvaluacionForm

    def form_valid(self, form):
        form.save()
        return super(EvaluacionCreate, self).form_valid(form)

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse_lazy('Doctores:evaluaciones')


# class JornadaDelete(PermissionRequiredMixin, DeleteView):  # NEF-23
#     permission_required = "Proyectos.delete_jornada"
#     model = Jornada
#     success_url = reverse_lazy('Proyectos:jornadas')

#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         success_url = self.get_success_url()

#         try:
#             self.object.delete()
#         except ProtectedError:
#             redirect(success_url)
#         return HttpResponseRedirect(success_url)


