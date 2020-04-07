from decimal import *
from django.contrib.contenttypes.models import ContentType
from .models import *
from django.urls import reverse, reverse_lazy
from Beneficiarios.models import *
import datetime
from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, Client


class AddClasificacionTest(TestCase):  # NEF-95
    def setUp(self):
        self.user_can_add = User(username='userCanAdd')
        self.user_can_add.save()
        self.user_can_add.user_permissions.add(Permission.objects.get(codename="add_clasificacion"))
        self.user_can_add.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        self.user_cannot_add = User(username='userCannotAdd')
        self.user_cannot_add.save()
        self.user_cannot_add.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))

        self.beneficiario = Beneficiario.objects.create(apellido_paterno="Gonzáles", apellido_materno="Hernández",
                                                        nombre="Discrepancia", sexo=True, activo_laboralmente=False,
                                                        fecha_nacimiento=date(2010, 5, 1))

        self.qs = QuimicaSanguinea.objects.create(beneficiario=self.beneficiario,
                                                  doctor="Doc", metodo="normal", glucosa=1,
                                                  max_glucosa=1, min_glucosa=1, urea=1,
                                                  max_urea=1, min_urea=1, bun=1,
                                                  max_bun=1, min_bun=1, creatinina=1.02,
                                                  max_creatinina_h=1, min_creatinina_h=1,
                                                  max_creatinina_m=1, min_creatinina_m=1)

        self.ma = Microalbuminuria.objects.create(
            beneficiario=self.beneficiario,
            doctor='dogtor',
            fecha='2019-03-07',
            metodo='normal',
            micro_albumina=45,
            micro_albumina_min=0,
            micro_albumina_max=30,
            micro_albumina_comentario="Hola",
            creatinina=1.02,
            creatinina_min=10,
            creatinina_max=300,
            creatinina_comentario="Adios",
            relacion=10,
            relacion_normal_min=0,
            relacion_normal_max=30,
            relacion_anormal_min=30,
            relacion_anormal_max=50,
            relacion_anormal_alta_min=50,
            relacion_anormal_alta_max=300
        )

        self.clasificacion = \
            Clasificacion.objects.create(beneficiario=self.beneficiario,
                                         categoria_gfr_estimada='G2',
                                         categoria_gfr='G3a',
                                         categoria_alb='A2',
                                         gfr_estimada=15,
                                         gfr=14,
                                         albumina=200,
                                         id_qs=self.qs,
                                         id_ma=self.ma)

    def testUserCanAdd(self):
        client = Client()
        client.force_login(self.user_can_add)
        url = '/beneficiarios/' + str(self.beneficiario.id)
        url_clasificacion = url + '/clasificacion/registrar'
        self.assertEqual(len(Clasificacion.objects.all()), 2)
        first_clasificacion = Clasificacion.objects.latest('id')
        self.assertNotEqual(first_clasificacion.categoria_gfr, first_clasificacion.categoria_gfr_estimada)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<form id="clasificacion_form" method="post" action="' + url_clasificacion + '">')
        data = {
            'clasificacion_id': self.clasificacion.id,
            'clasificacion': self.clasificacion.categoria_gfr
        }
        response = client.post(url_clasificacion, data)
        self.assertEqual(len(Clasificacion.objects.all()), 3)
        response = client.get(url)
        self.assertContains(response, self.clasificacion.categoria_gfr)
        self.assertNotContains(response,
                               '<form id="clasificacion_form" method="post" action="' + url_clasificacion + '">')

    def testSelectOnlyFromOptions(self):
        client = Client()
        client.force_login(self.user_can_add)
        url = '/beneficiarios/' + str(self.beneficiario.id)
        url_clasificacion = url + '/clasificacion/registrar'
        self.assertEqual(len(Clasificacion.objects.all()), 2)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<form id="clasificacion_form" method="post" action="' + url_clasificacion + '">')
        data = {
            'clasificacion_id': self.clasificacion.id,
            'clasificacion': 'R3'
        }
        response = client.post(url_clasificacion, data)
        self.assertEqual(len(Clasificacion.objects.all()), 2)
        response = client.get(url)
        self.assertContains(response,
                            '<form id="clasificacion_form" method="post" action="' + url_clasificacion + '">')

    def testUserCannotAdd(self):
        client = Client()
        client.force_login(self.user_cannot_add)
        url = '/beneficiarios/' + str(self.beneficiario.id)
        url_clasificacion = url + '/clasificacion/registrar'
        self.assertEqual(len(Clasificacion.objects.all()), 2)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
                               '<form id="clasificacion_form" method="post" action="' + url_clasificacion + '">')
        data = {
            'clasificacion_id': self.clasificacion.id,
            'clasificacion': self.clasificacion.categoria_gfr
        }
        response = client.post(url_clasificacion, data)
        self.assertEqual(len(Clasificacion.objects.all()), 2)
        response = client.get(url)
        self.assertContains(response, self.clasificacion.categoria_gfr)
        self.assertNotContains(response,
                               '<form id="clasificacion_form" method="post" action="' + url_clasificacion + '">')


class AddHemoglobinaGlucosiladaTest(TestCase):  # NEF-70
    def setUp(self):
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
            vivienda_propia=True)
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="add_hemoglobinaglucosilada"))

    def testHemoglobinaGlucosilada(self):
        self.client.force_login(self.user_can_view)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_captura': '2019-03-07',
            'metodo': 'normal',
            'doctor': 'doctor',
            'comentario': 'bexita',
            'hemoglobina_glucosilada': 12,
            'max_no_diabetico': 12,
            'min_no_diabetico': 1,
            'max_diabetico_cont': 12,
            'min_diabetico_cont': 1,
            'max_diabetico_no_cont': 12,
            'min_diabetico_no_cont': 1,
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id) +
                                    '/hemoglobinaglucosilada/registrar', data)
        self.assertEqual(response.status_code, 302)
        hemoglobina = HemoglobinaGlucosilada.objects.filter(beneficiario=self.beneficiario.id).exists()
        self.assertEqual(hemoglobina, True)

    def test_beneficiario_no_register(self):
        self.client.force_login(self.user_cannot_view)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_captura': '2019-03-07',
            'metodo': 'normal',
            'doctor': 'doctor',
            'comentario': 'bexita',
            'hemoglobina_glucosilada': 12,
            'max_no_diabetico': 12,
            'min_no_diabetico': 1,
            'max_diabetico_cont': 12,
            'min_diabetico_cont': 1,
            'max_diabetico_no_cont': 12,
            'min_diabetico_no_cont': 1,
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id) +
                                    '/hemoglobinaglucosilada/registrar', data)
        self.assertEqual(response.status_code, 403)

    def test_max_values_exceeded(self):
        self.client.force_login(self.user_can_view)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_captura': '2019-03-07',
            'metodo': 'normal',
            'doctor': 'doctor',
            'comentario': 'bexita',
            'hemoglobina_glucosilada': 12,
            'max_no_diabetico': 12,
            'min_no_diabetico': 1,
            'max_diabetico_cont': 12,
            'min_diabetico_cont': 1,
            'max_diabetico_no_cont': 12,
            'min_diabetico_no_cont': 1000000000,
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id) +
                                    '/hemoglobinaglucosilada/registrar', data)

        hemoglobina = HemoglobinaGlucosilada.objects.filter(beneficiario=self.beneficiario.id).exists()
        self.assertEqual(hemoglobina, False)

    def test_ivalid_data_type(self):
        self.client.force_login(self.user_can_view)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_captura': '2019-03-07',
            'metodo': 'normal',
            'doctor': 'doctor',
            'comentario': 'bexita',
            'hemoglobina_glucosilada': "hola",
            'max_no_diabetico': 12,
            'min_no_diabetico': 1,
            'max_diabetico_cont': 12,
            'min_diabetico_cont': 1,
            'max_diabetico_no_cont': 12,
            'min_diabetico_no_cont': 1,
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id) +
                                    '/hemoglobinaglucosilada/registrar', data)

        hemoglobina = HemoglobinaGlucosilada.objects.filter(beneficiario=self.beneficiario.id).exists()
        self.assertEqual(hemoglobina, False)

    def test_missing_field(self):
        self.client.force_login(self.user_can_view)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_captura': '2019-03-07',
            'metodo': 'normal',
            'doctor': 'doctor',
            'comentario': 'bexita',
            'hemoglobina_glucosilada': 12,
            'max_no_diabetico': 12,
            'min_no_diabetico': 1,
            'max_diabetico_cont': 12,
            'min_diabetico_cont': 1,
            'max_diabetico_no_cont': 12,
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id) +
                                    '/hemoglobinaglucosilada/registrar', data)

        hemoglobina = HemoglobinaGlucosilada.objects.filter(beneficiario=self.beneficiario.id).exists()
        self.assertEqual(hemoglobina, False)


class ViewHemoglobinaGlucosiladaTest(TestCase):  # NEF-71
    def testViewHemoglobinaGlucosiladaWithPerms(self):
        self.client = Client()
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1),
                                                   telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito',
                                                   vivienda_propia=True)
        beneficiario.save()

        rqs = HemoglobinaGlucosilada.objects.create(
            beneficiario=beneficiario,
            metodo='normal',
            doctor='doctor',
            comentario='bexita',
            hemoglobina_glucosilada=20,
            max_no_diabetico=12,
            min_no_diabetico=1,
            max_diabetico_cont=12,
            min_diabetico_cont=1,
            max_diabetico_no_cont=12,
            min_diabetico_no_cont=1)

        content_type = ContentType.objects.get(app_label='Formularios', model='hemoglobinaglucosilada')
        permission = Permission.objects.get(codename='view_hemoglobinaglucosilada')
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        self.geditor = Group(name='Editor')
        self.geditor.save()
        self.geditor.permissions.add(permission)
        my_group = Group.objects.get(name='Editor')
        my_group.user_set.add(self.my_admin)
        my_group.save()

        loginresponse = self.client.login(username='user', password='passphrase')
        response = self.client.get('/hemoglobinaglucosilada/'+str(rqs.id))
        self.assertEqual(response.status_code, 200)

    def testViewHemoglobinaGlucosiladaWithNoPerms(self):
        self.client = Client()
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1),
                                                   telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito',
                                                   vivienda_propia=True)
        beneficiario.save()

        rqs = HemoglobinaGlucosilada.objects.create(
            beneficiario=beneficiario,
            metodo='normal',
            doctor='doctor',
            comentario='bexita',
            hemoglobina_glucosilada=20,
            max_no_diabetico=12,
            min_no_diabetico=1,
            max_diabetico_cont=12,
            min_diabetico_cont=1,
            max_diabetico_no_cont=12,
            min_diabetico_no_cont=1)
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        loginresponse = self.client.login(username='user', password='passphrase')
        response = self.client.get('/hemoglobinaglucosilada/'+str(rqs.id))
        self.assertEqual(response.status_code, 403)

    def testViewHemoglobinaGlucosiladaNoLoggedIn(self):
        self.client = Client()
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1),
                                                   telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito',
                                                   vivienda_propia=True)
        beneficiario.save()

        rqs = HemoglobinaGlucosilada.objects.create(
            beneficiario=beneficiario,
            metodo='normal',
            doctor='doctor',
            comentario='bexita',
            hemoglobina_glucosilada=20,
            max_no_diabetico=12,
            min_no_diabetico=1,
            max_diabetico_cont=12,
            min_diabetico_cont=1,
            max_diabetico_no_cont=12,
            min_diabetico_no_cont=1)
        response = self.client.get('/hemoglobinaglucosilada/'+str(rqs.id))
        self.assertEqual(response.status_code, 302)


class AddQuimicaSanguineaTest(TestCase):  # NEF-66
    def setUp(self):
        self.user_can_create = User.objects.create_user(username="usercancreate",
                                                        email=None, password=None)
        self.user_can_not_create = User.objects.create_user(username="usercantcreate",
                                                            email=None, password=None)
        self.user_can_create.user_permissions.add(Permission.objects.get(codename="add_quimicasanguinea"))
        self.user_can_create.user_permissions.add(Permission.objects.get(codename="add_beneficiario"))
        self.jornada = Jornada.objects.create(nombre="piloto",
                                              fecha="2019-03-07",
                                              localidad="Queretarock",
                                              municipio="Qrock",
                                              estado="Qro")
        self.beneficiario = Beneficiario.objects.create(fecha_registro=date(2019, 3, 3),
                                                        apellido_paterno="Pérez",
                                                        apellido_materno="Suárez",
                                                        nombre="Karla",
                                                        sexo=False,
                                                        fecha_nacimiento=date(1996, 12, 8),
                                                        telefono="1457854887",
                                                        celular="4611785774",
                                                        correo="correo@correo.com",
                                                        activo_laboralmente=True,
                                                        nucleo_familiar="Solo",
                                                        vivienda_propia=False,
                                                        escolaridad="PRI",
                                                        jornada=self.jornada)

    def test_quimica_sanguinea_create(self):
        self.client = Client()
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1), telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito', vivienda_propia=True)
        beneficiario.save()
        response = self.client.get('/formularios/register/quimicaSanguinea/1/', follow=True)
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        loginresponse = self.client.login(username='user', password='passphrase')
        if loginresponse:
            rqs = QuimicaSanguinea.objects.create(beneficiario=beneficiario, doctor="Doc", metodo="normal", glucosa=1,
                                                  max_glucosa=1, min_glucosa=1, urea=1,
                                                  max_urea=1, min_urea=1, bun=1,
                                                  max_bun=1, min_bun=1, creatinina=1,
                                                  max_creatinina_h=1, min_creatinina_h=1,
                                                  max_creatinina_m=1, min_creatinina_m=1)
            verifiedRqs = QuimicaSanguinea.objects.get(doctor="Doc")
        self.assertEqual(verifiedRqs, rqs)

    def test_quimica_sanguinea_register_success(self):
        self.client.force_login(self.user_can_create)
        data = {
            'beneficiario ': self.beneficiario.id,
            'fecha': '2019-03-03',
            'doctor': "Doc",
            'metodo': "normal",
            'glucosa': 1,
            'max_glucosa': 1,
            'min_glucosa': 1,
            'comentario_glucosa': "Juan",
            'urea': 1,
            'max_urea': 1,
            'min_urea': 1,
            'comentario_urea': "sdaf",
            'bun': 1,
            'max_bun': 1,
            'min_bun': 1,
            'comentario_bun': "dsfasdfa",
            'creatinina': 1,
            'max_creatinina_h': 1,
            'min_creatinina_h': 1,
            'max_creatinina_m': 1,
            'min_creatinina_m': 1,
            'comentario_creatinina': "Sdffs",
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id)+'/quimicasanguinea/registrar', data)
        self.assertEqual(response.status_code, 302)
        exists = QuimicaSanguinea.objects.filter(doctor='Doc').exists()
        self.assertEqual(exists, True)

    def testAddQuimicaSanguineaWrongValues(self):
        self.client = Client()
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1),
                                                   telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito', vivienda_propia=True)
        beneficiario.save()
        response = self.client.get('/formularios/register/quimicaSanguinea/1/', follow=True)
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        loginresponse = self.client.login(username='user', password='passphrase')
        if loginresponse:
            try:
                rqs = QuimicaSanguinea.objects.create(beneficiario=beneficiario, doctor="Doc", metodo="normal",
                                                      glucosa=1,
                                                      max_glucosa=1, min_glucosa=1, urea=1, max_urea=1,
                                                      min_urea=1, bun=1,
                                                      max_bun=1, min_bun=1, creatinina=1,
                                                      max_creatinina_h=1, min_creatinina_h=1,
                                                      max_creatinina_m=1, min_creatinina_m=1256265466.06549843)

            except Exception:
                pass

    def testAddQuimicaSanguineaNegativeValues(self):
        self.client = Client()
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1),
                                                   telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito', vivienda_propia=True)
        beneficiario.save()
        response = self.client.get('/formularios/register/quimicaSanguinea/1/', follow=True)
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        loginresponse = self.client.login(username='user', password='passphrase')
        if loginresponse:
            try:
                rqs = QuimicaSanguinea.objects.create(beneficiario=beneficiario, doctor="Doc", metodo="normal",
                                                      glucosa=1,
                                                      max_glucosa=1, min_glucosa=1, urea=1, max_urea=1,
                                                      min_urea=1, bun=1,
                                                      max_bun=1, min_bun=1, creatinina=1,
                                                      max_creatinina_h=1, min_creatinina_h=1,
                                                      max_creatinina_m=1, min_creatinina_m=-1)
            except Exception:
                pass

    def testAddQuimicaSanguineaData(self):
        self.client = Client()
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1),
                                                   telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito', vivienda_propia=True)
        beneficiario.save()
        response = self.client.get('/formularios/register/quimicaSanguinea/1/', follow=True)
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        loginresponse = self.client.login(username='user', password='passphrase')
        if loginresponse:
            try:
                rqs = QuimicaSanguinea.objects.create(beneficiario=beneficiario, doctor="Doc", metodo="normal",
                                                      glucosa=1,
                                                      max_glucosa="Vamos bien", min_glucosa=1,
                                                      urea=1, max_urea=1, min_urea=1, bun=1,
                                                      max_bun=1, min_bun=1, creatinina=1,
                                                      max_creatinina_h=1, min_creatinina_h=1,
                                                      max_creatinina_m=1, min_creatinina_m=3)
            except Exception:
                pass

    def testAddQuimicaSanguineaMissingField(self):
        self.client = Client()
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1),
                                                   telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito', vivienda_propia=True)
        beneficiario.save()
        response = self.client.get('/formularios/register/quimicaSanguinea/1/', follow=True)
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        loginresponse = self.client.login(username='user', password='passphrase')
        if loginresponse:
            try:
                rqs = QuimicaSanguinea.objects.create(beneficiario=beneficiario, doctor="Doc", metodo="normal",
                                                      glucosa=1,
                                                      max_glucosa="Vamos bien", min_glucosa=1, urea=1, max_urea=1,
                                                      min_urea=1, bun=1,
                                                      max_bun=1, min_bun=1, creatinina=1, max_creatinina_h=1,
                                                      min_creatinina_h=1,
                                                      max_creatinina_m=1, )
            except Exception:
                pass

    def test_user_can_create(self):
        self.client.force_login(self.user_can_create)
        url = '/beneficiarios/'+str(self.beneficiario.id)+'/quimicasanguinea/registrar'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_not_create(self):
        self.client.force_login(self.user_can_not_create)
        url = '/beneficiarios/'+str(self.beneficiario.id)+'/quimicasanguinea/registrar'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ViewQuimicaSanguineaTest(TestCase):  # NEF-67

    def testViewQuimicaSanguineaNotUrl(self):
        self.client = Client()
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.create(apellido_paterno="a", apellido_materno="a", nombre="a",
                                                   sexo=True, fecha_nacimiento=date(2010, 5, 1), telefono="a4344134",
                                                   celular="a434324", correo="example@gamil.com",
                                                   activo_laboralmente=True,
                                                   nucleo_familiar='Nucleo bien bonito', vivienda_propia=True)
        beneficiario.save()
        self.client = Client()
        response = self.client.get('/formularios/quimicaSanguinea/1/view/4')
        self.assertEqual(response.status_code, 404)


class DiagnosticoAutomaticoTest(TestCase):  # NEF-94
    def setUp(self):
        self.beneficiario = Beneficiario.objects.create(
            apellido_paterno="a",
            apellido_materno="a",
            nombre="a",
            sexo=True,
            fecha_nacimiento=date(1990, 1, 1),
            telefono="a4344134",
            celular="a434324",
            correo="example@gamil.com",
            activo_laboralmente=True,
            nucleo_familiar='Nucleo bien bonito',
            vivienda_propia=True)
        self.rqs = QuimicaSanguinea.objects.create(beneficiario=self.beneficiario,
                                                   doctor="Doc", metodo="normal", glucosa=1,
                                                   max_glucosa=1, min_glucosa=1, urea=1,
                                                   max_urea=1, min_urea=1, bun=1,
                                                   max_bun=1, min_bun=1, creatinina=1.02,
                                                   max_creatinina_h=1, min_creatinina_h=1,
                                                   max_creatinina_m=1, min_creatinina_m=1)

        self.user = \
            User.objects.create_user(username='usercan',
                                     password='Q$#$IwZyT2j##4RpxhxN')
        self.group_add_microalbuminuria = Group.objects.create(name='Agregar Micro')
        permission = Permission.objects.get(codename='add_microalbuminuria')
        self.group_add_microalbuminuria.permissions.add(permission)
        self.user.groups.add(self.group_add_microalbuminuria)
        self.client.force_login(self.user)

    def test_add_clasification(self):
        data = {
            'beneficiario': self.beneficiario.id,
            'doctor': 'dogtor',
            'fecha': '2019-03-07',
            'metodo': 'normal',
            'micro_albumina': 45,
            'micro_albumina_min': 0,
            'micro_albumina_max': 30,
            'micro_albumina_comentario': "Hola",
            'creatinina': 1.02,
            'creatinina_min': 10,
            'creatinina_max': 300,
            'creatinina_comentario': "Adios",
            'relacion': 10,
            'relacion_normal_min': 0,
            'relacion_normal_max': 30,
            'relacion_anormal_min': 30,
            'relacion_anormal_max': 50,
            'relacion_anormal_alta_min': 50,
            'relacion_anormal_alta_max': 300
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id)+'/microalbuminuria/registrar', data)
        self.clasificacion = Clasificacion.objects.latest("id")
        self.microalbuminuria = Microalbuminuria.objects.latest("id")
        self.assertEqual(self.clasificacion.id_qs.id, self.rqs.id)
        self.assertEqual(self.clasificacion.id_ma.id, self.microalbuminuria.id)

    def test_GFR_expected(self):
        data = {
            'beneficiario': self.beneficiario.id,
            'doctor': 'dogtor',
            'fecha': '2019-03-07',
            'metodo': 'normal',
            'micro_albumina': 45,
            'micro_albumina_min': 0,
            'micro_albumina_max': 30,
            'micro_albumina_comentario': "Hola",
            'creatinina': 1.02,
            'creatinina_min': 10,
            'creatinina_max': 300,
            'creatinina_comentario': "Adios",
            'relacion': 10,
            'relacion_normal_min': 0,
            'relacion_normal_max': 30,
            'relacion_anormal_min': 30,
            'relacion_anormal_max': 50,
            'relacion_anormal_alta_min': 50,
            'relacion_anormal_alta_max': 300
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id)+'/microalbuminuria/registrar', data)
        self.clasificacion = Clasificacion.objects.latest("id")
        self.microalbuminuria = Microalbuminuria.objects.latest("id")
        expected_GFR_clasification = 'G1'
        expected_GFR_estimated_clasification = 'G2'
        expected_AM_clasification = 'A2'
        self.assertEqual(expected_GFR_estimated_clasification, self.clasificacion.categoria_gfr_estimada)
        self.assertEqual(expected_GFR_clasification, self.clasificacion.categoria_gfr)
        self.assertEqual(expected_AM_clasification, self.clasificacion.categoria_alb)
        user = User.objects.create_superuser('user', 'user@testuser.com', 'passphrase')
        user.save()


class GlucosaCapilarTest(TestCase):  # NEF-80 NEF-81

    def setUp(self):
        beneficiario = Beneficiario.objects.create(
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
            vivienda_propia=True)

        beneficiario.save()

        user = User.objects.create_superuser('user', 'user@testuser.com', 'passphrase')
        user.save()

    def testGlucosaCapilar_success(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'doctor': 'dogtor',
                'fecha': '2019-03-07',
                'metodo': 'normal',
                'comentario': 'bexita',
                'glucosa': 10,
                'min': 1,
                'max': 12
            }
            response = self.client.post('/beneficiarios/1/glucosacapilar/registrar', data)
            glucosaa_capilar = GlucosaCapilar.objects.get(doctor="dogtor")

        self.assertTrue(glucosaa_capilar)

    def testGlucosaCapilar_success_right_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'doctor': 'dogtor',
                'fecha': '2019-03-07',
                'metodo': 'normal',
                'comentario': 'bexita',
                'glucosa': 10,
                'min': 1,
                'max': 12
            }
            response = self.client.post('/beneficiarios/1/glucosacapilar/registrar', data)
            glucosaCapilar = GlucosaCapilar.objects.get(doctor="dogtor")

        self.assertTrue(glucosaCapilar)

        self.assertEqual(glucosaCapilar.beneficiario, beneficiario)
        self.assertEqual(glucosaCapilar.doctor, 'dogtor')
        self.assertEqual(glucosaCapilar.fecha,  datetime.date(2019, 3, 7))
        self.assertEqual(glucosaCapilar.metodo, 'normal')
        self.assertEqual(glucosaCapilar.comentario, 'bexita')
        self.assertEqual(glucosaCapilar.glucosa, 10)
        self.assertEqual(glucosaCapilar.min, 1)
        self.assertEqual(glucosaCapilar.max, 12)

    def testGlucosaCapilar_missing_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'doctor': 'dogtor',
                'metodo': 'normal',
                'min': 1,
                'max': 12
            }
            response = self.client.post('/beneficiarios/1/glucosacapilar/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testGlucosaCapilar_invalid_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'doctor': 'dogtor',
                'fecha':  '2019-03-07',
                'metodo': 'normal',
                'comentario': 'bexita',
                'glucosa': 'jamón',
                'min': 1,
                'max': 100000000000000000
            }
            response = self.client.post('/beneficiarios/1/glucosacapilar/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testGlucosaCapilar_unexisting_beneficiary(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')

        response = self.client.get('/beneficiarios/100/glucosacapilar/registrar', follow=True)

        self.assertEqual(response.status_code, 404)

    def testGlucosaCapilar_no_permission(self):
        user = User.objects.create_user('user_no_permission', 'user@testuser.com', 'password')
        user.save()
        loginresponse = self.client.login(username='user_no_permission',
                                          password='password')

        response = self.client.get('/beneficiarios/1/glucosacapilar/registrar', follow=True)

        self.assertEqual(response.status_code, 403)

    def testGlucosaCapilar_view(self):
        beneficiario = Beneficiario.objects.get(nombre="a")
        glucosacapilar = GlucosaCapilar.objects.create(
            beneficiario=beneficiario,
            doctor='marrano',
            fecha='2017-03-07',
            metodo='ansioso',
            comentario='mamamamarrano',
            glucosa=7,
            min=3,
            max=20,
        )
        glucosacapilar.save()

        loginresponse = self.client.login(username='user',
                                          password='passphrase')

        response = self.client.get('/glucosacapilar/' + str(glucosacapilar.id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Formularios/glucosacapilar_view.html')

    def testGlucosaCapilar_view_no_permission(self):
        user = User.objects.create_user('user_no_permission', 'user@testuser.com', 'password')
        user.save()
        loginresponse = self.client.login(username='user_no_permission',
                                          password='password')

        response = self.client.get('/glucosacapilar/1', follow=True)

        self.assertEqual(response.status_code, 403)


class TamizajeNutricionalTest(TestCase):  # NEF-62

    def setUp(self):
        beneficiario = Beneficiario.objects.create(
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
            vivienda_propia=True)
        beneficiario.save()

        user = User.objects.create_superuser('user', 'user@testuser.com', 'passphrase')
        user.save()

    def testTamizaje_success(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'presion_sistolica': 120,
                'presion_diastolica': 40,
                'peso': 68,
                'talla': 1.65,
                'circunferencia_brazo': 40,
                'pliegue_bicipital': 1,
                'pliegue_tricipital': 1,
            }
            response = self.client.post('/beneficiarios/1/tamizajenutricional/registrar', data)
            tamizaje_nutricional = TamizajeNutricional.objects.get(peso=68)

        self.assertTrue(tamizaje_nutricional)

    def testTamizaje_success_right_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'presion_sistolica': 120,
                'presion_diastolica': 40,
                'peso': 68,
                'talla': 1.65,
                'circunferencia_brazo': 40,
                'pliegue_bicipital': 1,
                'pliegue_tricipital': 1,
            }
            response = self.client.post('/beneficiarios/1/tamizajenutricional/registrar', data)
            tamizajeNutricional = TamizajeNutricional.objects.get(peso=68)

        self.assertTrue(tamizajeNutricional)

        self.assertEqual(tamizajeNutricional.beneficiario, beneficiario)
        self.assertEqual(tamizajeNutricional.fecha, datetime.date(2019, 3, 7))
        self.assertEqual(tamizajeNutricional.presion_sistolica, 120)
        self.assertEqual(tamizajeNutricional.presion_diastolica, 40)
        self.assertEqual(tamizajeNutricional.peso, 68)
        self.assertEqual(tamizajeNutricional.talla, Decimal('1.65'))
        self.assertEqual(tamizajeNutricional.circunferencia_brazo, 40)
        self.assertEqual(tamizajeNutricional.pliegue_bicipital, 1)
        self.assertEqual(tamizajeNutricional.pliegue_tricipital, 1)
        self.assertEqual(tamizajeNutricional.imc, Decimal('24.977'))

    def testTamizaje_missing_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'presion_sistolica': 120,
                'presion_diastolica': 40,
                'peso': 68,
                'talla': 1.65,
                'circunferencia_brazo': 40,
                'pliegue_bicipital': 1,
                'pliegue_tricipital': 1,
            }
            response = self.client.post('/beneficiarios/1/tamizajenutricional/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testTamizaje_invalid_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': 68,
                'presion_sistolica': 120,
                'presion_diastolica': 40,
                'peso': 68,
                'talla': 1.65,
                'circunferencia_brazo': 40,
                'pliegue_bicipital': 1,
                'pliegue_tricipital': 1,
            }
            response = self.client.post('/beneficiarios/1/tamizajenutricional/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testTamizaje_unexisting_beneficiary(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')

        response = self.client.get('/beneficiarios/100/tamizajenutricional/registrar', follow=True)

        self.assertEqual(response.status_code, 404)

    def testTamizaje_no_permission(self):
        user = User.objects.create_user('user_no_permission', 'user@testuser.com', 'password')
        user.save()
        loginresponse = self.client.login(username='user_no_permission',
                                          password='password')

        response = self.client.get('/beneficiarios/1/tamizajenutricional/registrar', follow=True)

        self.assertEqual(response.status_code, 403)


class MalNutricionInflamacionTest(TestCase):  # NEF-50

    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()

        tamizaje = TamizajeNutricional.objects.create(
            beneficiario=self.beneficiario,
            fecha="2019-03-07",
            presion_sistolica=120,
            presion_diastolica=40,
            peso=68,
            talla=1.65,
            circunferencia_brazo=40,
            pliegue_bicipital=1,
            pliegue_tricipital=1,
        )
        tamizaje.save()

        user = User.objects.create_superuser('user', 'user@testuser.com', 'passphrase')
        user.save()

    def testMalNutricion_success(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")
        tamizaje = TamizajeNutricional.objects.get(pliegue_bicipital=1)

        if loginresponse:
            data = {
                'beneficiario': self.beneficiario.id,
                'fecha': '2019-03-07',
                'porcentaje_perdida_peso': 1,
                'perdida_peso': 2,
                'peso': tamizaje.peso,
                'talla': tamizaje.talla,
                'imc_valor': tamizaje.imc,
                'imc_puntos': 4,
                'ingesta_alimentaria': 4,
                'gastrointestinales': 3,
                'incapacidad': 1,
                'comorbilidad': 4,
                'grasa_subcutanea': 1,
                'perdida_muscular': 1,
                'edema': 2,
                'fijacion_hierro': 1,
                'albumina': 2,
            }
            malnutricion_inflamacion = len(MalnutricionInflamacion.objects.all())
            response = \
                self.client.post('/beneficiarios/'
                                 + str(self.beneficiario.id) + '/malnutricioninflamacion/registrar', data)
            malnutricion_inflamacion_after = len(MalnutricionInflamacion.objects.all())
            self.assertGreater(malnutricion_inflamacion_after, malnutricion_inflamacion)
        self.assertEqual(response.status_code, 302)

    def testMalNutricion_missing_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': self.beneficiario.id,
                'fecha': '2019-03-07',
                'porcentaje_perdida_peso': 1,
                'comorbilidad': 4,
                'grasa_subcutanea': 1,
                'perdida_muscular': 1,
                'edema': 2,
                'fijacion_hierro': 1,
                'albumina': 2,
            }
            response = \
                self.client.post('/beneficiarios/'
                                 + str(self.beneficiario.id)+'/malnutricioninflamacion/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testMalNutricion_invalid_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")
        tamizaje = TamizajeNutricional.objects.get(pliegue_bicipital=1)

        if loginresponse:
            data = {
                'beneficiario': self.beneficiario.id,
                'fecha': '2019-03-07',
                'porcentaje_perdida_peso': 1,
                'perdida_peso': 2,
                'peso': tamizaje.peso,
                'talla': tamizaje.talla,
                'imc_valor': tamizaje.imc,
                'imc_puntos': 400,
                'ingesta_alimentaria': 4,
                'gastrointestinales': 3,
                'incapacidad': -1,
                'comorbilidad': 4,
                'grasa_subcutanea': 1,
                'perdida_muscular': -1,
                'edema': 2,
                'fijacion_hierro': 1,
                'albumina': 2,
            }
            response = \
                self.client.post('/beneficiarios/'
                                 + str(self.beneficiario.id) + '/malnutricioninflamacion/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testMalNutricion_no_permission(self):
        user = User.objects.create_user('user_no_permission', 'user@testuser.com', 'password')
        user.save()
        loginresponse = self.client.login(username='user_no_permission',
                                          password='password')

        response = \
            self.client.get('/beneficiarios/'
                            + str(self.beneficiario.id) + '/malnutricioninflamacion/registrar', follow=True)

        self.assertEqual(response.status_code, 403)


class AdherenciaTratamientoTest(TestCase):  # NEF-58

    def setUp(self):
        beneficiario = Beneficiario.objects.create(
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
            vivienda_propia=True)
        beneficiario.save()

        user = User.objects.create_superuser('user', 'user@testuser.com', 'passphrase')
        user.save()

    def testAdherenciaTraramiento_success(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'p1': 5,
                'p2': 2,
                'p3': 3,
                'p3': 1,
                'p4': 2,
                'p5': 1,
                'p6': 1,
                'p7': 1,
                'p8': 3,
                'p9': 2,
                'p10': 5,
                'p11': 'Hola soy Jacinto',
                'p12': 'Me caes mal',
                'p13': 'ASdfasdfasdf',
                'p14': 2,
                'p14_comentario': 'Saque 2',
                'p15': 1,
                'p15_comentario': 'El awa moja',
                'p16': 4,
                'p16_comentario': 'Puto el que lo lea',
                'p17': 2,
                'p17_comentario': 'F',
                'observaciones': 'Solo reacciones sad :('
            }
            response = self.client.post('/beneficiarios/1/adherenciatratamiento/registrar', data)
            adherencia_tratamiento = AdherenciaTratamiento.objects.get(p1=5)

        self.assertTrue(adherencia_tratamiento)

    def testAdherenciaTraramiento_view(self):  # NEF-59
        loginresponse = self.client.login(username='user', password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'p1': 5,
                'p2': 2,
                'p3': 3,
                'p3': 1,
                'p4': 2,
                'p5': 1,
                'p6': 1,
                'p7': 1,
                'p8': 3,
                'p9': 2,
                'p10': 5,
                'p11': 'Hola soy Jacinto',
                'p12': 'Me caes mal',
                'p13': 'ASdfasdfasdf',
                'p14': 2,
                'p14_comentario': 'Saque 2',
                'p15': 1,
                'p15_comentario': 'El awa moja',
                'p16': 4,
                'p16_comentario': 'Puto el que lo lea',
                'p17': 2,
                'p17_comentario': 'F',
                'observaciones': 'Solo reacciones sad :('
            }
            response = self.client.post('/beneficiarios/1/adherenciatratamiento/registrar', data)
            adherencia_tratamiento = AdherenciaTratamiento.objects.get(observaciones='Solo reacciones sad :(')
            response = self.client.get('/adherenciatratamiento/'+str(adherencia_tratamiento.id))
            self.assertEqual(response.status_code, 200)

    def testAdherenciaTraramiento_right_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'p1': 5,
                'p2': 2,
                'p3': 3,
                'p4': 2,
                'p5': 1,
                'p6': 1,
                'p7': 1,
                'p8': 3,
                'p9': 2,
                'p10': 5,
                'p11': 'Hola soy Jacinto',
                'p12': 'Me caes mal',
                'p13': 'ASdfasdfasdf',
                'p14': 2,
                'p14_comentario': 'Saque 2',
                'p15': 1,
                'p15_comentario': 'El awa moja',
                'p16': 4,
                'p16_comentario': 'Puto el que lo lea',
                'p17': 2,
                'p17_comentario': 'F',
                'observaciones': 'Solo reacciones sad :('
            }
            response = self.client.post('/beneficiarios/1/adherenciatratamiento/registrar', data)
            adherencia_tratamiento = AdherenciaTratamiento.objects.get(p1=5)

        self.assertEqual(adherencia_tratamiento.beneficiario, beneficiario)
        self.assertEqual(adherencia_tratamiento.fecha, datetime.date(2019, 3, 7))
        self.assertEqual(adherencia_tratamiento.p1, 5)
        self.assertEqual(adherencia_tratamiento.p2, 2)
        self.assertEqual(adherencia_tratamiento.p3, 3)
        self.assertEqual(adherencia_tratamiento.p4, 2)
        self.assertEqual(adherencia_tratamiento.p5, 1)
        self.assertEqual(adherencia_tratamiento.p6, 1)
        self.assertEqual(adherencia_tratamiento.p7, 1)
        self.assertEqual(adherencia_tratamiento.p8, 3)
        self.assertEqual(adherencia_tratamiento.p9, 2)
        self.assertEqual(adherencia_tratamiento.p10, 5)
        self.assertEqual(adherencia_tratamiento.p11, 'Hola soy Jacinto')
        self.assertEqual(adherencia_tratamiento.p12, 'Me caes mal')
        self.assertEqual(adherencia_tratamiento.p13, 'ASdfasdfasdf')
        self.assertEqual(adherencia_tratamiento.p14, 2)
        self.assertEqual(adherencia_tratamiento.p14_comentario, 'Saque 2')
        self.assertEqual(adherencia_tratamiento.p15, 1)
        self.assertEqual(adherencia_tratamiento.p15_comentario, 'El awa moja')
        self.assertEqual(adherencia_tratamiento.p16, 4)
        self.assertEqual(adherencia_tratamiento.p16_comentario, 'Puto el que lo lea')
        self.assertEqual(adherencia_tratamiento.p17, 2)
        self.assertEqual(adherencia_tratamiento.p17_comentario, 'F')
        self.assertEqual(adherencia_tratamiento.observaciones, 'Solo reacciones sad :(')

    def testAdherenciaTraramiento_missing_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'p1': 5,
                'p2': 2,
                'p3': 3,
                'p4': 2,
                'p5': 1,
                'p6': 1,
                'p7': 1,
                'p8': 3,
                'p9': 2,
                'p10': 5,
                'p16': 4,
                'p17': 2,
            }
            response = self.client.post('/beneficiarios/1/adherenciatratamiento/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testAdherenciaTratamiento_invalid_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'p1': 5,
                'p2': 2,
                'p3': 'Hola',
                'p4': 2,
                'p5': 1,
                'p6': 1,
                'p7': 'sadfasdf',
                'p8': 3,
                'p9': 2,
                'p10': 5,
                'p11': 'Hola soy Jacinto',
                'p12': 'Me caes mal',
                'p13': 'ASdfasdfasdf',
                'p14': 2,
                'p14_comentario': 'Saque 2',
                'p15': 1,
                'p15_comentario': 'El awa moja',
                'p16': 4,
                'p16_comentario': 'Puto el que lo lea',
                'p17': 2,
                'p17_comentario': 'F',
                'observaciones': 'Solo reacciones sad :('
            }
            response = \
                self.client.post('/beneficiarios/'
                                 + str(beneficiario.id) + '/adherenciatratamiento/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testAdherenciaTratamiento_no_permission(self):
        user = User.objects.create_user('user_no_permission', 'user@testuser.com', 'password')
        user.save()
        loginresponse = self.client.login(username='user_no_permission',
                                          password='password')

        beneficiario = Beneficiario.objects.get(apellido_paterno="a")
        response = \
            self.client.get('/beneficiarios/'
                            + str(beneficiario.id) + '/adherenciatratamiento/registrar', follow=True)

        self.assertEqual(response.status_code, 403)

    def testAdherenciaTraramiento_view(self):  # NEF-59
        loginresponse = self.client.login(username='user', password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'p1': 5,
                'p2': 2,
                'p3': 3,
                'p3': 1,
                'p4': 2,
                'p5': 1,
                'p6': 1,
                'p7': 1,
                'p8': 3,
                'p9': 2,
                'p10': 5,
                'p11': 'Hola soy Jacinto',
                'p12': 'Me caes mal',
                'p13': 'ASdfasdfasdf',
                'p14': 2,
                'p14_comentario': 'Saque 2',
                'p15': 1,
                'p15_comentario': 'El awa moja',
                'p16': 4,
                'p16_comentario': 'Puto el que lo lea',
                'p17': 2,
                'p17_comentario': 'F',
                'observaciones': 'Solo reacciones sad :('
            }
            response = self.client.post('/beneficiarios/1/adherenciatratamiento/registrar', data)
            adherencia_tratamiento = AdherenciaTratamiento.objects.get(observaciones='Solo reacciones sad :(')
            response = self.client.get('/adherenciatratamiento/'+str(adherencia_tratamiento.id))
            self.assertEqual(response.status_code, 200)


class FactorDeRiesgoTest(TestCase):  # NEF-30
    def setUp(self):
        beneficiario = Beneficiario.objects.create(
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
            vivienda_propia=True)
        beneficiario.save()
        content_type = ContentType.objects.get(app_label='Formularios', model='factorderiesgo')
        permission = Permission.objects.get(codename='add_factorderiesgo')
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('passphrase')
        self.my_admin.save()
        self.geditor = Group(name='Editor')
        self.geditor.save()
        self.geditor.permissions.add(permission)
        my_group = Group.objects.get(name='Editor')
        my_group.user_set.add(self.my_admin)
        my_group.save()

    def testFactorDeRiesgo_success(self):
        loginresponse = self.client.login(username='user', password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'p_1': 3,
                'p_1_cual': 'no se',
                'p_2': 3,
                'p_2_2': 4,
                'p_3': 3,
                'p_3_2': 4,
                'p_4': 3,
                'p_5': 2,
                'p_6': 2,
                'p_7': 2,
                'p_8': 2,
                'p_8_2': 3,
                'p_9': 2,
                'p_10': 2,
                'p_11': 2,
                'p_12': 2,
                'comentario': 'Nada de nada',
            }
            response = self.client.post('/beneficiarios/1/factorderiesgo/registrar', data)
            factor_de_riesgo = FactorDeRiesgo.objects.get(comentario='Nada de nada')
            self.assertEqual(response.status_code, 302)
            self.assertTrue(factor_de_riesgo)
            self.assertEqual(factor_de_riesgo.resultado, 39)
            self.assertEqual(factor_de_riesgo.beneficiario.id, beneficiario.id)

    def testFactorDeRiesgo_view(self):  # NEF-154
        loginresponse = self.client.login(username='user', password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")
        # permission to view the FactorDeRiesgo
        permission = Permission.objects.get(codename='view_factorderiesgo')
        self.geditor.permissions.add(permission)
        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'p_1': 3,
                'p_1_cual': 'no se',
                'p_2': 3,
                'p_2_2': 4,
                'p_3': 3,
                'p_3_2': 4,
                'p_4': 3,
                'p_5': 2,
                'p_6': 2,
                'p_7': 2,
                'p_8': 2,
                'p_8_2': 3,
                'p_9': 2,
                'p_10': 2,
                'p_11': 2,
                'p_12': 2,
                'comentario': 'Nada de nada',
            }
            response = self.client.post('/beneficiarios/1/factorderiesgo/registrar', data)
            factor_de_riesgo = FactorDeRiesgo.objects.get(comentario='Nada de nada')
            response = self.client.get('/factorderiesgo/'+str(factor_de_riesgo.id))
            self.assertEqual(response.status_code, 200)

        def testFactorDeRiesgo_view_nopermissions(self):  # NEF-154
            loginresponse = self.client.login(username='user', password='passphrase')
            beneficiario = Beneficiario.objects.get(nombre="a")

            if loginresponse:
                data = {
                    'beneficiario': beneficiario.id,
                    'fecha': '2019-03-07',
                    'p_1': 3,
                    'p_1_cual': 'no se',
                    'p_2': 3,
                    'p_2_2': 4,
                    'p_3': 3,
                    'p_3_2': 4,
                    'p_4': 3,
                    'p_5': 2,
                    'p_6': 2,
                    'p_7': 2,
                    'p_8': 2,
                    'p_8_2': 3,
                    'p_9': 2,
                    'p_10': 2,
                    'p_11': 2,
                    'p_12': 2,
                    'comentario': 'Nada de nada',
                }
                response = self.client.post('/beneficiarios/1/factorderiesgo/registrar', data)
                factor_de_riesgo = FactorDeRiesgo.objects.get(comentario='Nada de nada')
                response = self.client.get('/factorderiesgo/'+str(factor_de_riesgo.id))
                self.assertEqual(response.status_code, 403)


class AddMicroalbuminuriaTest(TestCase):

    def setUp(self):
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_microalbuminuria"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="add_microalbuminuria"))

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
            vivienda_propia=True)

        user = User.objects.create_superuser('user', 'user@testuser.com', 'passphrase')
        user.save()

    def testMicroalbuminuria_success(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'doctor': 'dogtor',
                'fecha': '2019-03-07',
                'metodo': 'normal',
                'micro_albumina': 5,
                'micro_albumina_min': 0,
                'micro_albumina_max': 30,
                'micro_albumina_comentario': "Hola",
                'creatinina': 80,
                'creatinina_min': 10,
                'creatinina_max': 300,
                'creatinina_comentario': "Adios",
                'relacion': 10,
                'relacion_normal_min': 0,
                'relacion_normal_max': 30,
                'relacion_anormal_min': 30,
                'relacion_anormal_max': 50,
                'relacion_anormal_alta_min': 50,
                'relacion_anormal_alta_max': 300
            }
            response = self.client.post('/beneficiarios/1/microalbuminuria/registrar', data)
            glucosaa_capilar = Microalbuminuria.objects.get(doctor="dogtor")

        self.assertTrue(glucosaa_capilar)

    def testMicroalbuminuria_success_right_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'doctor': 'dogtor',
                'fecha': '2019-03-07',
                'metodo': 'normal',
                'micro_albumina': 5,
                'micro_albumina_min': 0,
                'micro_albumina_max': 30,
                'micro_albumina_comentario': "Hola",
                'creatinina': 80,
                'creatinina_min': 10,
                'creatinina_max': 300,
                'creatinina_comentario': "Adios",
                'relacion': 10,
                'relacion_normal_min': 0,
                'relacion_normal_max': 30,
                'relacion_anormal_min': 30,
                'relacion_anormal_max': 50,
                'relacion_anormal_alta_min': 50,
                'relacion_anormal_alta_max': 300
            }
            response = self.client.post('/beneficiarios/1/microalbuminuria/registrar', data)
            microalbuminuria = Microalbuminuria.objects.get(doctor="dogtor")

        self.assertTrue(microalbuminuria)

        self.assertEqual(microalbuminuria.beneficiario, beneficiario)
        self.assertEqual(microalbuminuria.doctor, 'dogtor')
        self.assertEqual(microalbuminuria.fecha,  datetime.date(2019, 3, 7))
        self.assertEqual(microalbuminuria.metodo, 'normal')
        self.assertEqual(microalbuminuria.micro_albumina, 5)
        self.assertEqual(microalbuminuria.micro_albumina_min, 0)
        self.assertEqual(microalbuminuria.micro_albumina_max, 30)
        self.assertEqual(microalbuminuria.micro_albumina_comentario, 'Hola')
        self.assertEqual(microalbuminuria.creatinina, 80)
        self.assertEqual(microalbuminuria.creatinina_min,  10)
        self.assertEqual(microalbuminuria.creatinina_max, 300)
        self.assertEqual(microalbuminuria.creatinina_comentario, 'Adios')
        self.assertEqual(microalbuminuria.relacion, 10)
        self.assertEqual(microalbuminuria.relacion_normal_min, 0)
        self.assertEqual(microalbuminuria.relacion_normal_max, 30)
        self.assertEqual(microalbuminuria.relacion_anormal_min, 30)
        self.assertEqual(microalbuminuria.relacion_anormal_max, 50)
        self.assertEqual(microalbuminuria.relacion_anormal_alta_min, 50)
        self.assertEqual(microalbuminuria.relacion_anormal_alta_max, 300)

    def testMicroalbuminuria_missing_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'doctor': 'dogtor',
                'fecha': '2019-03-07',
                'micro_albumina_min': 0,
                'micro_albumina_max': 30,
                'creatinina': 80,
                'creatinina_min': 10,
                'creatinina_max': 300,
                'relacion_normal_min': 0,
                'relacion_normal_max': 30,
                'relacion_anormal_min': 30,
                'relacion_anormal_max': 50,
                'relacion_anormal_alta_min': 50,
                'relacion_anormal_alta_max': 300
            }
            response = self.client.post('/beneficiarios/1/microalbuminuria/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testMicroalbuminuria_invalid_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'doctor': 'dogtor',
                'fecha': '2019-03-07',
                'metodo': 'normal',
                'micro_albumina': 5,
                'micro_albumina_min': 0,
                'micro_albumina_max': 30,
                'micro_albumina_comentario': "Hola",
                'creatinina': "Este no es numero",
                'creatinina_min': 10,
                'creatinina_max': 300,
                'creatinina_comentario': "Adios",
                'relacion': 10,
                'relacion_normal_min': 0,
                'relacion_normal_max': 30,
                'relacion_anormal_min': 30,
                'relacion_anormal_max': 50,
                'relacion_anormal_alta_min': 50,
                'relacion_anormal_alta_max': 300000000000000000000000
            }
            response = self.client.post('/beneficiarios/1/microalbuminuria/registrar', data)
        self.assertNotEqual(response.content, b'')

    def testMicroalbuminuria_unexisting_beneficiary(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')

        response = self.client.get('/beneficiarios/100/microalbuminuria/registrar', follow=True)

        self.assertEqual(response.status_code, 404)

    def testMicroalbuminuria_no_permission(self):
        self.client.force_login(self.user_cannot_view)

        data = {
            'beneficiario': self.beneficiario.id,
            'doctor': 'dogtor',
            'fecha': '2019-03-07',
            'metodo': 'normal',
            'micro_albumina': 5,
            'micro_albumina_min': 0,
            'micro_albumina_max': 30,
            'micro_albumina_comentario': "Hola",
            'creatinina': 80,
            'creatinina_min': 10,
            'creatinina_max': 300,
            'creatinina_comentario': "Adios",
            'relacion': 10,
            'relacion_normal_min': 0,
            'relacion_normal_max': 30,
            'relacion_anormal_min': 30,
            'relacion_anormal_max': 50,
            'relacion_anormal_alta_min': 50,
            'relacion_anormal_alta_max': 300
        }
        response = self.client.post('/beneficiarios/1/microalbuminuria/registrar', data)
        self.assertEqual(response.status_code, 403)

    def testMicroalbuminuria_has_permission(self):
        self.client.force_login(self.user_can_view)

        data = {
            'beneficiario': self.beneficiario.id,
            'doctor': 'dogtor',
            'fecha': '2019-03-07',
            'metodo': 'normal',
            'micro_albumina': 5,
            'micro_albumina_min': 0,
            'micro_albumina_max': 30,
            'micro_albumina_comentario': "Hola",
            'creatinina': 80,
            'creatinina_min': 10,
            'creatinina_max': 300,
            'creatinina_comentario': "Adios",
            'relacion': 10,
            'relacion_normal_min': 0,
            'relacion_normal_max': 30,
            'relacion_anormal_min': 30,
            'relacion_anormal_max': 50,
            'relacion_anormal_alta_min': 50,
            'relacion_anormal_alta_max': 300
        }
        response = self.client.post('/beneficiarios/1/microalbuminuria/registrar', data)
        self.assertEqual(response.status_code, 302)
        microalbuminuria = Microalbuminuria.objects.filter(beneficiario=self.beneficiario.id).exists()
        self.assertEqual(microalbuminuria, True)


class ViewTamizajeNutricionalTest(TestCase):  # NEF-63

    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_create = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_create = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_create.user_permissions.add(Permission.objects.get(codename="view_tamizajenutricional"))

        self.tamizaje_nutricional = TamizajeNutricional.objects.create(
            fecha_creacion='2019-03-07',
            fecha='2019-03-07',
            presion_sistolica='10',
            presion_diastolica='10',
            peso='10',
            talla='10',
            circunferencia_brazo='10',
            pliegue_bicipital='10',
            pliegue_tricipital='10',
            imc='95',
            beneficiario=self.beneficiario)
        self.tamizaje_nutricional.save()

    def test_user_can_create_tamizaje(self):
        self.client.force_login(self.user_can_create)
        url = '/tamizajenutricional/' + str(self.tamizaje_nutricional.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Talla")
        self.assertContains(response, "10")

    def test_user_cannot_create_tamizaje(self):
        self.client.force_login(self.user_cannot_create)
        url = '/tamizajenutricional/' + str(self.tamizaje_nutricional.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class EscalaHamiltonTest(TestCase):  # NEF-54

    def setUp(self):
        beneficiario = Beneficiario.objects.create(
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
            vivienda_propia=True)
        beneficiario.save()

        self.user = User.objects.create_superuser('user', 'user@testuser.com', 'passphrase')
        self.user.save()
        self.usernoperms = User.objects.create_user('user_no_permission', 'user@testuser.com', 'password')
        self.usernoperms.save()

    def testEscalaHamilton_success(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'resultado': 4,
                'observaciones': 'Solo reacciones sad :('
            }
            response = self.client.post('/beneficiarios/1/escalahamilton/registrar', data)
            escala_hamilton = EscalaHamilton.objects.get(resultado=4)
            self.assertTrue(escala_hamilton)

    def testEscalaHamilton_right_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'resultado': 4,
                'observaciones': 'Solo reacciones sad :('
            }
            response = self.client.post('/beneficiarios/1/escalahamilton/registrar', data)
            escala_hamilton = EscalaHamilton.objects.get(resultado=4)
            self.assertEqual(escala_hamilton.beneficiario, beneficiario)
            self.assertEqual(escala_hamilton.fecha, datetime.date(2019, 3, 7))
            self.assertEqual(escala_hamilton.resultado, 4)
            self.assertEqual(escala_hamilton.observaciones, 'Solo reacciones sad :(')

    def testEscalaHamilton_missing_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'observaciones': 'Solo reacciones sad :('
            }
            response = self.client.post('/beneficiarios/' + str(beneficiario.id) + '/escalahamilton/registrar', data)
            self.assertNotEqual(response.content, b'')

    def testEscalaHamilton_invalid_fields(self):
        loginresponse = self.client.login(username='user',
                                          password='passphrase')
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'observaciones': 78
            }
            response = \
                self.client.post('/beneficiarios/'
                                 + str(beneficiario.id) + '/escalahamilton/registrar', data)
            self.assertNotEqual(response.content, b'')

    def testEscalaHamilton_no_permission(self):
        loginresponse = self.client.login(username='user_no_permission',
                                          password='password')

        if loginresponse:
            beneficiario = Beneficiario.objects.get(apellido_paterno="a")
            response = \
                self.client.get('/beneficiarios/'
                                + str(beneficiario.id) + '/escalahamilton/registrar', follow=True)

            self.assertEqual(response.status_code, 403)

    def testEscalaHamilton_view_no_perms(self):  # NEF-55
        loginresponse = self.client.login(username='user_no_permission',
                                          password='password')

        self.usernoperms.user_permissions.add(Permission.objects.get(codename="add_escalahamilton"))
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'resultado': 4,
                'observaciones': 'Solo reacciones sad'
            }
            response = self.client.post('/beneficiarios/1/escalahamilton/registrar', data)
            escala_hamilton = EscalaHamilton.objects.latest('id')
            response = self.client.get('/escalahamilton/'+str(escala_hamilton.id))
            self.assertEqual(response.status_code, 403)

    def testEscalaHamilton_view_perms(self):  # NEF-55
        loginresponse = self.client.login(username='user_no_permission',
                                          password='password')
        self.usernoperms.user_permissions.add(Permission.objects.get(codename="add_escalahamilton"))
        self.usernoperms.user_permissions.add(Permission.objects.get(codename="view_escalahamilton"))
        beneficiario = Beneficiario.objects.get(nombre="a")

        if loginresponse:
            data = {
                'beneficiario': beneficiario.id,
                'fecha': '2019-03-07',
                'resultado': 4,
                'observaciones': 'Solo reacciones sad'
            }
            response = self.client.post('/beneficiarios/1/escalahamilton/registrar', data)
            escala_hamilton = EscalaHamilton.objects.latest('id')
            response = self.client.get('/escalahamilton/'+str(escala_hamilton.id))
            self.assertEqual(response.status_code, 200)


class ConsultaMedicaCreateTest(TestCase):  # NEF-46
    def setUp(self):
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
            vivienda_propia=True)

        self.beneficiario.save()

        self.user_can_create = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_create = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_create.user_permissions.add(Permission.objects.get(codename="add_consultamedica"))

    def test_consultamedica_register_success(self):
        self.client.force_login(self.user_can_create)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_creacion': '2019-03-07',
            'peso': 32,
            'talla': 1.32,
            'imc': 20,
            'frecuencia_cardiaca': 123,
            'frecuencia_respiratoria': 60,
            'temperatura': 32,
            'especificaciones': 'Juan es chido',
            'analisis_enfermedad': 'Se está muriendo',
            'plan': 'Seguir siendo chido mientras muere',
            'tratamiento': 'alcoholes',
            'observaciones': 'Ábrete un tinder',
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id)+'/consultamedica/registrar', data)
        self.consultamedica = ConsultaMedica.objects.get(talla=1.32)
        self.assertEqual(response.status_code, 302)
        exists = ConsultaMedica.objects.filter(beneficiario=self.beneficiario.id).exists()
        self.assertEqual(exists, True)

    def test_consultamedica_register_wrong_field(self):
        self.client.force_login(self.user_can_create)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_creacion': '2019-03-07',
            'peso': 32,
            'talla': 'sdcs',
            'imc': 20,
            'frecuencia_cardiaca': 123,
            'frecuencia_respiratoria': 60,
            'temperatura': 32,
            'especificaciones': 'Juan es chido',
            'analisis_enfermedad': 'Se está muriendo',
            'plan': 'Seguir siendo chido mientras muere',
            'tratamiento': 'alcoholes',
            'observaciones': 'Ábrete un tinder',
        }
        response = self.client.post('/beneficiarios/1/consultamedica/registrar', data)
        self.assertEqual(response.status_code, 404)

    def test_consultamedica_register_missing_field(self):
        self.client.force_login(self.user_can_create)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_creacion': '2019-03-07',
            'peso': 32,
            'talla': '',
            'imc': 20,
            'frecuencia_cardiaca': 123,
            'frecuencia_respiratoria': 60,
            'temperatura': 32,
            'especificaciones': 'Juan es chido',
            'analisis_enfermedad': 'Se está muriendo',
            'plan': 'Seguir siendo chido mientras muere',
            'tratamiento': 'alcoholes',
            'observaciones': 'Ábrete un tinder',
        }
        response = self.client.post('/beneficiarios/1/consultamedica/registrar', data)
        self.assertEqual(response.status_code, 404)

    def test_consultamedica_view_no_permission(self):
        self.client.force_login(self.user_can_create)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_creacion': '2019-03-07',
            'peso': 32,
            'talla': 1.32,
            'imc': 20,
            'frecuencia_cardiaca': 123,
            'frecuencia_respiratoria': 60,
            'temperatura': 32,
            'especificaciones': 'Juan es chido',
            'analisis_enfermedad': 'Se está muriendo',
            'plan': 'Seguir siendo chido mientras muere',
            'tratamiento': 'alcoholes',
            'observaciones': 'Ábrete un tinder',
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id)+'/consultamedica/registrar', data)
        self.consultamedica = ConsultaMedica.objects.get(talla=1.32)
        url = '/consultamedica/' + str(self.consultamedica.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_consultamedica_view_permission(self):
        self.client.force_login(self.user_can_create)
        data = {
            'beneficiario': self.beneficiario.id,
            'fecha_creacion': '2019-03-07',
            'peso': 32,
            'talla': 1.32,
            'imc': 20,
            'frecuencia_cardiaca': 123,
            'frecuencia_respiratoria': 60,
            'temperatura': 32,
            'especificaciones': 'Juan es chido',
            'analisis_enfermedad': 'Se está muriendo',
            'plan': 'Seguir siendo chido mientras muere',
            'tratamiento': 'alcoholes',
            'observaciones': 'Ábrete un tinder',
        }
        response = self.client.post('/beneficiarios/'+str(self.beneficiario.id)+'/consultamedica/registrar', data)
        self.consultamedica = ConsultaMedica.objects.get(talla=1.32)
        self.user_can_create.user_permissions.add(Permission.objects.get(codename="view_consultamedica"))
        url = '/consultamedica/' + str(self.consultamedica.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ViewMalnutricionInflamacionTest(TestCase):  # NEF-51
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_malnutricioninflamacion"))

        self.tamizaje_nutricional = TamizajeNutricional.objects.create(
            fecha_creacion='2019-03-07',
            fecha='2019-03-07',
            presion_sistolica='10',
            presion_diastolica='10',
            peso='10',
            talla='10',
            circunferencia_brazo='10',
            pliegue_bicipital='10',
            pliegue_tricipital='10',
            imc='95',
            beneficiario=self.beneficiario)
        self.tamizaje_nutricional.save()

        self.malnutricion_inflamacion = MalnutricionInflamacion.objects.create(
            beneficiario=self.beneficiario,
            fecha='2019-03-07',
            porcentaje_perdida_peso=1,
            perdida_peso=2,
            peso=4,
            talla=3,
            imc_valor=2,
            imc_puntos=2,
            ingesta_alimentaria=4,
            gastrointestinales=4,
            incapacidad=5,
            comorbilidad=4,
            grasa_subcutanea=1,
            perdida_muscular=1,
            edema=2,
            fijacion_hierro=1,
            albumina=2,
        )
        self.malnutricion_inflamacion.save()

    def test_user_can_view_malnutricion_inflamacion(self):
        self.client.force_login(self.user_can_view)
        url = '/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Diarrea")
        self.assertContains(response, "Silla de ruedas")

    def test_user_cannot_view_malnutricion_inflamacion(self):
        self.client.force_login(self.user_cannot_view)
        url = '/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_user_can_change_malnutricion_inflamacion(self):
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="change_malnutricioninflamacion"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_malnutricioninflamacion"))
        self.client.force_login(self.user_can_view)
        url = '/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.id)
        response = self.client.get(url)
        self.assertContains(response, "Editar")

    def test_user_cannot_change_malnutricion_inflamacion(self):
        self.client.force_login(self.user_can_view)
        url = '/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Editar")


class ModifyMicroalbuminuriaTest(TestCase):  # NEF- 78

    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()

        self.ma = Microalbuminuria.objects.create(
            beneficiario=self.beneficiario,
            doctor='dogtor',
            fecha='2019-03-07',
            metodo='normal',
            micro_albumina=45,
            micro_albumina_min=0,
            micro_albumina_max=30,
            micro_albumina_comentario="Hola",
            creatinina=1.02,
            creatinina_min=10,
            creatinina_max=300,
            creatinina_comentario="Adios",
            relacion=10,
            relacion_normal_min=0,
            relacion_normal_max=30,
            relacion_anormal_min=30,
            relacion_anormal_max=50,
            relacion_anormal_alta_min=50,
            relacion_anormal_alta_max=300
        )
        self.ma.save()

        self.user_cannot_modify = User.objects.create_user(username="usercannotmodify", email=None, password=None)
        self.user_cannot_modify.user_permissions.add(Permission.objects.get(codename="view_microalbuminuria"))
        self.user_cannot_modify.save()

        self.user_can_modify = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="view_microalbuminuria"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="change_microalbuminuria"))
        self.user_can_modify.save()

    def test_admin_modify(self):
        client = Client()
        client.force_login(self.user_can_modify)
        response = client.get('/microalbuminuria/' + str(self.ma.pk), follow=True)
        self.assertContains(response, "Editar")

    def test_not_admin_modify(self):
        client = Client()
        client.force_login(self.user_cannot_modify)
        response = client.get('/microalbuminuria/' + str(self.ma.pk), follow=True)
        self.assertNotContains(response, "Editar")


class ChangeQuimicaSanguineaTest(TestCase):  # NEF-68

    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="change_quimicasanguinea"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_quimicasanguinea"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_quimicasanguinea"))

        self.quimica_sanguinea = QuimicaSanguinea.objects.create(
            beneficiario=self.beneficiario,
            fecha_creacion="2019-05-02",
            fecha="2019-05-02",
            doctor='Martin',
            metodo='X-23',
            glucosa=10,
            max_glucosa=15,
            min_glucosa=5,
            comentario_glucosa='Pedro infante murió',
            urea=7,
            max_urea=8,
            min_urea=2,
            comentario_urea='El elegido ha llegado',
            bun=4,
            max_bun=10,
            min_bun=7,
            comentario_bun='La proteina se descompone con nitrogeno',
            creatinina=5,
            max_creatinina_h=10,
            max_creatinina_m=7,
            min_creatinina_h=2,
            min_creatinina_m=1,
            comentario_creatinina='Eso dicen'
        )
        self.quimica_sanguinea.save()

    def test_user_can_change_quimica_sanquinea(self):
        self.client.force_login(self.user_can_view)
        url = '/quimicasanguinea/' + str(self.quimica_sanguinea.id)
        response = self.client.get(url)
        self.assertContains(response, "Editar")

    def test_user_can_not_change_quimica_sanquinea(self):
        self.client.force_login(self.user_cannot_view)
        url = '/quimicasanguinea/' + str(self.quimica_sanguinea.id)
        response = self.client.get(url)


class ModifyMalNutricionInflamacionTest(TestCase):  # NEF-52

    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_cannot_modify = User.objects.create_user(username="usercannotmodify", email=None, password=None)
        self.user_cannot_modify.user_permissions.add(Permission.objects.get(codename="view_malnutricioninflamacion"))
        self.user_cannot_modify.save()

        self.user_can_modify = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="view_malnutricioninflamacion"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="change_malnutricioninflamacion"))
        self.user_can_modify.save()

        self.tamizaje = TamizajeNutricional.objects.create(
            beneficiario=self.beneficiario,
            fecha="2019-03-07",
            presion_sistolica=120,
            presion_diastolica=40,
            peso=68,
            talla=1.65,
            circunferencia_brazo=40,
            pliegue_bicipital=1,
            pliegue_tricipital=1,
        )
        self.tamizaje.save()

        self.malnutricion_inflamacion = MalnutricionInflamacion.objects.create(
            beneficiario=self.beneficiario,
            fecha='2019-03-07',
            porcentaje_perdida_peso=1,
            perdida_peso=2,
            peso=4,
            talla=3,
            imc_valor=2,
            imc_puntos=2,
            ingesta_alimentaria=4,
            gastrointestinales=4,
            incapacidad=5,
            comorbilidad=4,
            grasa_subcutanea=1,
            perdida_muscular=1,
            edema=2,
            fijacion_hierro=1,
            albumina=2,
        )
        self.malnutricion_inflamacion.save()

    def test_admin_modify(self):
        client = Client()
        client.force_login(self.user_can_modify)
        response = client.get('/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.pk), follow=True)
        self.assertContains(response, "Editar")

    def test_not_admin_modify(self):
        client = Client()
        client.force_login(self.user_cannot_modify)
        response = client.get('/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.pk), follow=True)
        self.assertNotContains(response, "Editar")


class ModifyTamizajeTest(TestCase):  # NEF-64

    def setUp(self):
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
            vivienda_propia=True)

        self.user_cannot_modify = User.objects.create_user(username="usercannotmodify", email=None, password=None)
        self.user_cannot_modify.user_permissions.add(Permission.objects.get(codename="view_tamizajenutricional"))

        self.user_can_modify = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="view_tamizajenutricional"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="change_tamizajenutricional"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="add_tamizajenutricional"))

        self.tamizaje = TamizajeNutricional.objects.create(
            beneficiario=self.beneficiario,
            fecha="2019-03-07",
            presion_sistolica=120,
            presion_diastolica=40,
            peso=68,
            talla=1.65,
            circunferencia_brazo=40,
            pliegue_bicipital=1,
            pliegue_tricipital=1,
        )

    def test_admin_modify(self):
        client = Client()
        client.force_login(self.user_can_modify)
        response = client.get('/tamizajenutricional/' + str(self.tamizaje.pk), follow=True)
        self.assertContains(response, "Editar")

    def test_not_admin_modify(self):
        client = Client()
        client.force_login(self.user_cannot_modify)
        response = client.get('/tamizajenutricional/' + str(self.tamizaje.pk), follow=True)
        self.assertNotContains(response, "Editar")


class ModifyHamiltonTest(TestCase):    # NEF-56
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_escalahamilton"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="change_escalahamilton"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_escalahamilton"))

        self.hamilton = EscalaHamilton.objects.create(
            beneficiario=self.beneficiario,
            fecha='2019-03-02',
            resultado=5,
            observaciones='Comentario',
        )
        self.hamilton.save()

    def test_user_can_change_hamilton(self):
        self.client.force_login(self.user_can_view)
        url = '/escalahamilton/' + str(self.hamilton.id)
        response = self.client.get(url)
        self.assertContains(response, "Editar")

    def test_user_cannot_change_hamilton(self):
        self.client.force_login(self.user_cannot_view)
        url = '/escalahamilton/' + str(self.hamilton.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Editar")


class ModifyHemoglobinaGlucosiladaTest(TestCase):  # NEF-72

    def setUp(self):
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
            vivienda_propia=True)

        self.user_cannot_modify = User.objects.create_user(username="usercannotmodify", email=None, password=None)
        self.user_cannot_modify.user_permissions.add(Permission.objects.get(codename="view_hemoglobinaglucosilada"))

        self.user_can_modify = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="view_hemoglobinaglucosilada"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="change_hemoglobinaglucosilada"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="add_hemoglobinaglucosilada"))

        self.hemoglobinaglucosilada = HemoglobinaGlucosilada.objects.create(
            beneficiario=self.beneficiario,
            fecha_captura="2019-03-07",
            metodo="Nuevo",
            doctor="Jo",
            comentario="sd",
            hemoglobina_glucosilada="12",
            max_no_diabetico="32",
            min_no_diabetico="12",
            max_diabetico_cont="32",
            min_diabetico_cont="2",
            max_diabetico_no_cont="2",
            min_diabetico_no_cont="2",
        )

    def test_admin_modify(self):
        client = Client()
        client.force_login(self.user_can_modify)
        response = client.get('/hemoglobinaglucosilada/' + str(self.hemoglobinaglucosilada.pk), follow=True)
        self.assertContains(response, "Editar")

    def test_not_admin_modify(self):
        client = Client()
        client.force_login(self.user_cannot_modify)
        response = client.get('/hemoglobinaglucosilada/' + str(self.hemoglobinaglucosilada.pk), follow=True)
        self.assertNotContains(response, "Editar")


class ChangeGlucosaCapilarTest(TestCase):    # NEF-82
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_glucosacapilar"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="change_glucosacapilar"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_glucosacapilar"))

        self.glucosa_capilar = GlucosaCapilar.objects.create(
            beneficiario=self.beneficiario,
            fecha_creacion='2019-03-02',
            fecha='2019-03-02',
            doctor='Doctor',
            metodo='Método',
            glucosa=5,
            min=2,
            max=6,
            comentario='Comentario de glucosa capilar'
        )
        self.glucosa_capilar.save()

    def test_user_can_change_glucosa_capilar(self):
        self.client.force_login(self.user_can_view)
        url = '/glucosacapilar/' + str(self.glucosa_capilar.id)
        response = self.client.get(url)
        self.assertContains(response, "Editar")

    def test_user_cannot_change_glucosa_capilar(self):
        self.client.force_login(self.user_cannot_view)
        url = '/glucosacapilar/' + str(self.glucosa_capilar.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Editar")


class ChangeConsultaMedicaTest(TestCase):    # NEF-48
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_consultamedica"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="change_consultamedica"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_consultamedica"))

        self.consulta_medica = ConsultaMedica.objects.create(
            beneficiario=self.beneficiario,
            fecha_creacion="2019-02-01",
            peso=60,
            talla=58,
            imc=1.5,
            temperatura=32,
            frecuencia_cardiaca=18,
            frecuencia_respiratoria=20,
            especificaciones="texto de esp",
            analisis_enfermedad="enfermedad de la enferma",
            plan="comer bien",
            tratamiento="cuidate baby",
            observaciones="yas queen"
        )

    def test_user_can_change_consulta_medica(self):
        self.client.force_login(self.user_can_view)
        url = '/consultamedica/' + str(self.consulta_medica.id)
        response = self.client.get(url)
        self.assertContains(response, "Editar")

    def test_user_cannot_change_consulta_medica(self):
        self.client.force_login(self.user_cannot_view)
        url = '/consultamedica/' + str(self.consulta_medica.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Editar")


class DeleteConsultaMedicaTest(TestCase):    # NEF-49
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_consultamedica"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_consultamedica"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_consultamedica"))

        self.consulta_medica = ConsultaMedica.objects.create(
            beneficiario=self.beneficiario,
            fecha_creacion="2019-02-01",
            peso=60,
            talla=58,
            imc=1.5,
            temperatura=32,
            frecuencia_cardiaca=18,
            frecuencia_respiratoria=20,
            especificaciones="texto de esp",
            analisis_enfermedad="enfermedad de la enferma",
            plan="comer bien",
            tratamiento="cuidate baby",
            observaciones="yas queen"
        )

    def test_user_can_delete_consulta_medica(self):
        self.client.force_login(self.user_can_view)
        url = '/consultamedica/' + str(self.consulta_medica.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_consulta_medica(self):
        self.client.force_login(self.user_cannot_view)
        url = '/consultamedica/' + str(self.consulta_medica.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_consulta_medica_delete(self):
        self.client.force_login(self.user_can_view)
        url = '/consultamedica/' + str(self.consulta_medica.id) + '/eliminar'
        response = self.client.post(url)
        consulta = ConsultaMedica.objects.filter(id=self.consulta_medica.id)
        self.assertEqual(consulta.count(), 0)


class DeleteMalnutricionInflamacion(TestCase):  # NEF-53
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_cannot_delete = User.objects.create_user(username="usercannotmodify", email=None, password=None)
        self.user_cannot_delete.user_permissions.add(Permission.objects.get(codename="view_malnutricioninflamacion"))
        self.user_cannot_delete.save()

        self.user_can_delete = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_delete.user_permissions.add(Permission.objects.get(codename="view_malnutricioninflamacion"))
        self.user_can_delete.user_permissions.add(Permission.objects.get(codename="delete_malnutricioninflamacion"))
        self.user_can_delete.save()

        self.tamizaje = TamizajeNutricional.objects.create(
            beneficiario=self.beneficiario,
            fecha="2019-03-07",
            presion_sistolica=120,
            presion_diastolica=40,
            peso=68,
            talla=1.65,
            circunferencia_brazo=40,
            pliegue_bicipital=1,
            pliegue_tricipital=1,
        )
        self.tamizaje.save()

        self.malnutricion_inflamacion = MalnutricionInflamacion.objects.create(
            beneficiario=self.beneficiario,
            fecha='2019-03-07',
            porcentaje_perdida_peso=1,
            perdida_peso=2,
            peso=4,
            talla=3,
            imc_valor=2,
            imc_puntos=2,
            ingesta_alimentaria=4,
            gastrointestinales=4,
            incapacidad=5,
            comorbilidad=4,
            grasa_subcutanea=1,
            perdida_muscular=1,
            edema=2,
            fijacion_hierro=1,
            albumina=2,
        )
        self.malnutricion_inflamacion.save()

    def test_user_can_delete_malnutricion(self):
        self.client.force_login(self.user_can_delete)
        url = '/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_malnutricion(self):
        self.client.force_login(self.user_cannot_delete)
        url = '/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_malnutricion_delete(self):
        self.client.force_login(self.user_can_delete)
        url = '/malnutricioninflamacion/' + str(self.malnutricion_inflamacion.id) + '/eliminar'
        response = self.client.post(url)
        malnutricion = MalnutricionInflamacion.objects.filter(id=self.malnutricion_inflamacion.id)
        self.assertEqual(malnutricion.count(), 0)


class DeleteMicroalbuminuriaTest(TestCase):  # NEF- 79
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()

        self.microalbuminuria = Microalbuminuria.objects.create(
            beneficiario=self.beneficiario,
            doctor='dogtor',
            fecha='2019-03-07',
            metodo='normal',
            micro_albumina=45,
            micro_albumina_min=0,
            micro_albumina_max=30,
            micro_albumina_comentario="Hola",
            creatinina=1.02,
            creatinina_min=10,
            creatinina_max=300,
            creatinina_comentario="Adios",
            relacion=10,
            relacion_normal_min=0,
            relacion_normal_max=30,
            relacion_anormal_min=30,
            relacion_anormal_max=50,
            relacion_anormal_alta_min=50,
            relacion_anormal_alta_max=300
        )
        self.microalbuminuria.save()

        self.user_cannot_delete = User.objects.create_user(username="usercannotmodify", email=None, password=None)
        self.user_cannot_delete.user_permissions.add(Permission.objects.get(codename="view_microalbuminuria"))
        self.user_cannot_delete.save()

        self.user_can_delete = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_delete.user_permissions.add(Permission.objects.get(codename="view_microalbuminuria"))
        self.user_can_delete.user_permissions.add(Permission.objects.get(codename="delete_microalbuminuria"))
        self.user_can_delete.save()

    def test_user_can_delete_microalbuminuria(self):
        self.client.force_login(self.user_can_delete)
        url = '/microalbuminuria/' + str(self.microalbuminuria.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_microalbuminuria(self):
        self.client.force_login(self.user_cannot_delete)
        url = '/microalbuminuria/' + str(self.microalbuminuria.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_microalbuminuria_delete(self):
        self.client.force_login(self.user_can_delete)
        url = '/microalbuminuria/' + str(self.microalbuminuria.id) + '/eliminar'
        response = self.client.post(url)
        microalbuminuria = Microalbuminuria.objects.filter(id=self.microalbuminuria.id)
        self.assertEqual(microalbuminuria.count(), 0)


class ChangeFactorRiesgoTest(TestCase):    # NEF-592
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_factorderiesgo"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="change_factorderiesgo"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_factorderiesgo"))

        self.factor_riesgo = FactorDeRiesgo.objects.create(
            beneficiario=self.beneficiario,
            fecha_creacion="2019-02-01",
            fecha="2019-02-01",
            p_1=0,
            p_2=0,
            p_3=0,
            p_4=0,
            p_5=0,
            p_6=0,
            p_7=0,
            p_8=0,
            p_9=0,
            p_10=0,
            p_11=0,
            p_12=0,
            comentario="comentario"
        )

        self.factor_riesgo.save()

    def test_user_can_change_consulta_medica(self):
        self.client.force_login(self.user_can_view)
        url = '/factorderiesgo/' + str(self.factor_riesgo.id)
        response = self.client.get(url)
        self.assertContains(response, "Editar")

    def test_user_cannot_change_consulta_medica(self):
        self.client.force_login(self.user_cannot_view)
        url = '/factorderiesgo/' + str(self.factor_riesgo.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Editar")


class QuimicaSanguineaDeleteTest(TestCase):  # NEF-69
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="change_quimicasanguinea"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_quimicasanguinea"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_quimicasanguinea"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_quimicasanguinea"))

        self.quimica_sanguinea = QuimicaSanguinea.objects.create(
            beneficiario=self.beneficiario,
            fecha_creacion="2019-05-02",
            fecha="2019-05-02",
            doctor='Martin',
            metodo='X-23',
            glucosa=10,
            max_glucosa=15,
            min_glucosa=5,
            comentario_glucosa='Pedro infante murió',
            urea=7,
            max_urea=8,
            min_urea=2,
            comentario_urea='El elegido ha llegado',
            bun=4,
            max_bun=10,
            min_bun=7,
            comentario_bun='La proteina se descompone con nitrogeno',
            creatinina=5,
            max_creatinina_h=10,
            max_creatinina_m=7,
            min_creatinina_h=2,
            min_creatinina_m=1,
            comentario_creatinina='Eso dicen'
        )
        self.quimica_sanguinea.save()

    def test_user_can_delete_quimica_sanguinea(self):
        self.client.force_login(self.user_can_view)
        url = '/quimicasanguinea/' + str(self.quimica_sanguinea.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_quimica_sanguinea(self):
        self.client.force_login(self.user_cannot_view)
        url = '/quimicasanguinea/' + str(self.quimica_sanguinea.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_quimica_sanguinea_delete(self):
        self.client.force_login(self.user_can_view)
        url = '/quimicasanguinea/' + str(self.quimica_sanguinea.id) + '/eliminar'
        response = self.client.post(url)
        quimicas = QuimicaSanguinea.objects.filter(id=self.quimica_sanguinea.id)
        self.assertEqual(quimicas.count(), 0)


class DeleteFactorDeRiesgoTest(TestCase):    # NEF-153
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_factorderiesgo"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_factorderiesgo"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_factorderiesgo"))

        self.factor_de_riesgo = FactorDeRiesgo.objects.create(
            beneficiario=self.beneficiario,
            p_1=1,
            p_1_cual="una",
            p_2=1,
            p_2_2=1,
            p_3=1,
            p_3_2=1,
            p_4=1,
            p_5=1,
            p_6=1,
            p_7=1,
            p_8=1,
            p_8_2=1,
            p_9=1,
            p_10=1,
            p_11=1,
            p_12=1
        )

    def test_user_can_delete_factor_de_riesgo(self):
        self.client.force_login(self.user_can_view)
        url = '/factorderiesgo/' + str(self.factor_de_riesgo.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_factor_de_riesgo(self):
        self.client.force_login(self.user_cannot_view)
        url = '/factorderiesgo/' + str(self.factor_de_riesgo.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_factor_de_riesgo_delete(self):
        self.client.force_login(self.user_can_view)
        url = '/factorderiesgo/' + str(self.factor_de_riesgo.id) + '/eliminar'
        response = self.client.post(url)
        factor = FactorDeRiesgo.objects.filter(id=self.factor_de_riesgo.id)
        self.assertEqual(factor.count(), 0)


class DeleteTamizajeNutricionalTest(TestCase):    # NEF-65
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_tamizajenutricional"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_tamizajenutricional"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_tamizajenutricional"))

        self.tamizaje_nutricional = TamizajeNutricional.objects.create(
            beneficiario=self.beneficiario,
            presion_sistolica=1,
            presion_diastolica=1,
            peso=1,
            talla=1,
            circunferencia_brazo=1,
            pliegue_bicipital=1,
            pliegue_tricipital=1
        )

    def test_user_can_delete_tamizaje_nutricional(self):
        self.client.force_login(self.user_can_view)
        url = '/tamizajenutricional/' + str(self.tamizaje_nutricional.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_tamizaje_nutricional(self):
        self.client.force_login(self.user_cannot_view)
        url = '/tamizajenutricional/' + str(self.tamizaje_nutricional.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_tamizaje_nutricional_delete(self):
        self.client.force_login(self.user_can_view)
        url = '/tamizajenutricional/' + str(self.tamizaje_nutricional.id) + '/eliminar'
        response = self.client.post(url)
        tamizaje = TamizajeNutricional.objects.filter(id=self.tamizaje_nutricional.id)
        self.assertEqual(tamizaje.count(), 0)


class DeleteGlucosaCapilarTest(TestCase):    # NEF-65
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_glucosacapilar"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_glucosacapilar"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_glucosacapilar"))

        self.glucosa_capilar = GlucosaCapilar.objects.create(
            beneficiario=self.beneficiario,
            doctor='este',
            metodo='otro',
            glucosa=79
        )

    def test_user_can_delete_glucosa_capilar(self):
        self.client.force_login(self.user_can_view)
        url = '/glucosacapilar/' + str(self.glucosa_capilar.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_glucosa_capilar(self):
        self.client.force_login(self.user_cannot_view)
        url = '/glucosacapilar/' + str(self.glucosa_capilar.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_glucosa_capilar_delete(self):
        self.client.force_login(self.user_can_view)
        url = '/glucosacapilar/' + str(self.glucosa_capilar.id) + '/eliminar'
        response = self.client.post(url)
        glucosa = GlucosaCapilar.objects.filter(id=self.glucosa_capilar.id)
        self.assertEqual(glucosa.count(), 0)


class DeleteHemoglobinaGlucosiladaTest(TestCase):    # NEF-73
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_hemoglobinaglucosilada"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_hemoglobinaglucosilada"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_hemoglobinaglucosilada"))

        self.hemo_gluco = HemoglobinaGlucosilada.objects.create(
            beneficiario=self.beneficiario,
            doctor='este',
            metodo='otro',
            hemoglobina_glucosilada=1,
            max_no_diabetico=1,
            min_no_diabetico=1,
            max_diabetico_no_cont=1,
            min_diabetico_no_cont=1,
            max_diabetico_cont=1,
            min_diabetico_cont=1
        )

    def test_user_can_delete_hemo_gluco(self):
        self.client.force_login(self.user_can_view)
        url = '/hemoglobinaglucosilada/' + str(self.hemo_gluco.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_hemo_gluco(self):
        self.client.force_login(self.user_cannot_view)
        url = '/hemoglobinaglucosilada/' + str(self.hemo_gluco.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_hemo_gluco_delete(self):
        self.client.force_login(self.user_can_view)
        url = '/hemoglobinaglucosilada/' + str(self.hemo_gluco.id) + '/eliminar'
        response = self.client.post(url)
        hemoglobina = HemoglobinaGlucosilada.objects.filter(id=self.hemo_gluco.id)
        self.assertEqual(hemoglobina.count(), 0)


class DeleteEscalaHamiltonTest(TestCase):    # NEF-57
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_escalahamilton"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_escalahamilton"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_escalahamilton"))

        self.escala_hamilton = EscalaHamilton.objects.create(
            beneficiario=self.beneficiario,
            resultado=10,
        )

    def test_user_can_delete_escala_hamilton(self):
        self.client.force_login(self.user_can_view)
        url = '/escalahamilton/' + str(self.escala_hamilton.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_escala_hamilton(self):
        self.client.force_login(self.user_cannot_view)
        url = '/escalahamilton/' + str(self.escala_hamilton.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_escala_hamilton_delete(self):
        self.client.force_login(self.user_can_view)
        url = '/escalahamilton/' + str(self.escala_hamilton.id) + '/eliminar'
        response = self.client.post(url)
        escala_hamilton = EscalaHamilton.objects.filter(id=self.escala_hamilton.id)
        self.assertEqual(escala_hamilton.count(), 0)


class DeleteAdherenciaTratamientoTest(TestCase):    # NEF-61
    def setUp(self):
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
            vivienda_propia=True)
        self.beneficiario.save()
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_adherenciatratamiento"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="delete_adherenciatratamiento"))
        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_adherenciatratamiento"))

        self.adherencia_tratamiento = AdherenciaTratamiento.objects.create(
            beneficiario=self.beneficiario,
            p1=10,
            p2=10,
            p3=10,
            p4=10,
            p5=10,
            p6=10,
            p7=10,
            p8=10,
            p9=10,
            p10=10,
            p11="",
            p12="",
            p13="",
            p14=10,
            p15=10,
            p16=10,
            p17=10,
        )

    def test_user_can_delete_adherencia_tratamiento(self):
        self.client.force_login(self.user_can_view)
        url = '/adherenciatratamiento/' + str(self.adherencia_tratamiento.id)
        response = self.client.get(url)
        self.assertContains(response, "Borrar")

    def test_user_cannot_delete_adherencia_tratamiento(self):
        self.client.force_login(self.user_cannot_view)
        url = '/adherenciatratamiento/' + str(self.adherencia_tratamiento.id)
        response = self.client.get(url)
        self.assertNotContains(response, "Borrar")

    def test_adherencia_tratamiento_delete(self):
        self.client.force_login(self.user_can_view)
        url = '/adherenciatratamiento/' + str(self.adherencia_tratamiento.id) + '/eliminar'
        response = self.client.post(url)
        adherencia_tratamiento = AdherenciaTratamiento.objects.filter(id=self.adherencia_tratamiento.id)
        self.assertEqual(adherencia_tratamiento.count(), 0)
