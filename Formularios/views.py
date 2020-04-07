from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.models import LogEntry, DELETION, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.http import *
from django.urls import *
from Beneficiarios.models import *
from .models import *
from .models import Evidencia
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import date
from .forms import *
import sweetify
from sweetify.views import SweetifySuccessMixin
from django.core.serializers import serialize
from nefrovida.settings import BUCKET
import json
from datetime import timedelta
from django_datatables_view.base_datatable_view import BaseDatatableView

from google.cloud import storage
from django.utils.text import slugify


class EvidenciaCreate(PermissionRequiredMixin, CreateView):  # NEF-99
    permission_required = ('Formularios.add_evidencia')
    model = Evidencia
    form_class = EvidenciaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")

        return context

    def form_valid(self, form):
        ALLOWED_MIME = ['image/jpeg', 'application/pdf', 'octed-stream/pdf', 'image/gif', 'image/png']
        MAX_SIZE = 15 * 1024 * 1024

        size = int(form.data.get('size'))
        tipo = form.data.get('tipo')

        if size > MAX_SIZE:
            return HttpResponse(json.dumps({'error': 'El archivo excede el tamaño máximo de 15MB'}),
                                content_type="application/json", status=400)

        if tipo not in ALLOWED_MIME:
            return HttpResponse(json.dumps({'error': 'Sólo se admiten imágenes y pdf.'}),
                                content_type="application/json", status=400)

        evidencia = form.save(commit=False)
        evidencia.usuario = self.request.user
        evidencia.save()

        bucket = storage.Client().get_bucket(BUCKET)
        blob = bucket.blob('evidencias/' + evidencia.urn)
        url = blob.create_resumable_upload_session(size=size, content_type=tipo)

        return HttpResponse(json.dumps({'url': url}), content_type="application/json", status=200)


class EvidenciaView(PermissionRequiredMixin, TemplateView):  # NEF-210
    permission_required = 'Formularios.view_evidencia'
    model = Evidencia
    template_name = "Formularios/evidencia_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=self.kwargs.pop(
            'beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def list_blobs(self, bucket_name):
        """Lists all the blobs in the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)

        blobs = bucket.list_blobs()
        return blobs


class EvidenciasList(PermissionRequiredMixin, TemplateView):
    permission_required = "Formularios.view_evidencia"
    template_name = "Formularios/evidencia_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


class EvidenciasListJson(PermissionRequiredMixin, BaseDatatableView):  # NEF-34
    permission_required = "Formularios.view_evidencia"
    model = Evidencia

    def get_initial_queryset(self):
        return Evidencia.objects.filter(beneficiario__exact=self.kwargs['pk'])

    def render_column(self, row, column):
        if column == 'nombre':
            return row.nombre
        elif column == 'fecha_creacion':
            return row.fecha_creacion.strftime('%d-%b-%Y')
        elif column == 'descripcion':
            return row.descripcion
        elif column == 'acciones':
            if row.urn:
                button = '<button type="button" class="btn btn-download" onclick ="downloadEvidence(' + str(
                    row.pk) + ')">Descargar</button> <button type="button" class="button btn btn-form"' \
                              ' onclick="deleteEvidence(' + str(row.pk) + ')">Eliminar</button>'

            else:
                button = '<button type="button" class="btn btn-form" onclick="deleteEvidence(' + str(
                    row.pk) + ')">Eliminar Evidencia</button>'
            return button
        else:
            return super(EvidenciaListJson, self).render_column(row, column)


class EvidenciaDelete(PermissionRequiredMixin, DeleteView):  # NEF-69
    permission_required = ('Formularios.delete_evidencia')

    model = Evidencia

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        if request.is_ajax():
            evi = request.POST.get('evi')
            evidencia = Evidencia.objects.get(pk=evi)
            bucket = storage.Client().get_bucket(BUCKET)
            blob = bucket.blob('evidencias/' + evidencia.urn)
            if blob.exists():
                blob.delete()
            evidencia.delete()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(evidencia).pk,
                object_id=evidencia.id,
                object_repr=str(evidencia),
                action_flag=DELETION)
            return HttpResponseRedirect("/beneficiarios/" + str(evidencia.beneficiario.pk))


class EvidenciaDownload(PermissionRequiredMixin, TemplateView):  # NEF-210
    permission_required = ('Formularios.view_evidencia')
    model = Evidencia

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            evi = request.GET.get('evi')
            evidencia = Evidencia.objects.get(pk=evi)
            bucket = storage.Client().get_bucket(BUCKET)
            blob = bucket.blob('evidencias/' + evidencia.urn)
            url = ""
            if blob.exists():
                url = blob.generate_signed_url(method="GET", expiration=timedelta(minutes=5))
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(evidencia).pk,
                object_id=evidencia.id,
                object_repr=str(evidencia),
                action_flag=ADDITION)
            if url != "":
                context = {
                    'success': True,
                    'evidence': evi,
                    'url': url,
                }
            else:
                context = {
                    'success': False,
                }
            return JsonResponse(context)


class QuimicaSanguineaCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-66
    permission_required = ('Formularios.add_quimicasanguinea')
    model = QuimicaSanguinea
    form_class = QuimicaSanguineaForm

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
    error_message = 'Existen errores'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def form_valid(self, form):
        # form.save()
        return super(QuimicaSanguineaCreate, self).form_valid(form)

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario', args=[self.kwargs.pop('beneficiario')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class QuimicaSanguineaView(PermissionRequiredMixin, TemplateView):  # NEF-67, NEF-68
    permission_required = ('Formularios.view_quimicasanguinea')
    model = QuimicaSanguinea
    template_name = "Formularios/quimicasanguinea_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quimicaSanguinea'] = get_object_or_404(QuimicaSanguinea, pk=self.kwargs.pop(
            'quimicaSanguinea'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['quimicaSanguinea'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)

        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class QuimicaSanguineaDelete(PermissionRequiredMixin, DeleteView):  # NEF-69
    permission_required = ('Formularios.delete_quimicasanguinea')

    model = QuimicaSanguinea

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class MicroalbuminuriaCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-74
    permission_required = 'Formularios.add_microalbuminuria'

    model = Microalbuminuria
    form_class = MicroalbuminuriaForm

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
    error_message = 'Existen errores'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(
            Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # form.save()
        return super(MicroalbuminuriaCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])


class MicroalbuminuriaDelete(PermissionRequiredMixin, DeleteView):  # NEF-79
    permission_required = ('Formularios.delete_microalbuminuria')

    model = Microalbuminuria

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class HemoglobinaGlucosiladaCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-70
    permission_required = ('Formularios.add_hemoglobinaglucosilada')
    model = HemoglobinaGlucosilada
    form_class = HemoglobinaGlucosiladaForm
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
    error_message = 'Existen errores'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(
            Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def form_valid(self, form):
        form.save()
        return super(HemoglobinaGlucosiladaCreate, self).form_valid(form)

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])


class HemoglobinaGlucosiladaView(PermissionRequiredMixin, TemplateView):  # NEF-71
    permission_required = ('Formularios.view_hemoglobinaglucosilada')
    model = HemoglobinaGlucosilada
    template_name = "Formularios/hemoglobinaglucosilada_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hemoglobinaglucosilada'] = get_object_or_404(HemoglobinaGlucosilada, pk=self.kwargs.pop(
            'hemoglobinaglucosilada'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['hemoglobinaglucosilada'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class MicroalbuminuriaView(PermissionRequiredMixin, TemplateView):  # NEF-77, # NEF-78
    permission_required = 'Formularios.view_microalbuminuria'

    model = Microalbuminuria
    template_name = "Formularios/microalbuminuria_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['microalbuminuria'] = get_object_or_404(Microalbuminuria, pk=self.kwargs.pop(
            'microalbuminuria'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['microalbuminuria'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class GlucosaCapilarCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-80
    permission_required = 'Formularios.add_glucosacapilar'

    model = GlucosaCapilar
    form_class = GlucosaCapilarForm

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
    error_message = 'Existen errores'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def form_valid(self, form):
        form.save()
        return super(GlucosaCapilarCreate, self).form_valid(form)

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario', args=[self.kwargs.pop('beneficiario')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class GlucosaCapilarView(PermissionRequiredMixin, TemplateView):  # NEF-81
    permission_required = 'Formularios.view_glucosacapilar'

    model = GlucosaCapilar
    template_name = "Formularios/glucosacapilar_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['glucosacapilar'] = get_object_or_404(GlucosaCapilar, pk=self.kwargs.pop(
            'glucosacapilar'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['glucosacapilar'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class FactorDeRiesgoCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-30
    permission_required = ('Formularios.add_factorderiesgo')
    model = FactorDeRiesgo
    form_class = FactorDeRiesgoForm

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
    error_message = 'Existen errores'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def form_valid(self, form):
        form.save()
        return super(FactorDeRiesgoCreate, self).form_valid(form)

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario', args=[self.kwargs.pop('beneficiario')])


class TamizajeNutricionalCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-62
    permission_required = 'Formularios.add_tamizajenutricional'
    model = TamizajeNutricional
    form_class = TamizajeNutricionalForm
    template_name = "Formularios/tamizajenutricional_form.html"
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
    error_message = 'Existen errores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(
            Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super(TamizajeNutricionalCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def get_sweetify_options(self):
        return self.sweetify_options

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class MalnutricionInflamacionCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-50
    permission_required = 'Formularios.add_malnutricioninflamacion'
    model = MalnutricionInflamacion
    form_class = MalnutricionInflamacionForm
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
    error_message = 'Existen errores'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def form_valid(self, form):
        self.object = form.save()
        return super(MalnutricionInflamacionCreate, self).form_valid(form)

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=self.kwargs.pop('beneficiario'))
        context['tamizajenutricional'] = \
            TamizajeNutricional.objects.filter(beneficiario=context['beneficiario'].id).latest('id')
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])


class MalnutricionInflamacionDelete(PermissionRequiredMixin, DeleteView):  # NEF-53
    permission_required = ('Formularios.delete_malnutricioninflamacion')

    model = MalnutricionInflamacion

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class AdherenciaTratamientoCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-58
    permission_required = 'Formularios.add_adherenciatratamiento'
    model = AdherenciaTratamiento
    form_class = AdherenciaTratamientoForm
    template_name = "Formularios/adherenciatratamiento_form.html"
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(
            Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def form_valid(self, form):
        form.save()
        return super(AdherenciaTratamientoCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class AdherenciaTratamientoView(PermissionRequiredMixin, TemplateView):  # NEF-59, # NEF-60
    permission_required = 'Formularios.view_adherenciatratamiento'

    model = AdherenciaTratamiento
    template_name = "Formularios/adherenciatratamiento_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adherenciatratamiento'] = get_object_or_404(AdherenciaTratamiento, pk=self.kwargs.pop(
            'adherenciatratamiento'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['adherenciatratamiento'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class MalnutricionInflamacionView(PermissionRequiredMixin, TemplateView):  # NEF-51, NEF-52
    permission_required = ('Formularios.view_malnutricioninflamacion')
    model = MalnutricionInflamacion
    template_name = "Formularios/malnutricioninflamacion_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['malnutricioninflamacion'] = get_object_or_404(MalnutricionInflamacion, pk=self.kwargs.pop(
            'malnutricioninflamacion'))
        context['beneficiario'] = get_object_or_404(Beneficiario,
                                                    pk=context['malnutricioninflamacion'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        context['form'] = MalnutricionInflamacionForm
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class FactorDeRiesgoView(PermissionRequiredMixin, TemplateView):  # NEF-154, NEF-592
    permission_required = ('Formularios.view_factorderiesgo')
    model = FactorDeRiesgo
    template_name = "Formularios/factorderiesgo_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['factorderiesgo'] = get_object_or_404(FactorDeRiesgo, pk=self.kwargs.pop(
            'factorderiesgo'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['factorderiesgo'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class ClasificacionCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-95
    http_method_names = ['post']
    permission_required = 'Formularios.add_clasificacion'
    model = Clasificacion

    def post(self, request, **kwargs):
        clasificacion = get_object_or_404(Clasificacion, pk=request.POST.get('clasificacion_id'))
        new_clasificacion = request.POST.get('clasificacion')
        if new_clasificacion == clasificacion.categoria_gfr or new_clasificacion == \
                clasificacion.categoria_gfr_estimada:
            clasificacion.pk = None
            clasificacion.fecha = datetime.date.today()
            clasificacion.categoria_gfr = clasificacion.categoria_gfr_estimada = new_clasificacion
            clasificacion.usuario = request.user
            clasificacion.save()
        return redirect(reverse_lazy("Beneficiarios:beneficiario", args=[kwargs['beneficiario']]))


class TamizajeNutricionalView(PermissionRequiredMixin, TemplateView):  # NEF-63, # NEF-64
    model = TamizajeNutricional
    template_name = 'Formularios/tamizajenutricional_view.html'
    permission_required = 'Formularios.view_tamizajenutricional'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tamizajenutricional'] = get_object_or_404(TamizajeNutricional, pk=self.kwargs.pop(
            'tamizajenutricional'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['tamizajenutricional'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class EscalaHamiltonCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-62
    permission_required = 'Formularios.add_escalahamilton'
    model = EscalaHamilton
    form_class = EscalaHamiltonForm
    template_name = "Formularios/escalahamilton_form.html"
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
    error_message = 'Existen errores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(
            Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super(EscalaHamiltonCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def get_sweetify_options(self):
        return self.sweetify_options

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class ConsultaMedicaCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-46
    permission_required = 'Formularios.add_consultamedica'
    model = ConsultaMedica
    form_class = ConsultaMedicaForm
    template_name = "Formularios/consultamedica_form.html"
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
    error_message = 'Existen errores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(
            Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        tamizaje = TamizajeNutricional.objects.filter(beneficiario=context['beneficiario'].id)
        if tamizaje.exists():
            context['tamizaje'] = tamizaje.latest('id')

        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super(ConsultaMedicaCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def get_sweetify_options(self):
        return self.sweetify_options

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class ConsultaMedicaView(PermissionRequiredMixin, TemplateView):  # NEF-47, NEF-48
    permission_required = ('Formularios.view_consultamedica')
    model = ConsultaMedica
    template_name = "Formularios/consultamedica_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consultamedica'] = get_object_or_404(ConsultaMedica, pk=self.kwargs.pop(
            'consultamedica'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['consultamedica'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class ConsultaMedicaDelete(PermissionRequiredMixin, DeleteView):  # NEF-49
    permission_required = ('Formularios.delete_consultamedica')

    model = ConsultaMedica

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class EscalaHamiltonView(PermissionRequiredMixin, TemplateView):  # NEF-55, # NEF-56
    permission_required = ('Formularios.view_escalahamilton')
    model = EscalaHamilton
    template_name = "Formularios/escalahamilton_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['escalahamilton'] = get_object_or_404(EscalaHamilton, pk=self.kwargs.pop(
            'escalaHamilton'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['escalahamilton'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class FactorDeRiesgoDelete(PermissionRequiredMixin, DeleteView):  # NEF-153
    permission_required = ('Formularios.delete_factorderiesgo')

    model = FactorDeRiesgo

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class TamizajeNutricionalDelete(PermissionRequiredMixin, DeleteView):  # NEF-65
    permission_required = ('Formularios.delete_tamizajenutricional')

    model = TamizajeNutricional

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class GlucosaCapilarDelete(PermissionRequiredMixin, DeleteView):  # NEF-65
    permission_required = ('Formularios.delete_glucosacapilar')

    model = GlucosaCapilar

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class HemoglobinaGlucosiladaDelete(PermissionRequiredMixin, DeleteView):  # NEF-73
    permission_required = ('Formularios.delete_hemoglobinaglucosilada')

    model = HemoglobinaGlucosilada

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class EscalaHamiltonDelete(PermissionRequiredMixin, DeleteView):  # NEF-57
    permission_required = ('Formularios.delete_escalahamilton')

    model = EscalaHamilton

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)


class AdherenciaTratamientoDelete(PermissionRequiredMixin, DeleteView):  # NEF-61
    permission_required = ('Formularios.delete_adherenciatratamiento')

    model = AdherenciaTratamiento

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)



class NotaCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-46
    permission_required = 'Formularios.add_notas'
    model = Notas
    form_class = NotaForm
    template_name = "Formularios/nota_form.html" #AAAAAAAAAAAAAAA
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
    error_message = 'Existen errores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(
            Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        tamizaje = TamizajeNutricional.objects.filter(beneficiario=context['beneficiario'].id)
        if tamizaje.exists():
            context['tamizaje'] = tamizaje.latest('id')

        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super(NotaCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def get_sweetify_options(self):
        return self.sweetify_options

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class NotaView(PermissionRequiredMixin, TemplateView):  # NEF-47, NEF-48
    permission_required = ('Formularios.view_notas')
    model = Notas
    template_name = "Formularios/nota_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nota'] = get_object_or_404(Notas, pk=self.kwargs.pop(
            'nota'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['nota'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class NotaDelete(PermissionRequiredMixin, DeleteView):  # NEF-49
    permission_required = ('Formularios.delete_notas')

    model = Notas

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)
      
      
class EvaluacionesPlaticasCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-62
    permission_required = 'Formularios.add_escalahamilton'
    model = EvaluacionPlaticas
    form_class = EvaluacionPlaticasForm
    template_name = "Formularios/evaluacionplaticas_form.html"
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
    error_message = 'Existen errores'

    def form_valid(self, form):
        self.object = form.save()
        return super(EvaluacionesPlaticasCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response
     
    
    
class RegistroMensualCreate(PermissionRequiredMixin, SweetifySuccessMixin, CreateView):  # NEF-58
    permission_required = 'Formularios.add_registromensual'
    model = RegistroMensual
    form_class = RegistroMensualForm
    template_name = "Formularios/registromensual_form.html"
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficiario'] = get_object_or_404(
            Beneficiario, pk=self.kwargs.pop('beneficiario'))
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context

    def form_valid(self, form):
        form.save()
        return super(RegistroMensualCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Beneficiarios:beneficiario',
                            args=[self.kwargs.pop('beneficiario')])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            beneficiario=self.object.beneficiario,
        )

    def form_invalid(self, form):
        sweetify.error(self.request, 'Algo salió mal', icon='error', buttons=False, text=" ")
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class RegistroMensualView(PermissionRequiredMixin, TemplateView):  # NEF-59, # NEF-60
    permission_required = 'Formularios.view_registromensual'

    model = RegistroMensual
    template_name = "Formularios/registromensual_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registromensual'] = get_object_or_404(RegistroMensual, pk=self.kwargs.pop(
            'registromensual'))
        context['beneficiario'] = get_object_or_404(Beneficiario, pk=context['registromensual'].beneficiario.id)
        clasificacion = Clasificacion.objects.filter(beneficiario=context['beneficiario'].id)
        if clasificacion.exists():
            context["clasificacion"] = clasificacion.latest("id")
        return context


class RegistroMensualDelete(PermissionRequiredMixin, DeleteView):  # NEF-61
    permission_required = ('Formularios.delete_registromensual')

    model = RegistroMensual

    def get_success_url(self):
        beneficiario = self.get_object().beneficiario
        return reverse_lazy('Beneficiarios:beneficiario', args=[beneficiario.id])

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=DELETION)
        return HttpResponseRedirect(success_url)
