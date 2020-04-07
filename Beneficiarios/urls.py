from django.urls import path

from Beneficiarios.views import *

app_name = 'Beneficiarios'

urlpatterns = [
    path('<int:id_jornada>/beneficiarios/registrar', BeneficiariosNew.as_view(),
         name='beneficiarios_create'),
    path('beneficiarios/<int:id>/antecedentes/registrar', AntecedentesNew.as_view(),
         name='antecedentes_create'),
    path('beneficiarios', BeneficiariosList.as_view(), name='beneficiarios'),
    path('beneficiarios_json', BeneficiariosListJson.as_view(),
         name='beneficiarios_json'),
    path('beneficiarios/<int:pk>',
         BeneficiariosDetailView.as_view(), name='beneficiario'),
    path('beneficiarios/<int:pk>/expediente',
         BeneficiariosRecordView.as_view(), name='beneficiario_record'),
    path('r_est/<int:pk>',
         rEstJSON.as_view(), name='rEst'),
    path('r_tam/<int:pk>',
         rTamJSON.as_view(), name='rTam'),
    path('r_qui/<int:pk>',
         rQuiJSON.as_view(), name='rQui'),
    path('r_mic/<int:pk>',
         rMicJSON.as_view(), name='rMic'),
    path('r_hem/<int:pk>',
         rHemJSON.as_view(), name='rHem'),
    path('r_glu/<int:pk>',
         rGluJSON.as_view(), name='rGlu'),
    path('r_con/<int:pk>',
         rConJSON.as_view(), name='rCon'),
    path('r_adh/<int:pk>',
         rAdhJSON.as_view(), name='rAdh'),
    path('r_ham/<int:pk>',
         rHamJSON.as_view(), name='rHam'),
    path('r_mal/<int:pk>',
         rMalJSON.as_view(), name='rMal'),
    path('r_reg/<int:pk>',
         rRegJSON.as_view(), name='rReg'),


         
]
