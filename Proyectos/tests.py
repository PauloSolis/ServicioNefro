from django.test import TestCase
from django import forms
from .models import *
from Beneficiarios.models import *
from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, Client

# Create your tests here.


class JornadaCreateTest(TestCase):  # NEF-21
    def setUp(self):
        self.user_can_create = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_create = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_create.user_permissions.add(Permission.objects.get(codename="add_jornada"))

    def test_jornada_register_success(self):
        self.client.force_login(self.user_can_create)
        data = {
            'nombre': 'Prueba piloto',
            'fecha': '2019-03-07',
            'estado': 'Qro',
            'municipio': 'Qro',
            'localidad': 'Queretarock',
        }
        response = self.client.post('/jornadas/registrar', data)
        self.assertEqual(response.status_code, 302)
        exists = Jornada.objects.filter(localidad='Queretarock').exists()
        self.assertEqual(exists, True)

    def test_jornada_register_wrong_field(self):
        self.client.force_login(self.user_can_create)
        data = {
            'nombre': 'Prueba piloto',
            'fecha': ' ',
            'estado': 'Qro',
            'municipio': 'Qro',
            'localidad': 'Queretarock',
        }
        response = self.client.post('/jornadas/registrar', data)
        exists = Jornada.objects.filter(localidad='Queretarock').exists()
        self.assertEqual(exists, False)

    def test_jornada_view_permission(self):
        self.client.force_login(self.user_can_create)
        url = '/jornadas/registrar'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_jornada_view_no_permission(self):
        self.client.force_login(self.user_cannot_create)
        url = '/jornadas/registrar'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ModifyJornada(TestCase):  # NEF-31

    def setUp(self):
        self.user_cannot_modify = User.objects.create_user(username="usercannotmodify", email=None, password=None)
        self.user_cannot_modify.user_permissions.add(Permission.objects.get(codename="view_jornada"))

        self.user_can_modify = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="view_jornada"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="change_jornada"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="add_jornada"))

        self.jornada = Jornada.objects.create(
            nombre="PruebaJornada",
            fecha='2019-03-07',
            estado="PruebaJornada",
            municipio="PruebaJornada",
            localidad="PruebaJornada",
        )

    def test_admin_modify(self):
        client = Client()
        client.force_login(self.user_can_modify)
        response = client.get('/jornadas/' + str(self.jornada.pk), follow=True)
        self.assertContains(response, "Editar")

    def test_not_admin_modify(self):
        client = Client()
        client.force_login(self.user_cannot_modify)
        response = client.get('/jornadas/' + str(self.jornada.pk), follow=True)
        self.assertNotContains(response, "Editar")


class DeleteJornadaTest(TestCase):  # NEF-23

    def setUp(self):
        self.user_cannot_modify = User.objects.create_user(username="usercannotmodify", email=None, password=None)
        self.user_cannot_modify.user_permissions.add(Permission.objects.get(codename="view_jornada"))

        self.user_can_modify = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="view_jornada"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="change_jornada"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="add_jornada"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="delete_jornada"))

        self.jornada = Jornada.objects.create(
            nombre="PruebaJornada",
            fecha='2019-03-07',
            estado="PruebaJornada",
            municipio="PruebaJornada",
            localidad="PruebaJornada",
        )

    def test_delete_jornada(self):
        client = Client()
        client.force_login(self.user_can_modify)
        jornada_exists = Jornada.objects.get(nombre="PruebaJornada")
        self.assertIsNotNone(jornada_exists)
        response = client.post('/jornadas/delete/' + str(self.jornada.pk))
        jornada_exists = Jornada.objects.filter(nombre="PruebaJornada").count()
        self.assertEqual(jornada_exists, 0)

    def test_show_button(self):
        client = Client()
        client.force_login(self.user_can_modify)
        response = client.get('/jornadas/' + str(self.jornada.pk))
        self.assertContains(response, "Borrar")

    def test_not_show_button_prohibited(self):
        client = Client()
        client.force_login(self.user_cannot_modify)
        response = client.get('/jornadas/' + str(self.jornada.pk))
        self.assertNotContains(response, "Borrar")

    def test_not_show_button_not_empty(self):
        client = Client()
        client.force_login(self.user_can_modify)
        self.beneficiario = Beneficiario.objects.create(
            apellido_paterno="a",
            apellido_materno="a",
            nombre="a",
            sexo=True,
            fecha_nacimiento=date(2010, 5, 1),
            telefono="a4344134",
            celular="a434324",
            correo="example@gamil.com",
            activo_laboralmente=True,
            nucleo_familiar='Nucleo bien bonito',
            vivienda_propia=True,
            jornada=self.jornada
        )
        self.beneficiario.save()
        response = client.get('/jornadas/' + str(self.jornada.pk))
        self.assertNotContains(response, "Borrar")
