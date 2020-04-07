from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


class PermissionsTestCase(TestCase):
    def setUp(self):
        self.user_can_edit = \
            User.objects.create_user(username='usercan',
                                     password='Q$#$IwZyT2j##4RpxhxN')
        self.user_cannot_edit = \
            User.objects.create_user(username='usercannot',
                                     password='G9&xco38a68nGF^XN!6Q')
        self.group_change_user = Group.objects.create(name='Modificar usuario')
        permission = Permission.objects.get(codename='change_user')
        self.group_change_user.permissions.add(permission)

        self.group_view_beneficiario = Group.objects.create(name='Ver beneficiario')
        permission = Permission.objects.get(codename='view_beneficiario')
        self.group_view_beneficiario.permissions.add(permission)

        self.user_can_edit.groups.add(self.group_change_user)

    def test_can_modify(self):
        self.client.force_login(self.user_can_edit)
        url = '/usuarios/' + str(self.user_can_edit.id) + '/editar'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(self.user_can_edit.groups.all().filter(id=self.group_view_beneficiario.id)), 0)

        response = self.client.post(url, {'groups': str(self.group_view_beneficiario.id)})

        self.assertEqual(len(self.user_can_edit.groups.all().filter(id=self.group_view_beneficiario.id)), 1)

    def test_cannot_modify(self):
        self.client.force_login(self.user_cannot_edit)
        url = '/usuarios/' + str(self.user_can_edit.id) + '/editar'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

        self.assertEqual(len(self.user_can_edit.groups.all().filter(id=self.group_change_user.id)), 1)

        response = self.client.post(url, {'groups': str(self.group_view_beneficiario.id)})

        self.assertEqual(response.status_code, 403)

        self.assertEqual(len(self.user_can_edit.groups.all().filter(id=self.group_view_beneficiario.id)), 0)
        self.assertEqual(len(self.user_can_edit.groups.all().filter(id=self.group_change_user.id)), 1)


# Pruebas para iniciar sesión
class LoginTestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_superuser(username='testuser2',
                                                  email="example@example.com",
                                                  password='1b<ISRUkw+tuK')
        self.user.save()

    def tearDown(self):
        del self.user

    def test_logged_in_wrong_user(self):
        self.client.login(username='wrong', password='1b<ISRUkw+tuK')
        response = self.client.get('/login/')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_logged_in_wrong_password(self):
        self.client.login(username='testuser2', password='wrong')
        response = self.client.get('/login/')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_logged_in_wrong_user_password(self):
        self.client.login(username='wrong', password='wrong')
        response = self.client.get('/login/')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_logged_in_displays_home(self):
        self.client.login(username='testuser2', password='1b<ISRUkw+tuK')
        response = self.client.get('/')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
