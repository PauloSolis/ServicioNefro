from decimal import *
from django.contrib.contenttypes.models import ContentType
from .models import *
from Proyectos.models import *
from django.urls import reverse, reverse_lazy
import datetime
from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, Client

# Create your tests here.


class ReportesViewTest(TestCase):  # NEF-206, NEF-207, NEF-208
    def setUp(self):
        self.user = User.objects.create_user(username="userrepo", email=None, password=None)

    def test_view_without_permission(self):
        self.client.force_login(self.user)
        self.jornada = Jornada.objects.create(nombre='nombreJornada',
                                              fecha='2019-03-07',
                                              estado='estado',
                                              municipio='municipio',
                                              localidad='localidad',)
        url = '/reportes/jornada/' + str(self.jornada.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_with_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename="view_reportes"))
        self.client.force_login(self.user)
        self.jornada = Jornada.objects.create(nombre='nombreJornada',
                                              fecha='2019-03-07',
                                              estado='estado',
                                              municipio='municipio',
                                              localidad='localidad',)
        url = '/reportes/jornada/' + str(self.jornada.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_jornada_success(self):
        self.user.user_permissions.add(Permission.objects.get(codename="view_reportes"))
        self.client.force_login(self.user)
        self.jornada = Jornada.objects.create(nombre='nombreJornada',
                                              fecha='2019-03-07',
                                              estado='estado',
                                              municipio='municipio',
                                              localidad='localidad',)
        url = '/reportes/jornada/' + str(self.jornada.id)
        response = self.client.get(url)
        self.assertEqual(response.context['jornada'].id, self.jornada.id)
