from django.urls import path, include
from .views import *

app_name = 'Doctores'

urlpatterns = [
    path('capacitaciones', ReportesView.as_view(), name='reportes_view'),
    path('capacitaciones/evaluacion/<int:evaluacion>', ReportesEvaluacionView.as_view(), name='reportes_evaluacion_view'),
    path('evaluaciones', EvaluacionesList.as_view(), name='evaluaciones'),
    path('evaluaciones_json', EvaluacionesListJson.as_view(), name='evaluaciones_json'),
    path('evaluaciones/registrar', EvaluacionCreate.as_view(), name='evaluacion_create'),

]
