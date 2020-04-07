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
from .compareReports.compare import *
from django.core.exceptions import ObjectDoesNotExist

from django.db.models.expressions import RawSQL
from django.db import connection
# Create your views here.


def percentage(portion, total):
    if portion is not 0:
        if total is not 0:
            return round(portion * 100 / total)
        else:
            return 0
    else:
        return 0

def fix_percentage(context, arr):
    sum_val = 0  
    min_val = None
    min_key = None
    max_val = None
    max_key = None
    for key in arr:
        if min_val is None:
            min_val = context[key]
            min_key = key
        elif context[key] < min_val and context[key] > 0:
            min_val = context[key]
            min_key = key
        if max_val is None:
            max_val = context[key]
            max_key = key
        elif context[key] > max_val and context[key] > 0:
            max_val = context[key]
            max_key = key
        sum_val += context[key]
    if sum_val == 99:
        context[min_key] = min_val+1
    if sum_val == 101:
        context[max_key] = max_val-1


class ReportesView(PermissionRequiredMixin, TemplateView):  # NEF-206
    permission_required = ('Reportes.view_reportes')
    model = Reportes
    template_name = "Reportes/reportes_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jornadas"] = Jornada.objects.all()
        return context


class ReportesJornadaView(PermissionRequiredMixin, TemplateView):  # NEF-206, NEF-207, NEF-208
    permission_required = ('Reportes.view_reportes')
    model = Reportes
    template_name = "Reportes/reportes_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jornadas"] = Jornada.objects.all()
        context["jornada"] = get_object_or_404(Jornada, pk=self.kwargs.pop(
            'jornada'))
        if context["jornada"]:
            context["beneficiarios"] = Beneficiario.objects.filter(jornada=context["jornada"].id)
            context["total"] = context["beneficiarios"].count()
            if context["total"] is not 0:
                # Reporte sociodemográfico -----------------------------------------------------
                context["total_hombres"] = context["beneficiarios"].filter(sexo=True)
                context["total_mujeres"] = context["beneficiarios"].filter(sexo=False)
                context["p_h"] = percentage(context["total_hombres"].count(), context["total"])
                context["p_m"] = percentage(context["total_mujeres"].count(), context["total"])

                context["h_40"] = context["total_hombres"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["h_41"] = context["total_hombres"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["h_46"] = context["total_hombres"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["h_51"] = context["total_hombres"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["h_56"] = context["total_hombres"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["h_61"] = context["total_hombres"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["h_66"] = context["total_hombres"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["h_71"] = context["total_hombres"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["h_76"] = context["total_hombres"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["h_81"] = context["total_hombres"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["m_40"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["m_41"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["m_46"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["m_51"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["m_56"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["m_61"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["m_66"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["m_71"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["m_76"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["m_81"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                # Reporte estadificación -------------------------------------------------------
                G1 = Clasificacion.objects.filter(Q(categoria_gfr="G1") & Q(
                    categoria_gfr_estimada="G1") & Q(beneficiario__jornada=context["jornada"]))
                G2 = Clasificacion.objects.filter(Q(categoria_gfr="G2") & Q(
                    categoria_gfr_estimada="G2") & Q(beneficiario__jornada=context["jornada"]))
                G3a = Clasificacion.objects.filter(Q(categoria_gfr="G3a") & Q(
                    categoria_gfr_estimada="G3a") & Q(beneficiario__jornada=context["jornada"]))
                G3b = Clasificacion.objects.filter(Q(categoria_gfr="G3b") & Q(
                    categoria_gfr_estimada="G3b") & Q(beneficiario__jornada=context["jornada"]))
                G4 = Clasificacion.objects.filter(Q(categoria_gfr="G4") & Q(
                    categoria_gfr_estimada="G4") & Q(beneficiario__jornada=context["jornada"]))
                G5 = Clasificacion.objects.filter(Q(categoria_gfr="G5") & Q(
                    categoria_gfr_estimada="G5") & Q(beneficiario__jornada=context["jornada"]))

                total_class = G1.count() + G2.count() + G3a.count() + G3b.count() + G4.count() + G5.count()
                context["G1_p"] = percentage(G1.count(), total_class)
                context["G2_p"] = percentage(G2.count(), total_class)
                context["G3a_p"] = percentage(G3a.count(), total_class)
                context["G3b_p"] = percentage(G3b.count(), total_class)
                context["G4_p"] = percentage(G4.count(), total_class)
                context["G5_p"] = percentage(G5.count(), total_class)

                fix_percentage(context, ["G1_p", "G2_p", "G3a_p", "G3b_p", "G4_p", "G5_p"])

                context["m_G1"] = G1.filter(beneficiario__sexo=False)
                context["m_G2"] = G2.filter(beneficiario__sexo=False)
                context["m_G3a"] = G3a.filter(beneficiario__sexo=False)
                context["m_G3b"] = G3b.filter(beneficiario__sexo=False)
                context["m_G4"] = G4.filter(beneficiario__sexo=False)
                context["m_G5"] = G5.filter(beneficiario__sexo=False)

                mujer_total = context['m_G1'].count() + context['m_G2'].count() + context['m_G3a'].count() + \
                    context['m_G3b'].count() + context['m_G4'].count() + context['m_G5'].count()

                context["m_G1_p"] = percentage(context['m_G1'].count(), mujer_total)
                context["m_G2_p"] = percentage(context['m_G2'].count(), mujer_total)
                context["m_G3a_p"] = percentage(context['m_G3a'].count(), mujer_total)
                context["m_G3b_p"] = percentage(context['m_G3b'].count(), mujer_total)
                context["m_G4_p"] = percentage(context['m_G4'].count(), mujer_total)
                context["m_G5_p"] = percentage(context['m_G5'].count(), mujer_total)

                fix_percentage(context, ["m_G1_p", "m_G2_p", "m_G3a_p", "m_G3b_p", "m_G4_p", "m_G5_p"])

                context["h_G1"] = G1.filter(beneficiario__sexo=True)
                context["h_G2"] = G2.filter(beneficiario__sexo=True)
                context["h_G3a"] = G3a.filter(beneficiario__sexo=True)
                context["h_G3b"] = G3b.filter(beneficiario__sexo=True)
                context["h_G4"] = G4.filter(beneficiario__sexo=True)
                context["h_G5"] = G5.filter(beneficiario__sexo=True)

                hombre_total = context['h_G1'].count() + context['h_G2'].count() + context['h_G3a'].count() + \
                    context['h_G3b'].count() + context['h_G4'].count() + context['h_G5'].count()


                context["h_G1_p"] = percentage(context['h_G1'].count(), hombre_total)
                context["h_G2_p"] = percentage(context['h_G2'].count(), hombre_total)
                context["h_G3a_p"] = percentage(context['h_G3a'].count(), hombre_total)
                context["h_G3b_p"] = percentage(context['h_G3b'].count(), hombre_total)
                context["h_G4_p"] = percentage(context['h_G4'].count(), hombre_total)
                context["h_G5_p"] = percentage(context['h_G5'].count(), hombre_total)

                fix_percentage(context, ["h_G1_p", "h_G2_p", "h_G3a_p", "h_G3b_p", "h_G4_p", "h_G5_p"])

                context["h_G1_40"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G1_40"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G1_41"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G1_41"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G1_46"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G1_46"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G1_51"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G1_51"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G1_56"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G1_56"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G1_61"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G1_61"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G1_66"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G1_66"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G1_71"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G1_71"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G1_76"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G1_76"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G1_81"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G1_81"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G2_40"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G2_40"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G2_41"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G2_41"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G2_46"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G2_46"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G2_51"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G2_51"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G2_56"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G2_56"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G2_61"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G2_61"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G2_66"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G2_66"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G2_71"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G2_71"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G2_76"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G2_76"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G2_81"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G2_81"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G3a_40"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G3a_40"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G3a_41"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G3a_41"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G3a_46"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G3a_46"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G3a_51"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G3a_51"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G3a_56"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G3a_56"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G3a_61"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G3a_61"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G3a_66"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G3a_66"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G3a_71"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G3a_71"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G3a_76"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G3a_76"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G3a_81"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G3a_81"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G3b_40"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G3b_40"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G3b_41"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G3b_41"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G3b_46"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G3b_46"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G3b_51"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G3b_51"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G3b_56"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G3b_56"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G3b_61"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G3b_61"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G3b_66"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G3b_66"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G3b_71"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G3b_71"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G3b_76"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G3b_76"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G3b_81"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G3b_81"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G4_40"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G4_40"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G4_41"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G4_41"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G4_46"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G4_46"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G4_51"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G4_51"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G4_56"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G4_56"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G4_61"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G4_61"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G4_66"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G4_66"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G4_71"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G4_71"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G4_76"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G4_76"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G4_81"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G4_81"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G5_40"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G5_40"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G5_41"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G5_41"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G5_46"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G5_46"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G5_51"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G5_51"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G5_56"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G5_56"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G5_61"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G5_61"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G5_66"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G5_66"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G5_71"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G5_71"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G5_76"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G5_76"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G5_81"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G5_81"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                # Reporte diabetes / hipertensión
                context["t_h_n"] = context["total_hombres"].filter(diabetico_hipertenso=0)
                context["t_h_d"] = context["total_hombres"].filter(diabetico_hipertenso=1)
                context["t_h_h"] = context["total_hombres"].filter(diabetico_hipertenso=2)
                context["t_h_dh"] = context["total_hombres"].filter(diabetico_hipertenso=3)
                context["t_m_n"] = context["total_mujeres"].filter(diabetico_hipertenso=0)
                context["t_m_d"] = context["total_mujeres"].filter(diabetico_hipertenso=1)
                context["t_m_h"] = context["total_mujeres"].filter(diabetico_hipertenso=2)
                context["t_m_dh"] = context["total_mujeres"].filter(diabetico_hipertenso=3)

                total_hombres = context["total_hombres"].count()
                total_mujeres = context["total_mujeres"].count()

                context["p_h_n"] = percentage(context["t_h_n"].count(), total_hombres)
                context["p_h_d"] = percentage(context["t_h_d"].count(), total_hombres)
                context["p_h_h"] = percentage(context["t_h_h"].count(), total_hombres)
                context["p_h_dh"] = percentage(context["t_h_dh"].count(), total_hombres)
                context["p_m_n"] = percentage(context["t_m_n"].count(), total_mujeres)
                context["p_m_d"] = percentage(context["t_m_d"].count(), total_mujeres)
                context["p_m_h"] = percentage(context["t_m_h"].count(), total_mujeres)
                context["p_m_dh"] = percentage(context["t_m_dh"].count(), total_mujeres)

                fix_percentage(context, ["p_h_n", "p_h_d", "p_h_h", "p_h_dh"])
                fix_percentage(context, ["p_m_n", "p_m_d", "p_m_h", "p_m_dh"])

                context["h_n_40"] = context["t_h_n"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["h_d_40"] = context["t_h_d"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["h_h_40"] = context["t_h_h"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["h_dh_40"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()

                context["h_n_41"] = context["t_h_n"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["h_d_41"] = context["t_h_d"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["h_h_41"] = context["t_h_h"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["h_dh_41"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()

                context["h_n_46"] = context["t_h_n"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["h_d_46"] = context["t_h_d"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["h_h_46"] = context["t_h_h"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["h_dh_46"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()

                context["h_n_51"] = context["t_h_n"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["h_d_51"] = context["t_h_d"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["h_h_51"] = context["t_h_h"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["h_dh_51"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()

                context["h_n_56"] = context["t_h_n"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["h_d_56"] = context["t_h_d"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["h_h_56"] = context["t_h_h"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["h_dh_56"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()

                context["h_n_61"] = context["t_h_n"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["h_d_61"] = context["t_h_d"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["h_h_61"] = context["t_h_h"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["h_dh_61"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()

                context["h_n_66"] = context["t_h_n"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["h_d_66"] = context["t_h_d"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["h_h_66"] = context["t_h_h"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["h_dh_66"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()

                context["h_n_71"] = context["t_h_n"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["h_d_71"] = context["t_h_d"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["h_h_71"] = context["t_h_h"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["h_dh_71"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()

                context["h_n_76"] = context["t_h_n"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["h_d_76"] = context["t_h_d"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["h_h_76"] = context["t_h_h"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["h_dh_76"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()

                context["h_n_81"] = context["t_h_n"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["h_d_81"] = context["t_h_d"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["h_h_81"] = context["t_h_h"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["h_dh_81"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                # Mujeres
                context["m_n_40"] = context["t_m_n"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["m_d_40"] = context["t_m_d"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["m_h_40"] = context["t_m_h"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["m_dh_40"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()

                context["m_n_41"] = context["t_m_n"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["m_d_41"] = context["t_m_d"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["m_h_41"] = context["t_m_h"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["m_dh_41"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()

                context["m_n_46"] = context["t_m_n"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["m_d_46"] = context["t_m_d"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["m_h_46"] = context["t_m_h"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["m_dh_46"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()

                context["m_n_51"] = context["t_m_n"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["m_d_51"] = context["t_m_d"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["m_h_51"] = context["t_m_h"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["m_dh_51"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()

                context["m_n_56"] = context["t_m_n"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["m_d_56"] = context["t_m_d"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["m_h_56"] = context["t_m_h"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["m_dh_56"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()

                context["m_n_61"] = context["t_m_n"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["m_d_61"] = context["t_m_d"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["m_h_61"] = context["t_m_h"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["m_dh_61"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()

                context["m_n_66"] = context["t_m_n"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["m_d_66"] = context["t_m_d"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["m_h_66"] = context["t_m_h"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["m_dh_66"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()

                context["m_n_71"] = context["t_m_n"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["m_d_71"] = context["t_m_d"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["m_h_71"] = context["t_m_h"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["m_dh_71"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()

                context["m_n_76"] = context["t_m_n"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["m_d_76"] = context["t_m_d"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["m_h_76"] = context["t_m_h"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["m_dh_76"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()

                context["m_n_81"] = context["t_m_n"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["m_d_81"] = context["t_m_d"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["m_h_81"] = context["t_m_h"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["m_dh_81"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                # Reporte de Factor de Riesgo
                bajo_riesgo = FactorDeRiesgo.objects.filter(resultado__lte=10,
                                                            beneficiario__jornada=context['jornada'].id)
                moderado_riesgo = FactorDeRiesgo.objects.filter(resultado__gte=11, resultado__lte=19,
                                                                beneficiario__jornada=context['jornada'].id)
                alto_riesgo = FactorDeRiesgo.objects.filter(resultado__gte=20,
                                                            beneficiario__jornada=context['jornada'].id)

                h_bajo_riesgo = bajo_riesgo.filter(beneficiario__sexo=True)
                h_moderado_riesgo = moderado_riesgo.filter(beneficiario__sexo=True)
                h_alto_riesgo = alto_riesgo.filter(beneficiario__sexo=True)

                m_bajo_riesgo = bajo_riesgo.filter(beneficiario__sexo=False)
                m_moderado_riesgo = moderado_riesgo.filter(beneficiario__sexo=False)
                m_alto_riesgo = alto_riesgo.filter(beneficiario__sexo=False)

                context['h_br_40'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['h_br_41'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                          beneficiario__edad_inicial__lte=45).count()
                context['h_br_46'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                          beneficiario__edad_inicial__lte=50).count()
                context['h_br_51'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                          beneficiario__edad_inicial__lte=55).count()
                context['h_br_56'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                          beneficiario__edad_inicial__lte=60).count()
                context['h_br_61'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                          beneficiario__edad_inicial__lte=65).count()
                context['h_br_66'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                          beneficiario__edad_inicial__lte=70).count()
                context['h_br_71'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                          beneficiario__edad_inicial__lte=75).count()
                context['h_br_76'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                          beneficiario__edad_inicial__lte=80).count()
                context['h_br_81'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['h_mr_40'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['h_mr_41'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                              beneficiario__edad_inicial__lte=45).count()
                context['h_mr_46'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                              beneficiario__edad_inicial__lte=50).count()
                context['h_mr_51'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                              beneficiario__edad_inicial__lte=55).count()
                context['h_mr_56'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                              beneficiario__edad_inicial__lte=60).count()
                context['h_mr_61'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                              beneficiario__edad_inicial__lte=65).count()
                context['h_mr_66'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                              beneficiario__edad_inicial__lte=70).count()
                context['h_mr_71'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                              beneficiario__edad_inicial__lte=75).count()
                context['h_mr_76'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                              beneficiario__edad_inicial__lte=80).count()
                context['h_mr_81'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['h_ar_40'] = h_alto_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['h_ar_41'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                          beneficiario__edad_inicial__lte=45).count()
                context['h_ar_46'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                          beneficiario__edad_inicial__lte=50).count()
                context['h_ar_51'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                          beneficiario__edad_inicial__lte=55).count()
                context['h_ar_56'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                          beneficiario__edad_inicial__lte=60).count()
                context['h_ar_61'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                          beneficiario__edad_inicial__lte=65).count()
                context['h_ar_66'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                          beneficiario__edad_inicial__lte=70).count()
                context['h_ar_71'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                          beneficiario__edad_inicial__lte=75).count()
                context['h_ar_76'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                          beneficiario__edad_inicial__lte=80).count()
                context['h_ar_81'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['m_br_40'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['m_br_41'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                          beneficiario__edad_inicial__lte=45).count()
                context['m_br_46'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                          beneficiario__edad_inicial__lte=50).count()
                context['m_br_51'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                          beneficiario__edad_inicial__lte=55).count()
                context['m_br_56'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                          beneficiario__edad_inicial__lte=60).count()
                context['m_br_61'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                          beneficiario__edad_inicial__lte=65).count()
                context['m_br_66'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                          beneficiario__edad_inicial__lte=70).count()
                context['m_br_71'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                          beneficiario__edad_inicial__lte=75).count()
                context['m_br_76'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                          beneficiario__edad_inicial__lte=80).count()
                context['m_br_81'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['m_mr_40'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['m_mr_41'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                              beneficiario__edad_inicial__lte=45).count()
                context['m_mr_46'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                              beneficiario__edad_inicial__lte=50).count()
                context['m_mr_51'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                              beneficiario__edad_inicial__lte=55).count()
                context['m_mr_56'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                              beneficiario__edad_inicial__lte=60).count()
                context['m_mr_61'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                              beneficiario__edad_inicial__lte=65).count()
                context['m_mr_66'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                              beneficiario__edad_inicial__lte=70).count()
                context['m_mr_71'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                              beneficiario__edad_inicial__lte=75).count()
                context['m_mr_76'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                              beneficiario__edad_inicial__lte=80).count()
                context['m_mr_81'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['m_ar_40'] = m_alto_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['m_ar_41'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                          beneficiario__edad_inicial__lte=45).count()
                context['m_ar_46'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                          beneficiario__edad_inicial__lte=50).count()
                context['m_ar_51'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                          beneficiario__edad_inicial__lte=55).count()
                context['m_ar_56'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                          beneficiario__edad_inicial__lte=60).count()
                context['m_ar_61'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                          beneficiario__edad_inicial__lte=65).count()
                context['m_ar_66'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                          beneficiario__edad_inicial__lte=70).count()
                context['m_ar_71'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                          beneficiario__edad_inicial__lte=75).count()
                context['m_ar_76'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                          beneficiario__edad_inicial__lte=80).count()
                context['m_ar_81'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['h_br'] = h_bajo_riesgo.count()
                context['h_mr'] = h_moderado_riesgo.count()
                context['h_ar'] = h_alto_riesgo.count()
                context['h_sd'] = total_hombres-context['h_br']-context['h_mr']-context['h_ar']

                context['h_br_p'] = percentage(context['h_br'], total_hombres)
                context['h_mr_p'] = percentage(context['h_mr'], total_hombres)
                context['h_ar_p'] = percentage(context['h_ar'], total_hombres)
                context['h_sd_p'] = percentage(context['h_sd'], total_hombres)

                fix_percentage(context, ["h_br_p", "h_mr_p", "h_ar_p", "h_sd_p"])

                context['m_br'] = m_bajo_riesgo.count()
                context['m_mr'] = m_moderado_riesgo.count()
                context['m_ar'] = m_alto_riesgo.count()
                context['m_sd'] = total_mujeres - context['m_br'] - context['m_mr'] - context['m_ar']

                context['m_br_p'] = percentage(context['m_br'], total_mujeres)
                context['m_mr_p'] = percentage(context['m_mr'], total_mujeres)
                context['m_ar_p'] = percentage(context['m_ar'], total_mujeres)
                context['m_sd_p'] = percentage(context['m_sd'], total_mujeres)

                fix_percentage(context, ["m_br_p", "m_mr_p", "m_ar_p", "m_sd_p"])

                # Reporte de Factor de Riesgo
                malnutrición = MalnutricionInflamacion.objects.filter(beneficiario__jornada=context['jornada'].id).values(
                    'pk', 'beneficiario', 'fecha_creacion', 'fecha', 'resultado', 'beneficiario__sexo')
                beneficiarios_malnutricion = malnutrición.values('beneficiario')
                id_benef = []
                for set in beneficiarios_malnutricion:
                    if set['beneficiario'] not in id_benef:
                        id_benef.append(set['beneficiario'])

                pk_benf = []
                for beneficiario in id_benef:
                    pk_benf.append(malnutrición.filter(beneficiario=beneficiario).latest('fecha')["pk"])

                malnutrición_filtered = malnutrición.filter(pk__in=pk_benf)

                context['est_nut_a'] = malnutrición_filtered.filter(resultado=0).count()
                context['des_nut_leve_b'] = malnutrición_filtered.filter(resultado__gte=1, resultado__lte=9).count()
                context['des_nut_mod_c'] = malnutrición_filtered.filter(resultado__gte=10, resultado__lte=19).count()
                context['des_nut_grave_d'] = malnutrición_filtered.filter(resultado__gte=20, resultado__lte=29).count()
                context['des_nut_grav_e'] = malnutrición_filtered.filter(resultado__gte=30).count()
                context['nutricion_por'] = malnutrición_filtered.count()

                if(malnutrición_filtered.count() > 0):
                    context['p_est_nut_a'] = context['est_nut_a']/context['nutricion_por'] * 100
                    context['p_des_nut_leve_b'] = context['des_nut_leve_b']/context['nutricion_por'] * 100
                    context['p_des_nut_mod_c'] = context['des_nut_mod_c']/context['nutricion_por'] * 100
                    context['p_des_nut_grave_d'] = context['des_nut_grave_d']/context['nutricion_por'] * 100
                    context['p_des_nut_grav_e'] = context['des_nut_grav_e']/context['nutricion_por'] * 100

                # Reporte controlados y descontrolados

                    # Hipertensos controlados/descontrolados/sin datos

                hipertensos = context["beneficiarios"].filter(diabetico_hipertenso=2)
                h_total = hipertensos.count()
                h_controlados = 0
                h_descontrolados = 0
                h_nodatos = 0
                for p in range(h_total):
                    tamizaje = TamizajeNutricional.objects.filter(beneficiario=hipertensos[p].id)
                    if(len(tamizaje) == 0):
                        h_nodatos += 1
                    else:
                        actual = tamizaje.latest('fecha')
                        if(actual.presion_sistolica >= 140 and actual.presion_diastolica >= 90):
                            h_descontrolados += 1
                        else:
                            h_controlados += 1

                context['c_tension_hipertension'] = h_controlados
                context['nc_tension_hipertension'] = h_descontrolados
                context['sd_tension_hipertension'] = h_nodatos

                context['t_hipertension'] = percentage(h_controlados, h_total)
                context['t_nhipertension'] = percentage(h_descontrolados, h_total)
                context['sd_hipertension'] = percentage(h_nodatos, h_total)

                fix_percentage(context, ["t_hipertension", "t_nhipertension", "sd_hipertension"])

                # diabeticos controlados/descontrolados/sin datos
                context["diabetico_t"] = context["beneficiarios"].filter(diabetico_hipertenso=1).count()

                with connection.cursor() as diabc:
                    diabc.execute('''select jor.id, max(jor.id) as jornada, glucosa, hba1c
                                    from "Beneficiarios_beneficiario" as jor
                                    inner join (select fgc.beneficiario_id, max(fgc.id) as glucosa, hba1c
                                    from "Formularios_glucosacapilar" as fgc
                                    inner join (select asd.beneficiario_id, max(asd.id) as hba1c
                                    from "Formularios_hemoglobinaglucosilada" as asd
                                    where asd.hemoglobina_glucosilada < 7
                                    group by asd.beneficiario_id) as fhg
                                    on fhg.beneficiario_id = fgc.beneficiario_id
                                    where glucosa < 130 group by fgc.beneficiario_id, hba1c)
                                    as fght on jor.id = fght.beneficiario_id
                                    where jor.jornada_id = (%s)
                                    group by jor.id, glucosa, hba1c ''',
                                  (context['jornada'].id,))

                context['diab_cont'] = diabc.rowcount
                context['diab_ncont'] = context["diabetico_t"] - context['diab_cont']
                if (context['diabetico_t'] == 0):
                    context['sd_diabetico'] = 0
                    context['sd_d'] = 0
                    context['diab_ncont'] = 0
                    context['diab_ncont_p'] = 0
                    context['diabetico_t'] = context['diab_cont'] + context['diab_ncont']
                else:
                    if (context['diab_cont'] == 0 and context['diab_ncont'] == 0):
                        context['sd_diabetico'] = 0
                    else:
                        context['sd_diabetico'] = context['diabetico_t'] - context['diab_cont'] - context['diab_ncont']
                    context['sd_d'] = percentage(context['sd_diabetico'], context['diabetico_t'])
                    context['diab_ncont_p'] = percentage(context['diab_ncont'], context['diabetico_t'])
                context['diab_cont_p'] = percentage(context['diab_cont'], context['diabetico_t'])

                # diabeticos/hipertensos controlados/descontrolados/sin datos
                context["diabetico_hipertenso_t"] = context["beneficiarios"].filter(diabetico_hipertenso=3).count()

                with connection.cursor() as dhc:
                    dhc.execute('''select jor.id, max(jor.id) as jornada, glucosa, hba1c, presion
                                from "Beneficiarios_beneficiario" as jor
                                inner join (select fgc.beneficiario_id, max(fgc.id) as glucosa, hba1c, presion
                                from "Formularios_glucosacapilar" as fgc
                                inner join (select asd.beneficiario_id, max(asd.id) as hba1c, presion
                                from "Formularios_hemoglobinaglucosilada" as asd
                                inner join (select qwerty.beneficiario_id, max(qwerty.id) as presion
                                from "Formularios_tamizajenutricional" as qwerty
                                where presion_sistolica < 140 and presion_diastolica < 90
                                group by qwerty.beneficiario_id) as fgh
                                on asd.beneficiario_id = fgh.beneficiario_id
                                where asd.hemoglobina_glucosilada < 7
                                group by asd.beneficiario_id, presion) as fhg
                                on fhg.beneficiario_id = fgc.beneficiario_id
                                where glucosa < 130 group by fgc.beneficiario_id, hba1c, presion)
                                as fght on jor.id = fght.beneficiario_id
                                where jor.jornada_id = (%s)
                                group by jor.id, glucosa, hba1c, presion ''',
                                (context['jornada'].id,))

                context['dia_hip_cont'] = dhc.rowcount
                context['dia_hip_no_cont'] = context["diabetico_hipertenso_t"] - context['dia_hip_cont']
                if (context['diabetico_hipertenso_t'] == 0):
                    context['sd_diabetico_hipertenso'] = 0
                    context['sd_dh'] = 0
                    context['dia_hip_no_cont'] = 0
                    context['dia_hip_no_cont_p'] = 0
                    context['diabetico_hipertenso_t'] = context['dia_hip_cont'] + context['dia_hip_no_cont']
                else:
                    if (context['dia_hip_cont'] == 0 and context['dia_hip_no_cont'] == 0):
                        context['sd_diabetico_hipertenso'] = 0
                    else:
                        context['sd_diabetico_hipertenso'] = context['diabetico_hipertenso_t'] - \
                            context['dia_hip_cont'] - context['dia_hip_no_cont']
                    context['sd_dh'] = percentage(context['sd_diabetico_hipertenso'],
                                                  context['diabetico_hipertenso_t'])
                    context['dia_hip_no_cont_p'] = percentage(
                        context['dia_hip_no_cont'], context['diabetico_hipertenso_t'])
                context['dia_hip_cont_p'] = percentage(context['dia_hip_cont'], context['diabetico_hipertenso_t'])

                # Reporte de evaluaciones de platicas
                evaluacion = EvaluacionPlaticas.objects.filter(jornada=context['jornada'].id).values(
                    'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11')

                context["evaluacion"] = evaluacion
                context["evaluacion_count"] = evaluacion.count()

                context["correctas"], context["incorrectas"] = evaluate_data(evaluacion)

                # Adherencia al tratamiento
                context["a_t_re"] = 0
                context["a_t_ne"] = 0
                context["a_t_mo"] = 0
                context["a_t_ac"] = 0
                context["a_t_ad"] = 0

                context["a_h_re"] = 0
                context["a_h_ne"] = 0
                context["a_h_mo"] = 0
                context["a_h_ac"] = 0
                context["a_h_ad"] = 0

                context["a_m_re"] = 0
                context["a_m_ne"] = 0
                context["a_m_mo"] = 0
                context["a_m_ac"] = 0
                context["a_m_ad"] = 0

                context["adherencia"] = False

                for b in context["beneficiarios"]:
                    if AdherenciaTratamiento.objects.filter(beneficiario=b).exists():
                        at = AdherenciaTratamiento.objects.filter(beneficiario=b).order_by('-id')[0]
                        context["adherencia"] = True
                        if b.sexo:
                            if at.interpretacion == "Rechazo":
                                context["a_t_re"] += 1
                                context["a_h_re"] += 1
                            elif at.interpretacion == "Negación":
                                context["a_t_ne"] += 1
                                context["a_h_ne"] += 1
                            elif at.interpretacion == "Modificación":
                                context["a_t_mo"] += 1
                                context["a_h_mo"] += 1
                            elif at.interpretacion == "Aceptación":
                                context["a_t_ac"] += 1
                                context["a_h_ac"] += 1
                            elif at.interpretacion == "Adherencia":
                                context["a_t_ad"] += 1
                                context["a_h_ad"] += 1
                        else:
                            if at.interpretacion == "Rechazo":
                                context["a_t_re"] += 1
                                context["a_m_re"] += 1
                            elif at.interpretacion == "Negación":
                                context["a_t_ne"] += 1
                                context["a_m_ne"] += 1
                            elif at.interpretacion == "Modificación":
                                context["a_t_mo"] += 1
                                context["a_m_mo"] += 1
                            elif at.interpretacion == "Aceptación":
                                context["a_t_ac"] += 1
                                context["a_m_ac"] += 1
                            elif at.interpretacion == "Adherencia":
                                context["a_t_ad"] += 1
                                context["a_m_ad"] += 1

                # Hamilton
                context["h_t_md"] = 0
                context["h_t_ds"] = 0
                context["h_t_dm"] = 0
                context["h_t_dl"] = 0
                context["h_t_sd"] = 0

                context["h_h_md"] = 0
                context["h_h_ds"] = 0
                context["h_h_dm"] = 0
                context["h_h_dl"] = 0
                context["h_h_sd"] = 0

                context["h_m_md"] = 0
                context["h_m_ds"] = 0
                context["h_m_dm"] = 0
                context["h_m_dl"] = 0
                context["h_m_sd"] = 0

                context["hamilton"] = False

                for b in context["beneficiarios"]:
                    if EscalaHamilton.objects.filter(beneficiario=b).exists():
                        eh = EscalaHamilton.objects.filter(beneficiario=b).order_by('-id')[0]
                        context["hamilton"] = True
                        if b.sexo:
                            if eh.interpretacion == "No deprimido":
                                context["h_t_sd"] += 1
                                context["h_h_sd"] += 1
                            elif eh.interpretacion == "Depresión ligera/menor":
                                context["h_t_dl"] += 1
                                context["h_h_dl"] += 1
                            elif eh.interpretacion == "Depresión moderada":
                                context["h_t_dm"] += 1
                                context["h_h_dm"] += 1
                            elif eh.interpretacion == "Depresión severa":
                                context["h_t_ds"] += 1
                                context["h_h_ds"] += 1
                            elif eh.interpretacion == "Depresión muy severa":
                                context["h_t_md"] += 1
                                context["h_h_md"] += 1
                        else:
                            if eh.interpretacion == "No deprimido":
                                context["h_t_sd"] += 1
                                context["h_m_sd"] += 1
                            elif eh.interpretacion == "Depresión ligera/menor":
                                context["h_t_dl"] += 1
                                context["h_m_dl"] += 1
                            elif eh.interpretacion == "Depresión moderada":
                                context["h_t_dm"] += 1
                                context["h_m_dm"] += 1
                            elif eh.interpretacion == "Depresión severa":
                                context["h_t_ds"] += 1
                                context["h_m_ds"] += 1
                            elif eh.interpretacion == "Depresión muy severa":
                                context["h_t_md"] += 1
                                context["h_m_md"] += 1
        return context


def evaluate_data(datos):
    correct = []
    incorrect = []
    for evaluacion in datos:
        zippend((correct, incorrect), evaluate_questions(evaluacion))
    res_correct = [sum(x) for x in zip(*correct)]
    res_incorrect = [sum(x) for x in zip(*incorrect)]
    return res_correct, res_incorrect


def evaluate_questions(evaluacion):
    correct = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    incorrect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    current = 0
    for question in evaluacion.values():
        if question == 1:
            correct[current] += 1
        else:
            incorrect[current] += 1
        current += 1
        current = current % 11

    return correct, incorrect


def zippend(lists, values):
    assert len(lists) == len(values)
    for l, v in zip(lists, values):
        l.append(v)


# //////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////ReportesSeguimientoView///////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////

class ReportesSeguimientoView(PermissionRequiredMixin, TemplateView):  # NEF-206
    permission_required = ('Reportes.view_reportes')
    model = Reportes
    template_name = "Reportes/reportes_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jornadas"] = Jornada.objects.all()
        context["de_seguimiento"] = True
        return context


class ReportesSeguimientoJornadaView(PermissionRequiredMixin, TemplateView):  # NEF-206, NEF-207, NEF-208
    permission_required = ('Reportes.view_reportes')
    model = Reportes
    template_name = "Reportes/reportes_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jornadas"] = Jornada.objects.all()
        context["de_seguimiento"] = True
        context["jornada"] = get_object_or_404(Jornada, pk=self.kwargs.pop(
            'jornada'))
        if context["jornada"]:
            context["beneficiarios"] = Beneficiario.objects.filter(
                jornada=context["jornada"].id).filter(de_seguimiento=True)
            context["total"] = context["beneficiarios"].count()
            if context["total"] is not 0:
                # Reporte sociodemográfico -----------------------------------------------------
                context["total_hombres"] = context["beneficiarios"].filter(sexo=True)
                context["total_mujeres"] = context["beneficiarios"].filter(sexo=False)
                context["p_h"] = percentage(context["total_hombres"].count(), context["total"])
                context["p_m"] = percentage(context["total_mujeres"].count(), context["total"])
                context["h_40"] = context["total_hombres"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["h_41"] = context["total_hombres"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["h_46"] = context["total_hombres"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["h_51"] = context["total_hombres"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["h_56"] = context["total_hombres"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["h_61"] = context["total_hombres"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["h_66"] = context["total_hombres"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["h_71"] = context["total_hombres"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["h_76"] = context["total_hombres"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["h_81"] = context["total_hombres"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["m_40"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["m_41"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["m_46"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["m_51"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["m_56"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["m_61"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["m_66"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["m_71"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["m_76"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["m_81"] = context["total_mujeres"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                # Reporte estadificación -------------------------------------------------------
                G1 = Clasificacion.objects.filter(Q(categoria_gfr="G1") & Q(
                    categoria_gfr_estimada="G1") & Q(beneficiario__jornada=context["jornada"])
                    & Q(beneficiario__de_seguimiento=True))
                G2 = Clasificacion.objects.filter(Q(categoria_gfr="G2") & Q(
                    categoria_gfr_estimada="G2") & Q(beneficiario__jornada=context["jornada"])
                    & Q(beneficiario__de_seguimiento=True))
                G3a = Clasificacion.objects.filter(Q(categoria_gfr="G3a") & Q(
                    categoria_gfr_estimada="G3a") & Q(beneficiario__jornada=context["jornada"])
                    & Q(beneficiario__de_seguimiento=True))
                G3b = Clasificacion.objects.filter(Q(categoria_gfr="G3b") & Q(
                    categoria_gfr_estimada="G3b") & Q(beneficiario__jornada=context["jornada"])
                    & Q(beneficiario__de_seguimiento=True))
                G4 = Clasificacion.objects.filter(Q(categoria_gfr="G4") & Q(
                    categoria_gfr_estimada="G4") & Q(beneficiario__jornada=context["jornada"])
                    & Q(beneficiario__de_seguimiento=True))
                G5 = Clasificacion.objects.filter(Q(categoria_gfr="G5") & Q(
                    categoria_gfr_estimada="G5") & Q(beneficiario__jornada=context["jornada"])
                    & Q(beneficiario__de_seguimiento=True))

                total_class = G1.count() + G2.count() + G3a.count() + G3b.count() + G4.count() + G5.count()
                context["G1_p"] = percentage(G1.count(), total_class)
                context["G2_p"] = percentage(G2.count(), total_class)
                context["G3a_p"] = percentage(G3a.count(), total_class)
                context["G3b_p"] = percentage(G3b.count(), total_class)
                context["G4_p"] = percentage(G4.count(), total_class)
                context["G5_p"] = percentage(G5.count(), total_class)
                
                fix_percentage(context, ["G1_p", "G2_p", "G3a_p", "G3b_p", "G4_p", "G5_p"])
                
                context["m_G1"] = G1.filter(beneficiario__sexo=False)
                context["m_G2"] = G2.filter(beneficiario__sexo=False)
                context["m_G3a"] = G3a.filter(beneficiario__sexo=False)
                context["m_G3b"] = G3b.filter(beneficiario__sexo=False)
                context["m_G4"] = G4.filter(beneficiario__sexo=False)
                context["m_G5"] = G5.filter(beneficiario__sexo=False)

                mujer_total = context['m_G1'].count() + context['m_G2'].count() + context['m_G3a'].count() + \
                    context['m_G3b'].count() + context['m_G4'].count() + context['m_G5'].count()

                context["m_G1_p"] = percentage(context['m_G1'].count(), mujer_total)
                context["m_G2_p"] = percentage(context['m_G2'].count(), mujer_total)
                context["m_G3a_p"] = percentage(context['m_G3a'].count(), mujer_total)
                context["m_G3b_p"] = percentage(context['m_G3b'].count(), mujer_total)
                context["m_G4_p"] = percentage(context['m_G4'].count(), mujer_total)
                context["m_G5_p"] = percentage(context['m_G5'].count(), mujer_total)

                fix_percentage(context, ["m_G1_p", "m_G2_p", "m_G3a_p", "m_G3b_p", "m_G4_p", "m_G5_p"])

                context["h_G1"] = G1.filter(beneficiario__sexo=True)
                context["h_G2"] = G2.filter(beneficiario__sexo=True)
                context["h_G3a"] = G3a.filter(beneficiario__sexo=True)
                context["h_G3b"] = G3b.filter(beneficiario__sexo=True)
                context["h_G4"] = G4.filter(beneficiario__sexo=True)
                context["h_G5"] = G5.filter(beneficiario__sexo=True)

                hombre_total = context['h_G1'].count() + context['h_G2'].count() + context['h_G3a'].count() + \
                    context['h_G3b'].count() + context['h_G4'].count() + context['h_G5'].count()

                context["h_G1_p"] = percentage(context['h_G1'].count(), hombre_total)
                context["h_G2_p"] = percentage(context['h_G2'].count(), hombre_total)
                context["h_G3a_p"] = percentage(context['h_G3a'].count(), hombre_total)
                context["h_G3b_p"] = percentage(context['h_G3b'].count(), hombre_total)
                context["h_G4_p"] = percentage(context['h_G4'].count(), hombre_total)
                context["h_G5_p"] = percentage(context['h_G5'].count(), hombre_total)

                fix_percentage(context, ["h_G1_p", "h_G2_p", "h_G3a_p", "h_G3b_p", "h_G4_p", "h_G5_p"])

                context["h_G1_40"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G1_40"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G1_41"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G1_41"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G1_46"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G1_46"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G1_51"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G1_51"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G1_56"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G1_56"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G1_61"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G1_61"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G1_66"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G1_66"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G1_71"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G1_71"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G1_76"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G1_76"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G1_81"] = context["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G1_81"] = context["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G2_40"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G2_40"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G2_41"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G2_41"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G2_46"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G2_46"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G2_51"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G2_51"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G2_56"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G2_56"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G2_61"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G2_61"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G2_66"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G2_66"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G2_71"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G2_71"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G2_76"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G2_76"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G2_81"] = context["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G2_81"] = context["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G3a_40"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G3a_40"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G3a_41"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G3a_41"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G3a_46"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G3a_46"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G3a_51"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G3a_51"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G3a_56"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G3a_56"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G3a_61"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G3a_61"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G3a_66"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G3a_66"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G3a_71"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G3a_71"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G3a_76"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G3a_76"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G3a_81"] = context["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G3a_81"] = context["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G3b_40"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G3b_40"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G3b_41"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G3b_41"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G3b_46"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G3b_46"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G3b_51"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G3b_51"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G3b_56"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G3b_56"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G3b_61"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G3b_61"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G3b_66"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G3b_66"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G3b_71"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G3b_71"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G3b_76"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G3b_76"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G3b_81"] = context["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G3b_81"] = context["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G4_40"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G4_40"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G4_41"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G4_41"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G4_46"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G4_46"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G4_51"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G4_51"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G4_56"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G4_56"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G4_61"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G4_61"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G4_66"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G4_66"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G4_71"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G4_71"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G4_76"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G4_76"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G4_81"] = context["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G4_81"] = context["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                context["h_G5_40"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["m_G5_40"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                context["h_G5_41"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["m_G5_41"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                context["h_G5_46"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["m_G5_46"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                context["h_G5_51"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["m_G5_51"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                context["h_G5_56"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["m_G5_56"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                context["h_G5_61"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["m_G5_61"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                context["h_G5_66"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["m_G5_66"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                context["h_G5_71"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["m_G5_71"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                context["h_G5_76"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["m_G5_76"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                context["h_G5_81"] = context["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                context["m_G5_81"] = context["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                # Reporte diabetes / hipertensión
                context["t_h_n"] = context["total_hombres"].filter(diabetico_hipertenso=0)
                context["t_h_d"] = context["total_hombres"].filter(diabetico_hipertenso=1)
                context["t_h_h"] = context["total_hombres"].filter(diabetico_hipertenso=2)
                context["t_h_dh"] = context["total_hombres"].filter(diabetico_hipertenso=3)
                context["t_m_n"] = context["total_mujeres"].filter(diabetico_hipertenso=0)
                context["t_m_d"] = context["total_mujeres"].filter(diabetico_hipertenso=1)
                context["t_m_h"] = context["total_mujeres"].filter(diabetico_hipertenso=2)
                context["t_m_dh"] = context["total_mujeres"].filter(diabetico_hipertenso=3)

                total_hombres = context["total_hombres"].count()
                total_mujeres = context["total_mujeres"].count()

                context["p_h_n"] = percentage(context["t_h_n"].count(), total_hombres)
                context["p_h_d"] = percentage(context["t_h_d"].count(), total_hombres)
                context["p_h_h"] = percentage(context["t_h_h"].count(), total_hombres)
                context["p_h_dh"] = percentage(context["t_h_dh"].count(), total_hombres)
                context["p_m_n"] = percentage(context["t_m_n"].count(), total_mujeres)
                context["p_m_d"] = percentage(context["t_m_d"].count(), total_mujeres)
                context["p_m_h"] = percentage(context["t_m_h"].count(), total_mujeres)
                context["p_m_dh"] = percentage(context["t_m_dh"].count(), total_mujeres)

                fix_percentage(context, ["p_h_n", "p_h_d", "p_h_h", "p_h_dh"])
                fix_percentage(context, ["p_m_n", "p_m_d", "p_m_h", "p_m_dh"])

                context["h_n_40"] = context["t_h_n"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["h_d_40"] = context["t_h_d"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["h_h_40"] = context["t_h_h"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["h_dh_40"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()

                context["h_n_41"] = context["t_h_n"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["h_d_41"] = context["t_h_d"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["h_h_41"] = context["t_h_h"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["h_dh_41"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()

                context["h_n_46"] = context["t_h_n"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["h_d_46"] = context["t_h_d"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["h_h_46"] = context["t_h_h"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["h_dh_46"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()

                context["h_n_51"] = context["t_h_n"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["h_d_51"] = context["t_h_d"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["h_h_51"] = context["t_h_h"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["h_dh_51"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()

                context["h_n_56"] = context["t_h_n"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["h_d_56"] = context["t_h_d"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["h_h_56"] = context["t_h_h"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["h_dh_56"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()

                context["h_n_61"] = context["t_h_n"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["h_d_61"] = context["t_h_d"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["h_h_61"] = context["t_h_h"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["h_dh_61"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()

                context["h_n_66"] = context["t_h_n"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["h_d_66"] = context["t_h_d"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["h_h_66"] = context["t_h_h"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["h_dh_66"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()

                context["h_n_71"] = context["t_h_n"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["h_d_71"] = context["t_h_d"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["h_h_71"] = context["t_h_h"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["h_dh_71"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()

                context["h_n_76"] = context["t_h_n"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["h_d_76"] = context["t_h_d"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["h_h_76"] = context["t_h_h"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["h_dh_76"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()

                context["h_n_81"] = context["t_h_n"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["h_d_81"] = context["t_h_d"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["h_h_81"] = context["t_h_h"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["h_dh_81"] = context["t_h_dh"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                # Mujeres
                context["m_n_40"] = context["t_m_n"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["m_d_40"] = context["t_m_d"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["m_h_40"] = context["t_m_h"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                context["m_dh_40"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()

                context["m_n_41"] = context["t_m_n"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["m_d_41"] = context["t_m_d"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["m_h_41"] = context["t_m_h"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                context["m_dh_41"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()

                context["m_n_46"] = context["t_m_n"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["m_d_46"] = context["t_m_d"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["m_h_46"] = context["t_m_h"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                context["m_dh_46"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()

                context["m_n_51"] = context["t_m_n"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["m_d_51"] = context["t_m_d"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["m_h_51"] = context["t_m_h"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                context["m_dh_51"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()

                context["m_n_56"] = context["t_m_n"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["m_d_56"] = context["t_m_d"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["m_h_56"] = context["t_m_h"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                context["m_dh_56"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()

                context["m_n_61"] = context["t_m_n"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["m_d_61"] = context["t_m_d"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["m_h_61"] = context["t_m_h"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                context["m_dh_61"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()

                context["m_n_66"] = context["t_m_n"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["m_d_66"] = context["t_m_d"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["m_h_66"] = context["t_m_h"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                context["m_dh_66"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()

                context["m_n_71"] = context["t_m_n"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["m_d_71"] = context["t_m_d"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["m_h_71"] = context["t_m_h"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                context["m_dh_71"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()

                context["m_n_76"] = context["t_m_n"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["m_d_76"] = context["t_m_d"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["m_h_76"] = context["t_m_h"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                context["m_dh_76"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()

                context["m_n_81"] = context["t_m_n"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["m_d_81"] = context["t_m_d"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["m_h_81"] = context["t_m_h"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                context["m_dh_81"] = context["t_m_dh"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                # Reporte de Factor de Riesgo
                bajo_riesgo = FactorDeRiesgo.objects.filter(resultado__lte=10,
                                                            beneficiario__jornada=context['jornada'].id,
                                                            beneficiario__de_seguimiento=True)
                moderado_riesgo = FactorDeRiesgo.objects.filter(resultado__gte=11, resultado__lte=19,
                                                                beneficiario__jornada=context['jornada'].id,
                                                                beneficiario__de_seguimiento=True)
                alto_riesgo = FactorDeRiesgo.objects.filter(resultado__gte=20,
                                                            beneficiario__jornada=context['jornada'].id,
                                                            beneficiario__de_seguimiento=True)

                h_bajo_riesgo = bajo_riesgo.filter(beneficiario__sexo=True, beneficiario__de_seguimiento=True)
                h_moderado_riesgo = moderado_riesgo.filter(beneficiario__sexo=True, beneficiario__de_seguimiento=True)
                #                context['debug'] = h_moderado_riesgo
                h_alto_riesgo = alto_riesgo.filter(beneficiario__sexo=True, beneficiario__de_seguimiento=True)

                m_bajo_riesgo = bajo_riesgo.filter(beneficiario__sexo=False, beneficiario__de_seguimiento=True)
                m_moderado_riesgo = moderado_riesgo.filter(beneficiario__sexo=False, beneficiario__de_seguimiento=True)
                m_alto_riesgo = alto_riesgo.filter(beneficiario__sexo=False, beneficiario__de_seguimiento=True)

                context['h_br_40'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['h_br_41'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                          beneficiario__edad_inicial__lte=45).count()
                context['h_br_46'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                          beneficiario__edad_inicial__lte=50).count()
                context['h_br_51'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                          beneficiario__edad_inicial__lte=55).count()
                context['h_br_56'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                          beneficiario__edad_inicial__lte=60).count()
                context['h_br_61'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                          beneficiario__edad_inicial__lte=65).count()
                context['h_br_66'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                          beneficiario__edad_inicial__lte=70).count()
                context['h_br_71'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                          beneficiario__edad_inicial__lte=75).count()
                context['h_br_76'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                          beneficiario__edad_inicial__lte=80).count()
                context['h_br_81'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['h_mr_40'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['h_mr_41'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                              beneficiario__edad_inicial__lte=45).count()
                context['h_mr_46'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                              beneficiario__edad_inicial__lte=50).count()
                context['h_mr_51'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                              beneficiario__edad_inicial__lte=55).count()
                context['h_mr_56'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                              beneficiario__edad_inicial__lte=60).count()
                context['h_mr_61'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                              beneficiario__edad_inicial__lte=65).count()
                context['h_mr_66'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                              beneficiario__edad_inicial__lte=70).count()
                context['h_mr_71'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                              beneficiario__edad_inicial__lte=75).count()
                context['h_mr_76'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                              beneficiario__edad_inicial__lte=80).count()
                context['h_mr_81'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['h_ar_40'] = h_alto_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['h_ar_41'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                          beneficiario__edad_inicial__lte=45).count()
                context['h_ar_46'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                          beneficiario__edad_inicial__lte=50).count()
                context['h_ar_51'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                          beneficiario__edad_inicial__lte=55).count()
                context['h_ar_56'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                          beneficiario__edad_inicial__lte=60).count()
                context['h_ar_61'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                          beneficiario__edad_inicial__lte=65).count()
                context['h_ar_66'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                          beneficiario__edad_inicial__lte=70).count()
                context['h_ar_71'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                          beneficiario__edad_inicial__lte=75).count()
                context['h_ar_76'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                          beneficiario__edad_inicial__lte=80).count()
                context['h_ar_81'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['m_br_40'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['m_br_41'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                          beneficiario__edad_inicial__lte=45).count()
                context['m_br_46'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                          beneficiario__edad_inicial__lte=50).count()
                context['m_br_51'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                          beneficiario__edad_inicial__lte=55).count()
                context['m_br_56'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                          beneficiario__edad_inicial__lte=60).count()
                context['m_br_61'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                          beneficiario__edad_inicial__lte=65).count()
                context['m_br_66'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                          beneficiario__edad_inicial__lte=70).count()
                context['m_br_71'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                          beneficiario__edad_inicial__lte=75).count()
                context['m_br_76'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                          beneficiario__edad_inicial__lte=80).count()
                context['m_br_81'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['m_mr_40'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['m_mr_41'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                              beneficiario__edad_inicial__lte=45).count()
                context['m_mr_46'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                              beneficiario__edad_inicial__lte=50).count()
                context['m_mr_51'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                              beneficiario__edad_inicial__lte=55).count()
                context['m_mr_56'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                              beneficiario__edad_inicial__lte=60).count()
                context['m_mr_61'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                              beneficiario__edad_inicial__lte=65).count()
                context['m_mr_66'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                              beneficiario__edad_inicial__lte=70).count()
                context['m_mr_71'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                              beneficiario__edad_inicial__lte=75).count()
                context['m_mr_76'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                              beneficiario__edad_inicial__lte=80).count()
                context['m_mr_81'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['m_ar_40'] = m_alto_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                context['m_ar_41'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                          beneficiario__edad_inicial__lte=45).count()
                context['m_ar_46'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                          beneficiario__edad_inicial__lte=50).count()
                context['m_ar_51'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                          beneficiario__edad_inicial__lte=55).count()
                context['m_ar_56'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                          beneficiario__edad_inicial__lte=60).count()
                context['m_ar_61'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                          beneficiario__edad_inicial__lte=65).count()
                context['m_ar_66'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                          beneficiario__edad_inicial__lte=70).count()
                context['m_ar_71'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                          beneficiario__edad_inicial__lte=75).count()
                context['m_ar_76'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                          beneficiario__edad_inicial__lte=80).count()
                context['m_ar_81'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                context['h_br'] = h_bajo_riesgo.count()
                context['h_mr'] = h_moderado_riesgo.count()
                context['h_ar'] = h_alto_riesgo.count()
                context['h_sd'] = total_hombres-context['h_br']-context['h_mr']-context['h_ar']

                context['h_br_p'] = percentage(context['h_br'], total_hombres)
                context['h_mr_p'] = percentage(context['h_mr'], total_hombres)
                context['h_ar_p'] = percentage(context['h_ar'], total_hombres)
                context['h_sd_p'] = percentage(context['h_sd'], total_hombres)

                fix_percentage(context, ["h_br_p", "h_mr_p", "h_ar_p", "h_sd_p"])

                context['m_br'] = m_bajo_riesgo.count()
                context['m_mr'] = m_moderado_riesgo.count()
                context['m_ar'] = m_alto_riesgo.count()
                context['m_sd'] = total_mujeres - context['m_br'] - context['m_mr'] - context['m_ar']

                context['m_br_p'] = percentage(context['m_br'], total_mujeres)
                context['m_mr_p'] = percentage(context['m_mr'], total_mujeres)
                context['m_ar_p'] = percentage(context['m_ar'], total_mujeres)
                context['m_sd_p'] = percentage(context['m_sd'], total_mujeres)

                fix_percentage(context, ["m_br_p", "m_mr_p", "m_ar_p", "m_sd_p"])

                # Reporte de Factor de Riesgo
                malnutrición = MalnutricionInflamacion.objects.filter(beneficiario__jornada=context['jornada'].id, beneficiario__de_seguimiento=True).values(
                    'pk', 'beneficiario', 'fecha_creacion', 'fecha', 'resultado', 'beneficiario__sexo')
                beneficiarios_malnutricion = malnutrición.values('beneficiario')
                id_benef = []
                for set in beneficiarios_malnutricion:
                    if set['beneficiario'] not in id_benef:
                        id_benef.append(set['beneficiario'])

                pk_benf = []
                for beneficiario in id_benef:
                    pk_benf.append(malnutrición.filter(beneficiario=beneficiario).latest('fecha')["pk"])

                malnutrición_filtered = malnutrición.filter(pk__in=pk_benf)

                context['est_nut_a'] = malnutrición_filtered.filter(resultado=0).count()
                context['des_nut_leve_b'] = malnutrición_filtered.filter(resultado__gte=1, resultado__lte=9).count()
                context['des_nut_mod_c'] = malnutrición_filtered.filter(resultado__gte=10, resultado__lte=19).count()
                context['des_nut_grave_d'] = malnutrición_filtered.filter(resultado__gte=20, resultado__lte=29).count()
                context['des_nut_grav_e'] = malnutrición_filtered.filter(resultado__gte=30).count()
                context['nutricion_por'] = malnutrición_filtered.count()

                if(malnutrición_filtered.count() > 0):
                    context['p_est_nut_a'] = context['est_nut_a']/context['nutricion_por'] * 100
                    context['p_des_nut_leve_b'] = context['des_nut_leve_b']/context['nutricion_por'] * 100
                    context['p_des_nut_mod_c'] = context['des_nut_mod_c']/context['nutricion_por'] * 100
                    context['p_des_nut_grave_d'] = context['des_nut_grave_d']/context['nutricion_por'] * 100
                    context['p_des_nut_grav_e'] = context['des_nut_grav_e']/context['nutricion_por'] * 100

                # Reporte controlados y descontrolados

                    # Hipertensos controlados/descontrolados/sin datos

                hipertensos = context["beneficiarios"].filter(diabetico_hipertenso=2)
                h_total = hipertensos.count()
                h_controlados = 0
                h_descontrolados = 0
                h_nodatos = 0
                for p in range(h_total):
                    tamizaje = TamizajeNutricional.objects.filter(
                        beneficiario=hipertensos[p].id, beneficiario__de_seguimiento=True)
                    if(len(tamizaje) == 0):
                        h_nodatos += 1
                    else:
                        actual = tamizaje.latest('fecha')
                        if(actual.presion_sistolica >= 140 and actual.presion_diastolica >= 90):
                            h_descontrolados += 1
                        else:
                            h_controlados += 1

                context['c_tension_hipertension'] = h_controlados
                context['nc_tension_hipertension'] = h_descontrolados
                context['sd_tension_hipertension'] = h_nodatos

                context['t_hipertension'] = percentage(h_controlados, h_total)
                context['t_nhipertension'] = percentage(h_descontrolados, h_total)
                context['sd_hipertension'] = percentage(h_nodatos, h_total)

                fix_percentage(context, ["t_hipertension", "t_nhipertension", "sd_hipertension"])

                # diabeticos controlados/descontrolados/sin datos
                context["diabetico_t"] = context["beneficiarios"].filter(diabetico_hipertenso=1).count()

                with connection.cursor() as diabc:
                    diabc.execute('''select jor.id, max(jor.id) as jornada, glucosa, hba1c
                                    from "Beneficiarios_beneficiario" as jor
                                    inner join (select fgc.beneficiario_id, max(fgc.id) as glucosa, hba1c
                                    from "Formularios_glucosacapilar" as fgc
                                    inner join (select asd.beneficiario_id, max(asd.id) as hba1c
                                    from "Formularios_hemoglobinaglucosilada" as asd
                                    where asd.hemoglobina_glucosilada < 7
                                    group by asd.beneficiario_id) as fhg
                                    on fhg.beneficiario_id = fgc.beneficiario_id
                                    where glucosa < 130 group by fgc.beneficiario_id, hba1c)
                                    as fght on jor.id = fght.beneficiario_id
                                    where jor.jornada_id = (%s)
                                    group by jor.id, glucosa, hba1c ''',
                                  (context['jornada'].id,))

                context['diab_cont'] = diabc.rowcount
                context['diab_ncont'] = context["diabetico_t"] - context['diab_cont']
                if (context['diabetico_t'] == 0):
                    context['sd_diabetico'] = 0
                    context['sd_d'] = 0
                    context['diab_ncont'] = 0
                    context['diab_ncont_p'] = 0
                    context['diabetico_t'] = context['diab_cont'] + context['diab_ncont']
                else:
                    if (context['diab_cont'] == 0 and context['diab_ncont'] == 0):
                        context['sd_diabetico'] = 0
                    else:
                        context['sd_diabetico'] = context['diabetico_t'] - context['diab_cont'] - context['diab_ncont']
                    context['sd_d'] = percentage(context['sd_diabetico'], context['diabetico_t'])
                    context['diab_ncont_p'] = percentage(context['diab_ncont'], context['diabetico_t'])
                context['diab_cont_p'] = percentage(context['diab_cont'], context['diabetico_t'])

                # diabeticos/hipertensos controlados/descontrolados/sin datos
                context["diabetico_hipertenso_t"] = context["beneficiarios"].filter(diabetico_hipertenso=3).count()

                with connection.cursor() as dhc:
                    dhc.execute('''select jor.id, max(jor.id) as jornada, glucosa, hba1c, presion
                                from "Beneficiarios_beneficiario" as jor
                                inner join (select fgc.beneficiario_id, max(fgc.id) as glucosa, hba1c, presion
                                from "Formularios_glucosacapilar" as fgc
                                inner join (select asd.beneficiario_id, max(asd.id) as hba1c, presion
                                from "Formularios_hemoglobinaglucosilada" as asd
                                inner join (select qwerty.beneficiario_id, max(qwerty.id) as presion
                                from "Formularios_tamizajenutricional" as qwerty
                                where presion_sistolica < 140 and presion_diastolica < 90
                                group by qwerty.beneficiario_id) as fgh
                                on asd.beneficiario_id = fgh.beneficiario_id
                                where asd.hemoglobina_glucosilada < 7
                                group by asd.beneficiario_id, presion) as fhg
                                on fhg.beneficiario_id = fgc.beneficiario_id
                                where glucosa < 130 group by fgc.beneficiario_id, hba1c, presion)
                                as fght on jor.id = fght.beneficiario_id
                                where jor.jornada_id = (%s)
                                group by jor.id, glucosa, hba1c, presion ''',
                                (context['jornada'].id,))

                context['dia_hip_cont'] = dhc.rowcount
                context['dia_hip_no_cont'] = context["diabetico_hipertenso_t"] - context['dia_hip_cont']
                if (context['diabetico_hipertenso_t'] == 0):
                    context['sd_diabetico_hipertenso'] = 0
                    context['sd_dh'] = 0
                    context['dia_hip_no_cont'] = 0
                    context['dia_hip_no_cont_p'] = 0
                    context['diabetico_hipertenso_t'] = context['dia_hip_cont'] + context['dia_hip_no_cont']
                else:
                    if (context['dia_hip_cont'] == 0 and context['dia_hip_no_cont'] == 0):
                        context['sd_diabetico_hipertenso'] = 0
                    else:
                        context['sd_diabetico_hipertenso'] = context['diabetico_hipertenso_t'] - \
                            context['dia_hip_cont'] - context['dia_hip_no_cont']
                    context['sd_dh'] = percentage(context['sd_diabetico_hipertenso'],
                                                  context['diabetico_hipertenso_t'])
                    context['dia_hip_no_cont_p'] = percentage(
                        context['dia_hip_no_cont'], context['diabetico_hipertenso_t'])
                context['dia_hip_cont_p'] = percentage(context['dia_hip_cont'], context['diabetico_hipertenso_t'])

                # Reporte de evaluaciones de platicas
                evaluacion = EvaluacionPlaticas.objects.filter(jornada=context['jornada'].id).values(
                    'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11')

                context["evaluacion"] = evaluacion
                context["evaluacion_count"] = evaluacion.count()

                context["correctas"], context["incorrectas"] = evaluate_data(evaluacion)

                # Adherencia al tratamiento
                context["a_t_re"] = 0
                context["a_t_ne"] = 0
                context["a_t_mo"] = 0
                context["a_t_ac"] = 0
                context["a_t_ad"] = 0

                context["a_h_re"] = 0
                context["a_h_ne"] = 0
                context["a_h_mo"] = 0
                context["a_h_ac"] = 0
                context["a_h_ad"] = 0

                context["a_m_re"] = 0
                context["a_m_ne"] = 0
                context["a_m_mo"] = 0
                context["a_m_ac"] = 0
                context["a_m_ad"] = 0

                context["adherencia"] = False

                for b in context["beneficiarios"]:
                    if AdherenciaTratamiento.objects.filter(beneficiario=b).exists():
                        at = AdherenciaTratamiento.objects.filter(beneficiario=b).order_by('-id')[0]
                        context["adherencia"] = True
                        if b.sexo:
                            if at.interpretacion == "Rechazo":
                                context["a_t_re"] += 1
                                context["a_h_re"] += 1
                            elif at.interpretacion == "Negación":
                                context["a_t_ne"] += 1
                                context["a_h_ne"] += 1
                            elif at.interpretacion == "Modificación":
                                context["a_t_mo"] += 1
                                context["a_h_mo"] += 1
                            elif at.interpretacion == "Aceptación":
                                context["a_t_ac"] += 1
                                context["a_h_ac"] += 1
                            elif at.interpretacion == "Adherencia":
                                context["a_t_ad"] += 1
                                context["a_h_ad"] += 1
                        else:
                            if at.interpretacion == "Rechazo":
                                context["a_t_re"] += 1
                                context["a_m_re"] += 1
                            elif at.interpretacion == "Negación":
                                context["a_t_ne"] += 1
                                context["a_m_ne"] += 1
                            elif at.interpretacion == "Modificación":
                                context["a_t_mo"] += 1
                                context["a_m_mo"] += 1
                            elif at.interpretacion == "Aceptación":
                                context["a_t_ac"] += 1
                                context["a_m_ac"] += 1
                            elif at.interpretacion == "Adherencia":
                                context["a_t_ad"] += 1
                                context["a_m_ad"] += 1

                # Hamilton
                context["h_t_md"] = 0
                context["h_t_ds"] = 0
                context["h_t_dm"] = 0
                context["h_t_dl"] = 0
                context["h_t_sd"] = 0

                context["h_h_md"] = 0
                context["h_h_ds"] = 0
                context["h_h_dm"] = 0
                context["h_h_dl"] = 0
                context["h_h_sd"] = 0

                context["h_m_md"] = 0
                context["h_m_ds"] = 0
                context["h_m_dm"] = 0
                context["h_m_dl"] = 0
                context["h_m_sd"] = 0

                context["hamilton"] = False

                for b in context["beneficiarios"]:
                    if EscalaHamilton.objects.filter(beneficiario=b).exists():
                        eh = EscalaHamilton.objects.filter(beneficiario=b).order_by('-id')[0]
                        context["hamilton"] = True
                        if b.sexo:
                            if eh.interpretacion == "No deprimido":
                                context["h_t_sd"] += 1
                                context["h_h_sd"] += 1
                            elif eh.interpretacion == "Depresión ligera/menor":
                                context["h_t_dl"] += 1
                                context["h_h_dl"] += 1
                            elif eh.interpretacion == "Depresión moderada":
                                context["h_t_dm"] += 1
                                context["h_h_dm"] += 1
                            elif eh.interpretacion == "Depresión severa":
                                context["h_t_ds"] += 1
                                context["h_h_ds"] += 1
                            elif eh.interpretacion == "Depresión muy severa":
                                context["h_t_md"] += 1
                                context["h_h_md"] += 1
                        else:
                            if eh.interpretacion == "No deprimido":
                                context["h_t_sd"] += 1
                                context["h_m_sd"] += 1
                            elif eh.interpretacion == "Depresión ligera/menor":
                                context["h_t_dl"] += 1
                                context["h_m_dl"] += 1
                            elif eh.interpretacion == "Depresión moderada":
                                context["h_t_dm"] += 1
                                context["h_m_dm"] += 1
                            elif eh.interpretacion == "Depresión severa":
                                context["h_t_ds"] += 1
                                context["h_m_ds"] += 1
                            elif eh.interpretacion == "Depresión muy severa":
                                context["h_t_md"] += 1
                                context["h_m_md"] += 1
        return context
