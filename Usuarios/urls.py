from django.urls import path, include
from . import views
from Usuarios.views import *
from django.contrib.auth import views as auth_views

app_name = 'Usuarios'

urlpatterns = [
    path('usuarios/<int:pk>/editar', UserUpdate.as_view(), name='usuarios_editar'),
    path('usuarios/', include('django.contrib.auth.urls'))
]
