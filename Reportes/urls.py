from django.urls import path, include
from .views import *

app_name = 'Reportes'

urlpatterns = [
    path('reportes', ReportesView.as_view(), name='reportes_view'),
    path('reportes/jornada/<int:jornada>', ReportesJornadaView.as_view(), name='reportes_jornada_view'),
    path('seguimiento', ReportesSeguimientoView.as_view(), name='reportes_seguimiento_view'),
    path('seguimiento/jornada/<int:jornada>', ReportesSeguimientoJornadaView.as_view(), name='reportes_seguimiento_jornada_view'),
    path('comparar', CompareJornadaView.as_view(), name='compare_jornada_view'),
]
