from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http import *
from django.urls import *
from Beneficiarios.models import *
from Formularios.models import *
from Proyectos.models import *
from Reportes.models import *
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import date
from django.db.models import Q
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


class CompareJornadaView(PermissionRequiredMixin, TemplateView):
    permission_required = ('Reportes.view_reportes')
    model = Reportes
    template_name = "Reportes/compare_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jornadas"] = Jornada.objects.all()
        context["is_post"] = False
        return context

    def post(self, request, *args, **kwargs):
        jornadasToReport = request.POST.getlist('jornadas')
        jornadasInfo = getJornadasData(jornadasToReport)
        jornadasInfo = orderData(jornadasInfo)
        jornadas = Jornada.objects.all()

        return render(request, 'Reportes/compare_view.html', {'jornadas': jornadas, 'jornadasInfo': jornadasInfo, 'is_post': True})


def orderData(jornadasInfo):
    info = {}
    socio = []
    dh = []
    fdr = []
    estadificacion = []
    malnutricion = []
    control = []
    adherencia = []
    hamilton = []
    i = 0
    for j in jornadasInfo:
        j["socio"]["counter"] = i
        socio.append(j["socio"])
        j["dh"]["counter"] = i
        dh.append(j["dh"])
        j["fdr"]["counter"] = i
        fdr.append(j["fdr"])
        j["estadificacion"]["counter"] = i
        estadificacion.append(j["estadificacion"])
        j["malnutricion"]["counter"] = i
        malnutricion.append(j["malnutricion"])
        j["control"]["counter"] = i
        control.append(j["control"])
        j["adherencia"]["counter"] = i
        adherencia.append(j["adherencia"])
        j["hamilton"]["counter"] = i
        hamilton.append(j["hamilton"])
        i += 1
    info["Sociodemografico"] = socio
    info["DiabetesHipertension"] = dh
    info["FactorRiesgo"] = fdr
    info["Estadificacion"] = estadificacion
    info["ControladoDescontrolado"] = control
    info["MalnutricionInflamacion"] = malnutricion
    info["AdherenciaTratamiento"] = adherencia
    info["EscalaHamilton"] = hamilton
    return info


def getJornadasData(jornadas):
    jornadasReport = []
    for j in jornadas:
        oneJornada = {}

        jornadaRep = {}
        jornadaCleanReport = {}
        jornadaCleanReportSocio = {}
        jornadaCleanReportDH = {}
        jornadaCleanReportFDR = {}
        jornadaCleanReportEstadificacion = {}
        jornadaCleanReportMalnutricion = {}
        jornadaCleanReportControl = {}
        jornadaCleanReportAdherencia = {}
        jornadaCleanReportHamilton = {}

        jornadaRep["jornada"] = get_object_or_404(Jornada, pk=j)
        jornadaRep["jornadaName"] = jornadaRep["jornada"].nombre

        jornadaRep["beneficiarios"] = Beneficiario.objects.filter(jornada=jornadaRep["jornada"].id)
        jornadaRep["total"] = jornadaRep["beneficiarios"].count()

        jornadaCleanReportSocio["Nombre"] = jornadaRep["jornadaName"]
        if jornadaRep["total"] is not 0:
            if 1 == 1:
                # Reporte sociodemográfico -----------------------------------------------------
                jornadaRep["total_hombres"] = jornadaRep["beneficiarios"].filter(sexo=True)
                jornadaRep["total_mujeres"] = jornadaRep["beneficiarios"].filter(sexo=False)
                jornadaRep["p_h"] = percentage(jornadaRep["total_hombres"].count(), jornadaRep["total"])
                jornadaRep["p_m"] = percentage(jornadaRep["total_mujeres"].count(), jornadaRep["total"])
                jornadaRep["h_40"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                jornadaRep["h_41"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                jornadaRep["h_46"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                jornadaRep["h_51"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                jornadaRep["h_56"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                jornadaRep["h_61"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                jornadaRep["h_66"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                jornadaRep["h_71"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                jornadaRep["h_76"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                jornadaRep["h_81"] = jornadaRep["total_hombres"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                jornadaRep["m_40"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                jornadaRep["m_41"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                jornadaRep["m_46"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                jornadaRep["m_51"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                jornadaRep["m_56"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                jornadaRep["m_61"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                jornadaRep["m_66"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                jornadaRep["m_71"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                jornadaRep["m_76"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                jornadaRep["m_81"] = jornadaRep["total_mujeres"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                G1 = Clasificacion.objects.filter(Q(categoria_gfr="G1") & Q(
                    categoria_gfr_estimada="G1") & Q(beneficiario__jornada=jornadaRep["jornada"]))
                G2 = Clasificacion.objects.filter(Q(categoria_gfr="G2") & Q(
                    categoria_gfr_estimada="G2") & Q(beneficiario__jornada=jornadaRep["jornada"]))
                G3a = Clasificacion.objects.filter(Q(categoria_gfr="G3a") & Q(
                    categoria_gfr_estimada="G3a") & Q(beneficiario__jornada=jornadaRep["jornada"]))
                G3b = Clasificacion.objects.filter(Q(categoria_gfr="G3b") & Q(
                    categoria_gfr_estimada="G3b") & Q(beneficiario__jornada=jornadaRep["jornada"]))
                G4 = Clasificacion.objects.filter(Q(categoria_gfr="G4") & Q(
                    categoria_gfr_estimada="G4") & Q(beneficiario__jornada=jornadaRep["jornada"]))
                G5 = Clasificacion.objects.filter(Q(categoria_gfr="G5") & Q(
                    categoria_gfr_estimada="G5") & Q(beneficiario__jornada=jornadaRep["jornada"]))

                total_class = G1.count() + G2.count() + G3a.count() + G3b.count() + G4.count() + G5.count()
                jornadaRep["G1_p"] = percentage(G1.count(), total_class)
                jornadaRep["G2_p"] = percentage(G2.count(), total_class)
                jornadaRep["G3a_p"] = percentage(G3a.count(), total_class)
                jornadaRep["G3b_p"] = percentage(G3b.count(), total_class)
                jornadaRep["G4_p"] = percentage(G4.count(), total_class)
                jornadaRep["G5_p"] = percentage(G5.count(), total_class)

                fix_percentage(jornadaRep, ["G1_p", "G2_p", "G3a_p", "G3b_p", "G4_p", "G5_p"])

                jornadaRep["m_G1"] = G1.filter(beneficiario__sexo=False)
                jornadaRep["m_G2"] = G2.filter(beneficiario__sexo=False)
                jornadaRep["m_G3a"] = G3a.filter(beneficiario__sexo=False)
                jornadaRep["m_G3b"] = G3b.filter(beneficiario__sexo=False)
                jornadaRep["m_G4"] = G4.filter(beneficiario__sexo=False)
                jornadaRep["m_G5"] = G5.filter(beneficiario__sexo=False)

                jornadaRep["m_G1_p"] = percentage(jornadaRep['m_G1'].count(), G1.count())
                jornadaRep["m_G2_p"] = percentage(jornadaRep['m_G2'].count(), G2.count())
                jornadaRep["m_G3a_p"] = percentage(jornadaRep['m_G3a'].count(), G3a.count())
                jornadaRep["m_G3b_p"] = percentage(jornadaRep['m_G3b'].count(), G3b.count())
                jornadaRep["m_G4_p"] = percentage(jornadaRep['m_G4'].count(), G4.count())
                jornadaRep["m_G5_p"] = percentage(jornadaRep['m_G5'].count(), G5.count())

                fix_percentage(jornadaRep, ["m_G1_p", "m_G2_p", "m_G3a_p", "m_G3b_p", "m_G4_p", "m_G5_p"])

                jornadaRep["h_G1"] = G1.filter(beneficiario__sexo=True)
                jornadaRep["h_G2"] = G2.filter(beneficiario__sexo=True)
                jornadaRep["h_G3a"] = G3a.filter(beneficiario__sexo=True)
                jornadaRep["h_G3b"] = G3b.filter(beneficiario__sexo=True)
                jornadaRep["h_G4"] = G4.filter(beneficiario__sexo=True)
                jornadaRep["h_G5"] = G5.filter(beneficiario__sexo=True)

                jornadaRep["h_G1_p"] = percentage(jornadaRep['h_G1'].count(), G1.count())
                jornadaRep["h_G2_p"] = percentage(jornadaRep['h_G2'].count(), G2.count())
                jornadaRep["h_G3a_p"] = percentage(jornadaRep['h_G3a'].count(), G3a.count())
                jornadaRep["h_G3b_p"] = percentage(jornadaRep['h_G3b'].count(), G3b.count())
                jornadaRep["h_G4_p"] = percentage(jornadaRep['h_G4'].count(), G4.count())
                jornadaRep["h_G5_p"] = percentage(jornadaRep['h_G5'].count(), G5.count())

                fix_percentage(jornadaRep, ["h_G1_p", "h_G2_p", "h_G3a_p", "h_G3b_p", "h_G4_p", "h_G5_p"])

                jornadaRep["h_G1_40"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["m_G1_40"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["h_G1_41"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["m_G1_41"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["h_G1_46"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["m_G1_46"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["h_G1_51"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["m_G1_51"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["h_G1_56"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["m_G1_56"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["h_G1_61"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["m_G1_61"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["h_G1_66"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["m_G1_66"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["h_G1_71"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["m_G1_71"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["h_G1_76"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["m_G1_76"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["h_G1_81"] = jornadaRep["h_G1"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                jornadaRep["m_G1_81"] = jornadaRep["m_G1"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep["h_G2_40"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["m_G2_40"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["h_G2_41"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["m_G2_41"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["h_G2_46"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["m_G2_46"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["h_G2_51"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["m_G2_51"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["h_G2_56"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["m_G2_56"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["h_G2_61"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["m_G2_61"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["h_G2_66"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["m_G2_66"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["h_G2_71"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["m_G2_71"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["h_G2_76"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["m_G2_76"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["h_G2_81"] = jornadaRep["h_G2"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                jornadaRep["m_G2_81"] = jornadaRep["m_G2"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep["h_G3a_40"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["m_G3a_40"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["h_G3a_41"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["m_G3a_41"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["h_G3a_46"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["m_G3a_46"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["h_G3a_51"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["m_G3a_51"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["h_G3a_56"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["m_G3a_56"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["h_G3a_61"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["m_G3a_61"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["h_G3a_66"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["m_G3a_66"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["h_G3a_71"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["m_G3a_71"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["h_G3a_76"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["m_G3a_76"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["h_G3a_81"] = jornadaRep["h_G3a"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                jornadaRep["m_G3a_81"] = jornadaRep["m_G3a"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep["h_G3b_40"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["m_G3b_40"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["h_G3b_41"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["m_G3b_41"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["h_G3b_46"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["m_G3b_46"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["h_G3b_51"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["m_G3b_51"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["h_G3b_56"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["m_G3b_56"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["h_G3b_61"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["m_G3b_61"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["h_G3b_66"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["m_G3b_66"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["h_G3b_71"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["m_G3b_71"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["h_G3b_76"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["m_G3b_76"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["h_G3b_81"] = jornadaRep["h_G3b"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                jornadaRep["m_G3b_81"] = jornadaRep["m_G3b"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep["h_G4_40"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["m_G4_40"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["h_G4_41"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["m_G4_41"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["h_G4_46"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["m_G4_46"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["h_G4_51"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["m_G4_51"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["h_G4_56"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["m_G4_56"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["h_G4_61"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["m_G4_61"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["h_G4_66"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["m_G4_66"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["h_G4_71"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["m_G4_71"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["h_G4_76"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["m_G4_76"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["h_G4_81"] = jornadaRep["h_G4"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                jornadaRep["m_G4_81"] = jornadaRep["m_G4"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep["h_G5_40"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["m_G5_40"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=41).filter(beneficiario__edad_inicial__gte=1).count()
                jornadaRep["h_G5_41"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["m_G5_41"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=46).filter(beneficiario__edad_inicial__gte=41).count()
                jornadaRep["h_G5_46"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["m_G5_46"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=51).filter(beneficiario__edad_inicial__gte=46).count()
                jornadaRep["h_G5_51"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["m_G5_51"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=56).filter(beneficiario__edad_inicial__gte=51).count()
                jornadaRep["h_G5_56"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["m_G5_56"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=61).filter(beneficiario__edad_inicial__gte=56).count()
                jornadaRep["h_G5_61"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["m_G5_61"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=66).filter(beneficiario__edad_inicial__gte=61).count()
                jornadaRep["h_G5_66"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["m_G5_66"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=71).filter(beneficiario__edad_inicial__gte=66).count()
                jornadaRep["h_G5_71"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["m_G5_71"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=76).filter(beneficiario__edad_inicial__gte=71).count()
                jornadaRep["h_G5_76"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["m_G5_76"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=81).filter(beneficiario__edad_inicial__gte=76).count()
                jornadaRep["h_G5_81"] = jornadaRep["h_G5"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()
                jornadaRep["m_G5_81"] = jornadaRep["m_G5"].exclude(
                    beneficiario__edad_inicial__gte=120).filter(beneficiario__edad_inicial__gte=81).count()

                # Reporte diabetes / hipertensión
                jornadaRep["t_h_n"] = jornadaRep["total_hombres"].filter(diabetico_hipertenso=0)
                jornadaRep["t_h_d"] = jornadaRep["total_hombres"].filter(diabetico_hipertenso=1)
                jornadaRep["t_h_h"] = jornadaRep["total_hombres"].filter(diabetico_hipertenso=2)
                jornadaRep["t_h_dh"] = jornadaRep["total_hombres"].filter(diabetico_hipertenso=3)
                jornadaRep["t_m_n"] = jornadaRep["total_mujeres"].filter(diabetico_hipertenso=0)
                jornadaRep["t_m_d"] = jornadaRep["total_mujeres"].filter(diabetico_hipertenso=1)
                jornadaRep["t_m_h"] = jornadaRep["total_mujeres"].filter(diabetico_hipertenso=2)
                jornadaRep["t_m_dh"] = jornadaRep["total_mujeres"].filter(diabetico_hipertenso=3)

                total_hombres = jornadaRep["total_hombres"].count()
                total_mujeres = jornadaRep["total_mujeres"].count()

                jornadaRep["p_h_n"] = percentage(jornadaRep["t_h_n"].count(), total_hombres)
                jornadaRep["p_h_d"] = percentage(jornadaRep["t_h_d"].count(), total_hombres)
                jornadaRep["p_h_h"] = percentage(jornadaRep["t_h_h"].count(), total_hombres)
                jornadaRep["p_h_dh"] = percentage(jornadaRep["t_h_dh"].count(), total_hombres)
                jornadaRep["p_m_n"] = percentage(jornadaRep["t_m_n"].count(), total_mujeres)
                jornadaRep["p_m_d"] = percentage(jornadaRep["t_m_d"].count(), total_mujeres)
                jornadaRep["p_m_h"] = percentage(jornadaRep["t_m_h"].count(), total_mujeres)
                jornadaRep["p_m_dh"] = percentage(jornadaRep["t_m_dh"].count(), total_mujeres)

                fix_percentage(jornadaRep, ["p_h_n", "p_h_d", "p_h_h", "p_h_dh"])
                fix_percentage(jornadaRep, ["p_m_n", "p_m_d", "p_m_h", "p_m_dh"])

                jornadaRep["h_n_40"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                jornadaRep["h_d_40"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                jornadaRep["h_h_40"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                jornadaRep["h_dh_40"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()

                jornadaRep["h_n_41"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                jornadaRep["h_d_41"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                jornadaRep["h_h_41"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                jornadaRep["h_dh_41"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()

                jornadaRep["h_n_46"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                jornadaRep["h_d_46"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                jornadaRep["h_h_46"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                jornadaRep["h_dh_46"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()

                jornadaRep["h_n_51"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                jornadaRep["h_d_51"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                jornadaRep["h_h_51"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                jornadaRep["h_dh_51"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()

                jornadaRep["h_n_56"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                jornadaRep["h_d_56"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                jornadaRep["h_h_56"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                jornadaRep["h_dh_56"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()

                jornadaRep["h_n_61"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                jornadaRep["h_d_61"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                jornadaRep["h_h_61"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                jornadaRep["h_dh_61"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()

                jornadaRep["h_n_66"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                jornadaRep["h_d_66"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                jornadaRep["h_h_66"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                jornadaRep["h_dh_66"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()

                jornadaRep["h_n_71"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                jornadaRep["h_d_71"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                jornadaRep["h_h_71"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                jornadaRep["h_dh_71"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()

                jornadaRep["h_n_76"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                jornadaRep["h_d_76"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                jornadaRep["h_h_76"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                jornadaRep["h_dh_76"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()

                jornadaRep["h_n_81"] = jornadaRep["t_h_n"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                jornadaRep["h_d_81"] = jornadaRep["t_h_d"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                jornadaRep["h_h_81"] = jornadaRep["t_h_h"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                jornadaRep["h_dh_81"] = jornadaRep["t_h_dh"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                # Mujeres
                jornadaRep["m_n_40"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                jornadaRep["m_d_40"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                jornadaRep["m_h_40"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()
                jornadaRep["m_dh_40"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=41).filter(edad_inicial__gte=1).count()

                jornadaRep["m_n_41"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                jornadaRep["m_d_41"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                jornadaRep["m_h_41"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()
                jornadaRep["m_dh_41"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=46).filter(edad_inicial__gte=41).count()

                jornadaRep["m_n_46"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                jornadaRep["m_d_46"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                jornadaRep["m_h_46"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()
                jornadaRep["m_dh_46"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=51).filter(edad_inicial__gte=46).count()

                jornadaRep["m_n_51"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                jornadaRep["m_d_51"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                jornadaRep["m_h_51"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()
                jornadaRep["m_dh_51"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=56).filter(edad_inicial__gte=51).count()

                jornadaRep["m_n_56"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                jornadaRep["m_d_56"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                jornadaRep["m_h_56"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()
                jornadaRep["m_dh_56"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=61).filter(edad_inicial__gte=56).count()

                jornadaRep["m_n_61"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                jornadaRep["m_d_61"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                jornadaRep["m_h_61"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()
                jornadaRep["m_dh_61"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=66).filter(edad_inicial__gte=61).count()

                jornadaRep["m_n_66"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                jornadaRep["m_d_66"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                jornadaRep["m_h_66"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()
                jornadaRep["m_dh_66"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=71).filter(edad_inicial__gte=66).count()

                jornadaRep["m_n_71"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                jornadaRep["m_d_71"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                jornadaRep["m_h_71"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()
                jornadaRep["m_dh_71"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=76).filter(edad_inicial__gte=71).count()

                jornadaRep["m_n_76"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                jornadaRep["m_d_76"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                jornadaRep["m_h_76"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()
                jornadaRep["m_dh_76"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=81).filter(edad_inicial__gte=76).count()

                jornadaRep["m_n_81"] = jornadaRep["t_m_n"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                jornadaRep["m_d_81"] = jornadaRep["t_m_d"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                jornadaRep["m_h_81"] = jornadaRep["t_m_h"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()
                jornadaRep["m_dh_81"] = jornadaRep["t_m_dh"].exclude(
                    edad_inicial__gte=120).filter(edad_inicial__gte=81).count()

                # Reporte de Factor de Riesgo
                bajo_riesgo = FactorDeRiesgo.objects.filter(resultado__lte=10,
                                                            beneficiario__jornada=jornadaRep['jornada'].id)
                moderado_riesgo = FactorDeRiesgo.objects.filter(resultado__gte=11, resultado__lte=19,
                                                                beneficiario__jornada=jornadaRep['jornada'].id)
                alto_riesgo = FactorDeRiesgo.objects.filter(resultado__gte=20,
                                                            beneficiario__jornada=jornadaRep['jornada'].id)

                h_bajo_riesgo = bajo_riesgo.filter(beneficiario__sexo=True)
                h_moderado_riesgo = moderado_riesgo.filter(beneficiario__sexo=True)
                #jornadaRep['debug'] = h_moderado_riesgo
                h_alto_riesgo = alto_riesgo.filter(beneficiario__sexo=True)

                m_bajo_riesgo = bajo_riesgo.filter(beneficiario__sexo=False)
                m_moderado_riesgo = moderado_riesgo.filter(beneficiario__sexo=False)
                m_alto_riesgo = alto_riesgo.filter(beneficiario__sexo=False)

                jornadaRep['h_br_40'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                jornadaRep['h_br_41'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                             beneficiario__edad_inicial__lte=45).count()
                jornadaRep['h_br_46'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                             beneficiario__edad_inicial__lte=50).count()
                jornadaRep['h_br_51'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                             beneficiario__edad_inicial__lte=55).count()
                jornadaRep['h_br_56'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                             beneficiario__edad_inicial__lte=60).count()
                jornadaRep['h_br_61'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                             beneficiario__edad_inicial__lte=65).count()
                jornadaRep['h_br_66'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                             beneficiario__edad_inicial__lte=70).count()
                jornadaRep['h_br_71'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                             beneficiario__edad_inicial__lte=75).count()
                jornadaRep['h_br_76'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                             beneficiario__edad_inicial__lte=80).count()
                jornadaRep['h_br_81'] = h_bajo_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep['h_mr_40'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                jornadaRep['h_mr_41'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                                 beneficiario__edad_inicial__lte=45).count()
                jornadaRep['h_mr_46'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                                 beneficiario__edad_inicial__lte=50).count()
                jornadaRep['h_mr_51'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                                 beneficiario__edad_inicial__lte=55).count()
                jornadaRep['h_mr_56'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                                 beneficiario__edad_inicial__lte=60).count()
                jornadaRep['h_mr_61'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                                 beneficiario__edad_inicial__lte=65).count()
                jornadaRep['h_mr_66'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                                 beneficiario__edad_inicial__lte=70).count()
                jornadaRep['h_mr_71'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                                 beneficiario__edad_inicial__lte=75).count()
                jornadaRep['h_mr_76'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                                 beneficiario__edad_inicial__lte=80).count()
                jornadaRep['h_mr_81'] = h_moderado_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep['h_ar_40'] = h_alto_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                jornadaRep['h_ar_41'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                             beneficiario__edad_inicial__lte=45).count()
                jornadaRep['h_ar_46'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                             beneficiario__edad_inicial__lte=50).count()
                jornadaRep['h_ar_51'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                             beneficiario__edad_inicial__lte=55).count()
                jornadaRep['h_ar_56'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                             beneficiario__edad_inicial__lte=60).count()
                jornadaRep['h_ar_61'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                             beneficiario__edad_inicial__lte=65).count()
                jornadaRep['h_ar_66'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                             beneficiario__edad_inicial__lte=70).count()
                jornadaRep['h_ar_71'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                             beneficiario__edad_inicial__lte=75).count()
                jornadaRep['h_ar_76'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                             beneficiario__edad_inicial__lte=80).count()
                jornadaRep['h_ar_81'] = h_alto_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep['m_br_40'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                jornadaRep['m_br_41'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                             beneficiario__edad_inicial__lte=45).count()
                jornadaRep['m_br_46'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                             beneficiario__edad_inicial__lte=50).count()
                jornadaRep['m_br_51'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                             beneficiario__edad_inicial__lte=55).count()
                jornadaRep['m_br_56'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                             beneficiario__edad_inicial__lte=60).count()
                jornadaRep['m_br_61'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                             beneficiario__edad_inicial__lte=65).count()
                jornadaRep['m_br_66'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                             beneficiario__edad_inicial__lte=70).count()
                jornadaRep['m_br_71'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                             beneficiario__edad_inicial__lte=75).count()
                jornadaRep['m_br_76'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                             beneficiario__edad_inicial__lte=80).count()
                jornadaRep['m_br_81'] = m_bajo_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep['m_mr_40'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                jornadaRep['m_mr_41'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                                 beneficiario__edad_inicial__lte=45).count()
                jornadaRep['m_mr_46'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                                 beneficiario__edad_inicial__lte=50).count()
                jornadaRep['m_mr_51'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                                 beneficiario__edad_inicial__lte=55).count()
                jornadaRep['m_mr_56'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                                 beneficiario__edad_inicial__lte=60).count()
                jornadaRep['m_mr_61'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                                 beneficiario__edad_inicial__lte=65).count()
                jornadaRep['m_mr_66'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                                 beneficiario__edad_inicial__lte=70).count()
                jornadaRep['m_mr_71'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                                 beneficiario__edad_inicial__lte=75).count()
                jornadaRep['m_mr_76'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                                 beneficiario__edad_inicial__lte=80).count()
                jornadaRep['m_mr_81'] = m_moderado_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep['m_ar_40'] = m_alto_riesgo.filter(beneficiario__edad_inicial__lte=40).count()
                jornadaRep['m_ar_41'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=41,
                                                             beneficiario__edad_inicial__lte=45).count()
                jornadaRep['m_ar_46'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=46,
                                                             beneficiario__edad_inicial__lte=50).count()
                jornadaRep['m_ar_51'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=51,
                                                             beneficiario__edad_inicial__lte=55).count()
                jornadaRep['m_ar_56'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=56,
                                                             beneficiario__edad_inicial__lte=60).count()
                jornadaRep['m_ar_61'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=61,
                                                             beneficiario__edad_inicial__lte=65).count()
                jornadaRep['m_ar_66'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=66,
                                                             beneficiario__edad_inicial__lte=70).count()
                jornadaRep['m_ar_71'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=71,
                                                             beneficiario__edad_inicial__lte=75).count()
                jornadaRep['m_ar_76'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=76,
                                                             beneficiario__edad_inicial__lte=80).count()
                jornadaRep['m_ar_81'] = m_alto_riesgo.filter(beneficiario__edad_inicial__gte=81).count()

                jornadaRep['h_br'] = h_bajo_riesgo.count()
                jornadaRep['h_mr'] = h_moderado_riesgo.count()
                jornadaRep['h_ar'] = h_alto_riesgo.count()
                jornadaRep['h_sd'] = total_hombres-jornadaRep['h_br']-jornadaRep['h_mr']-jornadaRep['h_ar']

                jornadaRep['h_br_p'] = percentage(jornadaRep['h_br'], total_hombres)
                jornadaRep['h_mr_p'] = percentage(jornadaRep['h_mr'], total_hombres)
                jornadaRep['h_ar_p'] = percentage(jornadaRep['h_ar'], total_hombres)
                jornadaRep['h_sd_p'] = percentage(jornadaRep['h_sd'], total_hombres)

                fix_percentage(jornadaRep, ["h_br_p", "h_mr_p", "h_ar_p", "h_sd_p"])

                jornadaRep['m_br'] = m_bajo_riesgo.count()
                jornadaRep['m_mr'] = m_moderado_riesgo.count()
                jornadaRep['m_ar'] = m_alto_riesgo.count()
                jornadaRep['m_sd'] = total_mujeres - jornadaRep['m_br'] - jornadaRep['m_mr'] - jornadaRep['m_ar']

                jornadaRep['m_br_p'] = percentage(jornadaRep['m_br'], total_mujeres)
                jornadaRep['m_mr_p'] = percentage(jornadaRep['m_mr'], total_mujeres)
                jornadaRep['m_ar_p'] = percentage(jornadaRep['m_ar'], total_mujeres)
                jornadaRep['m_sd_p'] = percentage(jornadaRep['m_sd'], total_mujeres)

                fix_percentage(jornadaRep, ["m_br_p", "m_mr_p", "m_ar_p", "m_sd_p"])

                # Reporte de Factor de Riesgo
                malnutrición = MalnutricionInflamacion.objects.filter(
                    beneficiario__jornada=jornadaRep['jornada'].id).values('resultado', 'beneficiario__sexo')

                jornadaRep['est_nut_a'] = malnutrición.filter(resultado=0).count()
                jornadaRep['des_nut_leve_b'] = malnutrición.filter(resultado__gte=1, resultado__lte=9).count()
                jornadaRep['des_nut_mod_c'] = malnutrición.filter(resultado__gte=10, resultado__lte=19).count()
                jornadaRep['des_nut_grave_d'] = malnutrición.filter(resultado__gte=20, resultado__lte=29).count()
                jornadaRep['des_nut_grav_e'] = malnutrición.filter(resultado__gte=30).count()
                jornadaRep['nutricion_por'] = malnutrición.count()

                if(malnutrición.count() > 0):
                    jornadaRep['p_est_nut_a'] = jornadaRep['est_nut_a']/jornadaRep['nutricion_por'] * 100
                    jornadaRep['p_des_nut_leve_b'] = jornadaRep['des_nut_leve_b']/jornadaRep['nutricion_por'] * 100
                    jornadaRep['p_des_nut_mod_c'] = jornadaRep['des_nut_mod_c']/jornadaRep['nutricion_por'] * 100
                    jornadaRep['p_des_nut_grave_d'] = jornadaRep['des_nut_grave_d']/jornadaRep['nutricion_por'] * 100
                    jornadaRep['p_des_nut_grav_e'] = jornadaRep['des_nut_grav_e']/jornadaRep['nutricion_por'] * 100

                # Reporte controlados y descontrolados

                    # Hipertensos controlados/descontrolados/sin datos

                jornadaRep["hipertension"] = jornadaRep["beneficiarios"].filter(diabetico_hipertenso=2).count()

                jornadaRep["nc_tension_hipertension"] = TamizajeNutricional.objects.filter(presion_sistolica__gte=140,
                                                                                           presion_diastolica__gte=90,
                                                                                           beneficiario__jornada=jornadaRep['jornada'].id).count()
                jornadaRep["c_tension_hipertension"] = TamizajeNutricional.objects.filter(presion_sistolica__lt=140, presion_sistolica__gt=0,
                                                                                          presion_diastolica__lt=90, presion_diastolica__gt=0,
                                                                                          beneficiario__jornada=jornadaRep['jornada'].id).count()
                jornadaRep["sd_tension"] = jornadaRep["hipertension"] - \
                    jornadaRep["nc_tension_hipertension"] - jornadaRep["c_tension_hipertension"]

                jornadaRep["t_hipertension"] = percentage(jornadaRep['c_tension_hipertension'], jornadaRep['hipertension'])
                jornadaRep["t_nhipertension"] = percentage(jornadaRep['nc_tension_hipertension'], jornadaRep['hipertension'])
                jornadaRep['t_sd_tension'] = percentage(jornadaRep['sd_tension'], jornadaRep['hipertension'])

                fix_percentage(jornadaRep, ["t_hipertension", "t_nhipertension", "t_sd_tension"])

            # Sociodemográfico
            jornadaCleanReportSocio["Total de beneficiarios"] = jornadaRep["total"]
            jornadaCleanReportSocio["# Hombres"] = jornadaRep["total_hombres"].count()
            jornadaCleanReportSocio["# Mujeres"] = jornadaRep["total_mujeres"].count()
            total_de_seg = jornadaRep["beneficiarios"].filter(de_seguimiento = True)
            jornadaCleanReportSocio["Total de segumiento"] = total_de_seg.count()
            jornadaCleanReportSocio["# Hombres de seguimiento"] = total_de_seg.filter(sexo=True).count()
            jornadaCleanReportSocio["# Mujeres de seguimiento"] = total_de_seg.filter(sexo=False).count()
            jornadaCleanReportSocio["% Hombres"] = str(jornadaRep["p_h"])+'%'
            jornadaCleanReportSocio["% Mujeres"] = str(jornadaRep["p_m"])+'%'
            jornadaCleanReportSocio["Hombres < 40"] = jornadaRep["h_40"]
            jornadaCleanReportSocio["Hombres 41-50"] = jornadaRep["h_41"]+jornadaRep["h_46"]
            jornadaCleanReportSocio["Hombres 51-60"] = jornadaRep["h_51"]+jornadaRep["h_56"]
            jornadaCleanReportSocio["Hombres 61-70"] = jornadaRep["h_61"]+jornadaRep["h_66"]
            jornadaCleanReportSocio["Hombres 71-80"] = jornadaRep["h_71"]+jornadaRep["h_76"]
            jornadaCleanReportSocio["Hombres > 40"] = jornadaRep["h_81"]
            jornadaCleanReportSocio["Mujeres < 40"] = jornadaRep["m_40"]
            jornadaCleanReportSocio["Mujeres 41-50"] = jornadaRep["m_41"]+jornadaRep["m_46"]
            jornadaCleanReportSocio["Mujeres 51-60"] = jornadaRep["m_51"]+jornadaRep["m_56"]
            jornadaCleanReportSocio["Mujeres 61-70"] = jornadaRep["m_61"]+jornadaRep["m_66"]
            jornadaCleanReportSocio["Mujeres 71-80"] = jornadaRep["m_71"]+jornadaRep["m_76"]
            jornadaCleanReportSocio["Mujeres > 40"] = jornadaRep["m_81"]

            # Diabetes hipertensión
            jornadaCleanReportDH["Total diabetes"] = jornadaRep["t_h_d"].count()+jornadaRep["t_m_d"].count()
            jornadaCleanReportDH["Total hipertensión"] = jornadaRep["t_h_h"].count()+jornadaRep["t_m_h"].count()
            jornadaCleanReportDH["Total diabetes e hipertensión"] = jornadaRep["t_h_dh"].count() + \
                jornadaRep["t_m_dh"].count()
            jornadaCleanReportDH["Hombres diabetes"] = jornadaRep["t_h_d"].count()
            jornadaCleanReportDH["Hombres hipertensión"] = jornadaRep["t_h_h"].count()
            jornadaCleanReportDH["Hombres diabetes e hipertensión"] = jornadaRep["t_h_dh"].count()
            jornadaCleanReportDH["Mujeres diabetes"] = jornadaRep["t_m_d"].count()
            jornadaCleanReportDH["Mujeres hipertensión"] = jornadaRep["t_m_h"].count()
            jornadaCleanReportDH["Mujeres diabetes e hipertensión"] = jornadaRep["t_m_dh"].count()

            # Factor de riesgo
            jornadaCleanReportFDR["Total bajo riesgo"] = bajo_riesgo.count()
            jornadaCleanReportFDR["Total moderado riesgo"] = moderado_riesgo.count()
            jornadaCleanReportFDR["Total alto riesgo"] = alto_riesgo.count()
            jornadaCleanReportFDR["Hombres bajo riesgo"] = h_bajo_riesgo.count()
            jornadaCleanReportFDR["Hombres moderado riesgo"] = h_moderado_riesgo.count()
            jornadaCleanReportFDR["Hombres alto riesgo"] = h_alto_riesgo.count()
            jornadaCleanReportFDR["Mujeres bajo riesgo"] = m_bajo_riesgo.count()
            jornadaCleanReportFDR["Mujeres moderado riesgo"] = m_moderado_riesgo.count()
            jornadaCleanReportFDR["Mujeres alto riesgo"] = m_alto_riesgo.count()

            # Estadificación
            jornadaCleanReportEstadificacion["G1"] = jornadaRep["h_G1"].count()+jornadaRep["m_G1"].count()
            jornadaCleanReportEstadificacion["G2"] = jornadaRep["h_G2"].count()+jornadaRep["m_G2"].count()
            jornadaCleanReportEstadificacion["G3a"] = jornadaRep["h_G3a"].count()+jornadaRep["m_G3a"].count()
            jornadaCleanReportEstadificacion["G3b"] = jornadaRep["h_G3b"].count()+jornadaRep["m_G3b"].count()
            jornadaCleanReportEstadificacion["G4"] = jornadaRep["h_G4"].count()+jornadaRep["m_G4"].count()
            jornadaCleanReportEstadificacion["G5"] = jornadaRep["h_G5"].count()+jornadaRep["m_G5"].count()

            jornadaCleanReportEstadificacion["Hombres G1"] = jornadaRep["h_G1"].count()
            jornadaCleanReportEstadificacion["Hombres G2"] = jornadaRep["h_G2"].count()
            jornadaCleanReportEstadificacion["Hombres G3a"] = jornadaRep["h_G3a"].count()
            jornadaCleanReportEstadificacion["Hombres G3b"] = jornadaRep["h_G3b"].count()
            jornadaCleanReportEstadificacion["Hombres G4"] = jornadaRep["h_G4"].count()
            jornadaCleanReportEstadificacion["Hombres G5"] = jornadaRep["h_G5"].count()

            jornadaCleanReportEstadificacion["Mujeres G1"] = jornadaRep["m_G1"].count()
            jornadaCleanReportEstadificacion["Mujeres G2"] = jornadaRep["m_G2"].count()
            jornadaCleanReportEstadificacion["Mujeres G3a"] = jornadaRep["m_G3a"].count()
            jornadaCleanReportEstadificacion["Mujeres G3b"] = jornadaRep["m_G3b"].count()
            jornadaCleanReportEstadificacion["Mujeres G4"] = jornadaRep["m_G4"].count()
            jornadaCleanReportEstadificacion["Mujeres G5"] = jornadaRep["m_G5"].count()

            # Malnutrición
            jornadaCleanReportMalnutricion["Estado nutricional A"] = jornadaRep['est_nut_a']
            jornadaCleanReportMalnutricion["Desnutrición leve"] = jornadaRep['des_nut_leve_b']
            jornadaCleanReportMalnutricion["Desnutrición moderada"] = jornadaRep['des_nut_mod_c']
            jornadaCleanReportMalnutricion["Desnutrición grave"] = jornadaRep['des_nut_grave_d']
            jornadaCleanReportMalnutricion["Desnutrición gravísima"] = jornadaRep['des_nut_grav_e']

            # Controlado / descontrolado
            controlados = 0
            descontrolados = 0
            d_controlados = 0
            d_descontrolados = 0
            h_controlados = 0
            h_descontrolados = 0
            dh_controlados = 0
            dh_descontrolados = 0
            sin_datos = 0
            for b in jornadaRep["beneficiarios"]:
                qs = None
                hg = None
                tn = None

                if b.diabetico_hipertenso == 1:
                    if QuimicaSanguinea.objects.filter(beneficiario=b).exists():
                        qs = QuimicaSanguinea.objects.filter(beneficiario=b).order_by('-id')[0]
                    if HemoglobinaGlucosilada.objects.filter(beneficiario=b).exists():
                        hg = HemoglobinaGlucosilada.objects.filter(beneficiario=b).order_by('-id')[0]
                    if qs is None or hg is None:
                        sin_datos += 1
                    else:
                        if qs.glucosa > 130 or hg.hemoglobina_glucosilada > 7.0:
                            descontrolados += 1
                            d_descontrolados += 1
                        else:
                            controlados += 1
                            d_controlados += 1
                elif b.diabetico_hipertenso == 2:
                    if TamizajeNutricional.objects.filter(beneficiario=b).exists():
                        tn = TamizajeNutricional.objects.filter(beneficiario=b).order_by('-id')[0]
                    if tn is None:
                        sin_datos += 1
                    else:
                        if tn.presion_sistolica/tn.presion_diastolica > (14/9):
                            descontrolados += 1
                            h_descontrolados += 1
                        else:
                            controlados += 1
                            h_controlados += 1
                elif b.diabetico_hipertenso == 3:
                    if QuimicaSanguinea.objects.filter(beneficiario=b).exists():
                        qs = QuimicaSanguinea.objects.filter(beneficiario=b).order_by('-id')[0]
                    if HemoglobinaGlucosilada.objects.filter(beneficiario=b).exists():
                        hg = HemoglobinaGlucosilada.objects.filter(beneficiario=b).order_by('-id')[0]
                    if TamizajeNutricional.objects.filter(beneficiario=b).exists():
                        tn = TamizajeNutricional.objects.filter(beneficiario=b).order_by('-id')[0]
                    if qs is None or hg is None or tn is None:
                        sin_datos += 1
                    else:
                        if qs.glucosa > 130 \
                                or hg.hemoglobina_glucosilada > 7.0 \
                                or tn.presion_sistolica/tn.presion_diastolica > (13/8):
                            descontrolados += 1
                            dh_descontrolados += 1
                        else:
                            controlados += 1
                            dh_controlados += 1
                else:
                    sin_datos += 1
            jornadaCleanReportControl["Controlados"] = controlados
            jornadaCleanReportControl["Descontrolados"] = descontrolados
            jornadaCleanReportControl["Diabéticos controlados"] = d_controlados
            jornadaCleanReportControl["Diabéticos descontrolados"] = d_descontrolados
            jornadaCleanReportControl["Hipertensos controlados"] = h_controlados
            jornadaCleanReportControl["Hipertensos descontrolados"] = h_descontrolados
            jornadaCleanReportControl["Diabéticos e hipertensos controlados"] = dh_controlados
            jornadaCleanReportControl["Diabeticos e hipertensos descontrolados"] = dh_descontrolados
            jornadaCleanReportControl["Sin información"] = sin_datos

            # Adherencia al tratamiento
            a_t_re = 0
            a_t_ne = 0
            a_t_mo = 0
            a_t_ac = 0
            a_t_ad = 0
            a_h_re = 0
            a_h_ne = 0
            a_h_mo = 0
            a_h_ac = 0
            a_h_ad = 0
            a_m_re = 0
            a_m_ne = 0
            a_m_mo = 0
            a_m_ac = 0
            a_m_ad = 0

            for b in jornadaRep["beneficiarios"]:
                if AdherenciaTratamiento.objects.filter(beneficiario=b).exists():
                    at = AdherenciaTratamiento.objects.filter(beneficiario=b).order_by('-id')[0]
                    if b.sexo:
                        if at.interpretacion == "Rechazo":
                            a_t_re += 1
                            a_h_re += 1
                        elif at.interpretacion == "Negación":
                            a_t_ne += 1
                            a_h_ne += 1
                        elif at.interpretacion == "Modificación":
                            a_t_mo += 1
                            a_h_mo += 1
                        elif at.interpretacion == "Aceptación":
                            a_t_ac += 1
                            a_h_ac += 1
                        elif at.interpretacion == "Adherencia":
                            a_t_ad += 1
                            a_h_ad += 1
                    else:
                        if at.interpretacion == "Rechazo":
                            a_t_re += 1
                            a_m_re += 1
                        elif at.interpretacion == "Negación":
                            a_t_ne += 1
                            a_m_ne += 1
                        elif at.interpretacion == "Modificación":
                            a_t_mo += 1
                            a_m_mo += 1
                        elif at.interpretacion == "Aceptación":
                            a_t_ac += 1
                            a_m_ac += 1
                        elif at.interpretacion == "Adherencia":
                            a_t_ad += 1
                            a_m_ad += 1
            jornadaCleanReportAdherencia["Total rechazo"] = a_t_re
            jornadaCleanReportAdherencia["Total negación"] = a_t_ne
            jornadaCleanReportAdherencia["Total modificación"] = a_t_mo
            jornadaCleanReportAdherencia["Total aceptación"] = a_t_ac
            jornadaCleanReportAdherencia["Total adherencia"] = a_t_ad
            jornadaCleanReportAdherencia["Hombres rechazo"] = a_h_re
            jornadaCleanReportAdherencia["Hombres negación"] = a_h_ne
            jornadaCleanReportAdherencia["Hombres modificación"] = a_h_mo
            jornadaCleanReportAdherencia["Hombres aceptación"] = a_h_ac
            jornadaCleanReportAdherencia["Hombres adherencia"] = a_h_ad
            jornadaCleanReportAdherencia["Mujeres rechazo"] = a_m_re
            jornadaCleanReportAdherencia["Mujeres negación"] = a_m_ne
            jornadaCleanReportAdherencia["Mujeres modificación"] = a_m_mo
            jornadaCleanReportAdherencia["Mujeres aceptación"] = a_m_ac
            jornadaCleanReportAdherencia["Mujeres adherencia"] = a_m_ad

            # Hamilton
            h_t_md = 0
            h_t_ds = 0
            h_t_dm = 0
            h_t_dl = 0
            h_t_sd = 0
            h_h_md = 0
            h_h_ds = 0
            h_h_dm = 0
            h_h_dl = 0
            h_h_sd = 0
            h_m_md = 0
            h_m_ds = 0
            h_m_dm = 0
            h_m_dl = 0
            h_m_sd = 0

            for b in jornadaRep["beneficiarios"]:
                if EscalaHamilton.objects.filter(beneficiario=b).exists():
                    eh = EscalaHamilton.objects.filter(beneficiario=b).order_by('-id')[0]
                    if b.sexo:
                        if eh.interpretacion == "No deprimido":
                            h_t_sd += 1
                            h_h_sd += 1
                        elif eh.interpretacion == "Depresión ligera/menor":
                            h_t_dl += 1
                            h_h_dl += 1
                        elif eh.interpretacion == "Depresión moderada":
                            h_t_dm += 1
                            h_h_dm += 1
                        elif eh.interpretacion == "Depresión severa":
                            h_t_ds += 1
                            h_h_ds += 1
                        elif eh.interpretacion == "Depresión muy severa":
                            h_t_md += 1
                            h_h_md += 1
                    else:
                        if eh.interpretacion == "No deprimido":
                            h_t_sd += 1
                            h_m_sd += 1
                        elif eh.interpretacion == "Depresión ligera/menor":
                            h_t_dl += 1
                            h_m_dl += 1
                        elif eh.interpretacion == "Depresión moderada":
                            h_t_dm += 1
                            h_m_dm += 1
                        elif eh.interpretacion == "Depresión severa":
                            h_t_ds += 1
                            h_m_ds += 1
                        elif eh.interpretacion == "Depresión muy severa":
                            h_t_md += 1
                            h_m_md += 1

            jornadaCleanReportHamilton["Total no deprimidos"] = h_t_sd
            jornadaCleanReportHamilton["Total depresión ligera/menor"] = h_t_dl
            jornadaCleanReportHamilton["Total depresión moderada"] = h_t_dm
            jornadaCleanReportHamilton["Total depresión severa"] = h_t_ds
            jornadaCleanReportHamilton["Total depresión muy severa"] = h_t_md
            jornadaCleanReportHamilton["Hombres no deprimidos"] = h_h_sd
            jornadaCleanReportHamilton["Hombres depresión ligera/menor"] = h_h_dl
            jornadaCleanReportHamilton["Hombres depresión moderada"] = h_h_dm
            jornadaCleanReportHamilton["Hombres depresión severa"] = h_h_ds
            jornadaCleanReportHamilton["Hombres depresión muy severa"] = h_h_md
            jornadaCleanReportHamilton["Mujeres no deprimidas"] = h_m_sd
            jornadaCleanReportHamilton["Mujeres depresión ligera/menor"] = h_m_dl
            jornadaCleanReportHamilton["Mujeres depresión moderada"] = h_m_dm
            jornadaCleanReportHamilton["Mujeres depresión severa"] = h_m_ds
            jornadaCleanReportHamilton["Mujeres depresión muy severa"] = h_m_md

        # Order data
        oneJornada["socio"] = jornadaCleanReportSocio
        oneJornada["dh"] = jornadaCleanReportDH
        oneJornada["fdr"] = jornadaCleanReportFDR
        oneJornada["estadificacion"] = jornadaCleanReportEstadificacion
        oneJornada["malnutricion"] = jornadaCleanReportMalnutricion
        oneJornada["control"] = jornadaCleanReportControl
        oneJornada["adherencia"] = jornadaCleanReportAdherencia
        oneJornada["hamilton"] = jornadaCleanReportHamilton

        jornadasReport.append(oneJornada)

    return jornadasReport
