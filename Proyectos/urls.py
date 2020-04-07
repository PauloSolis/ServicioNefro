from django.urls import path, include
from Proyectos.views import *

app_name = 'Proyectos'

urlpatterns = [
    path('jornadas', JornadasList.as_view(), name='jornadas'),
    path('jornadas/registrar', JornadaCreate.as_view(), name='jornadas_create'),
    path('jornadas_json', JornadasListJson.as_view(), name='jornadas_json'),
    path('jornadas/<int:pk>', JornadaDetailView.as_view(), name='jornadas_detail'),
    path('jornadas/delete/<int:pk>', JornadaDelete.as_view(), name='jornada_delete'),
]
