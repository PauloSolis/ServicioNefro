from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import *
from Formularios.models import *
from Proyectos.models import *
from datetime import datetime, date, timezone


class FiltrarResultadosTest(TestCase):  # NEF-39
    def setUp(self):
        self.user = User.objects.create_user(username="user", email=None, password=None)
        self.user.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        self.beneficiario_one = \
            Beneficiario.objects.create(fecha_registro=datetime.now(timezone.utc),
                                        apellido_paterno="Pérez",
                                        apellido_materno="Suárez",
                                        nombre="Karlos",
                                        sexo=False,
                                        fecha_nacimiento=date(1996, 12, 8),
                                        telefono="1457854887",
                                        celular="4611785774",
                                        correo="correo@correo.com",
                                        activo_laboralmente=True,
                                        nucleo_familiar="Solo",
                                        vivienda_propia=False,
                                        escolaridad="PRI")
        self.beneficiario_two = \
            Beneficiario.objects.create(fecha_registro=datetime.now(timezone.utc),
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
                                        escolaridad="PRI")
        self.qs = QuimicaSanguinea.objects.create(beneficiario=self.beneficiario_one,
                                                  doctor="Doc", metodo="normal", glucosa=1,
                                                  max_glucosa=1, min_glucosa=1, urea=1,
                                                  max_urea=1, min_urea=1, bun=1,
                                                  max_bun=1, min_bun=1, creatinina=1.02,
                                                  max_creatinina_h=1, min_creatinina_h=1,
                                                  max_creatinina_m=1, min_creatinina_m=1)

        self.ma = Microalbuminuria.objects.create(
            beneficiario=self.beneficiario_one,
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

        self.clasificacion_discrepancia = \
            Clasificacion.objects.create(beneficiario=self.beneficiario_one,
                                         categoria_gfr_estimada='G2',
                                         categoria_gfr='G3a',
                                         categoria_alb='A2',
                                         gfr_estimada=15,
                                         gfr=14,
                                         albumina=200,
                                         id_qs=self.qs,
                                         id_ma=self.ma)
        self.clasificacion_g3a = \
            Clasificacion.objects.create(beneficiario=self.beneficiario_two,
                                         categoria_gfr_estimada='G3a',
                                         categoria_gfr='G3a',
                                         categoria_alb='A2',
                                         gfr_estimada=15,
                                         gfr=14,
                                         albumina=200,
                                         id_qs=self.qs,
                                         id_ma=self.ma)

        def show_only_categoria(self):
            self.client.force_login(self.user)
            response = self.client.get(('/beneficiario_json?draw=1&columns%5B0%5D'
                                        '%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=id'
                                        '&columns%5B0%5D%5Bsearchable%5D=true&columns'
                                        '%5B0%5D%5Borderable%5D=true&columns%5B0'
                                        '%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0'
                                        '%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname'
                                        '%5D=nombre&columns%5B1%5D%5Bsearchable'
                                        '%5D=true&columns%5B1%5D%5Borderable%5D=true'
                                        '&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns'
                                        '%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=apellido_paterno'
                                        '&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable'
                                        '%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue'
                                        '%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false'
                                        '&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname'
                                        '%5D=apellido_materno&columns%5B3%5D%5Bsearchable'
                                        '%5D=true&columns%5B3%5D%5Borderable%5D=true&columns'
                                        '%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch'
                                        '%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns'
                                        '%5B4%5D%5Bname%5D=sexo&columns%5B4%5D%5Bsearchable%5D=false'
                                        '&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch'
                                        '%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=clasificacion&columns'
                                        '%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false'
                                        '&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch'
                                        '%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns'
                                        '%5B6%5D%5Bname%5D=edad&columns%5B6%5D%5Bsearchable%5D=false'
                                        '&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch'
                                        '%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false'
                                        '&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0'
                                        '&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false'
                                        '&categoria=G3'
                                        '&_=1554914817732'))
            self.assertContains(response,
                                '{"draw": 1, "recordsTotal": 2, "recordsFiltered": 1, "data": [["'
                                + self.beneficiario_two + '",')

        def show_only_search_with_categoria_parameter(self):
            self.client.force_login(self.user)
            response = self.client.get(('/beneficiario_json?draw=1&columns%5B0%5D'
                                        '%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=id'
                                        '&columns%5B0%5D%5Bsearchable%5D=true&columns'
                                        '%5B0%5D%5Borderable%5D=true&columns%5B0'
                                        '%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0'
                                        '%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname'
                                        '%5D=nombre&columns%5B1%5D%5Bsearchable'
                                        '%5D=true&columns%5B1%5D%5Borderable%5D=true'
                                        '&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns'
                                        '%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=apellido_paterno'
                                        '&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable'
                                        '%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue'
                                        '%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false'
                                        '&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname'
                                        '%5D=apellido_materno&columns%5B3%5D%5Bsearchable'
                                        '%5D=true&columns%5B3%5D%5Borderable%5D=true&columns'
                                        '%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch'
                                        '%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns'
                                        '%5B4%5D%5Bname%5D=sexo&columns%5B4%5D%5Bsearchable%5D=false'
                                        '&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch'
                                        '%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=clasificacion&columns'
                                        '%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false'
                                        '&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch'
                                        '%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns'
                                        '%5B6%5D%5Bname%5D=edad&columns%5B6%5D%5Bsearchable%5D=false'
                                        '&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch'
                                        '%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false'
                                        '&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0'
                                        '&length=10'
                                        '&search%5Bvalue%5D=Karla'
                                        '&search%5Bregex%5D=false'
                                        '&categoria=G3'
                                        '&_=1554914817732'))
            self.assertContains(response,
                                '{"draw": 1, "recordsTotal": 2, "recordsFiltered": 1, "data": [["'
                                + self.beneficiario_two + '",')

        def no_show_if_different_categoria_parameter(self):
            self.client.force_login(self.user)
            response = self.client.get(('/beneficiario_json?draw=1&columns%5B0%5D'
                                        '%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=id'
                                        '&columns%5B0%5D%5Bsearchable%5D=true&columns'
                                        '%5B0%5D%5Borderable%5D=true&columns%5B0'
                                        '%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0'
                                        '%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname'
                                        '%5D=nombre&columns%5B1%5D%5Bsearchable'
                                        '%5D=true&columns%5B1%5D%5Borderable%5D=true'
                                        '&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns'
                                        '%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=apellido_paterno'
                                        '&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable'
                                        '%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue'
                                        '%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false'
                                        '&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname'
                                        '%5D=apellido_materno&columns%5B3%5D%5Bsearchable'
                                        '%5D=true&columns%5B3%5D%5Borderable%5D=true&columns'
                                        '%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch'
                                        '%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns'
                                        '%5B4%5D%5Bname%5D=sexo&columns%5B4%5D%5Bsearchable%5D=false'
                                        '&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch'
                                        '%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns'
                                        '%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=clasificacion&columns'
                                        '%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false'
                                        '&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch'
                                        '%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns'
                                        '%5B6%5D%5Bname%5D=edad&columns%5B6%5D%5Bsearchable%5D=false'
                                        '&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch'
                                        '%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false'
                                        '&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0'
                                        '&length=10'
                                        '&search%5Bvalue%5D=Karlos'
                                        '&search%5Bregex%5D=false'
                                        '&categoria=G3'
                                        '&_=1554914817732'))
            self.assertContains(response,
                                '{"draw": 1, "recordsTotal": 2, "recordsFiltered": 1, "data": [["'
                                + self.beneficiario_one + '",')


class BeneficiarioDetailViewTest(TestCase):  # NEF-35
    def setUp(self):
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="add_antecedentes"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="add_microalbuminuria"))
        self.beneficiario = \
            Beneficiario.objects.create(fecha_registro=datetime.now(timezone.utc),
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
                                        escolaridad="PRI")

    def create_antecedentes(self):
        self.antecedentes = \
            Antecedentes.objects.create(beneficiario=self.beneficiario,
                                        enfermedad_cardio_abuelo=True,
                                        enfermedad_cardio_padre=True,
                                        enfermedad_cardio_madre=True,
                                        enfermedad_cardio_hermanos=True,
                                        hta_abuelo=True,
                                        hta_padre=True,
                                        hta_madre=True,
                                        hta_hermanos=True,
                                        diabetes_abuelo=True,
                                        diabetes_padre=True,
                                        diabetes_madre=True,
                                        diabetes_hermanos=True,
                                        dislipidemias_abuelo=True,
                                        dislipidemias_padre=True,
                                        dislipidemias_madre=True,
                                        dislipidemias_hermanos=True,
                                        obesidad_abuelo=True,
                                        obesidad_padre=True,
                                        obesidad_madre=True,
                                        obesidad_hermanos=True,
                                        enfermedad_cerebro_abuelo=True,
                                        enfermedad_cerebro_padre=True,
                                        enfermedad_cerebro_madre=True,
                                        enfermedad_cerebro_hermanos=True,
                                        enfermedad_renal_abuelo=True,
                                        enfermedad_renal_padre=True,
                                        enfermedad_renal_madre=True,
                                        enfermedad_renal_hermanos=True,
                                        drogadiccion=True,
                                        intervencion_quirurgica=True,
                                        intervencion_hospitalaria=True,
                                        enfermedad_cardiovascular=True,
                                        tabaquismo=True,
                                        infeccion_urinaria=True,
                                        sedentarismo=True,
                                        alcoholismo=True,
                                        actividiad_fisica=True)

    def test_user_can_view(self):
        self.client.force_login(self.user_can_view)
        url = '/beneficiarios/' + str(self.beneficiario.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.beneficiario.nombre)
        self.assertContains(response, self.beneficiario.edad)
        self.assertContains(response, '/beneficiarios/' + str(self.beneficiario.id) + '/antecedentes/registrar')

        self.create_antecedentes()

        response = self.client.get(url)
        self.assertContains(response, '/beneficiarios/' + str(self.beneficiario.id) + '/antecedentes/registrar', 0)
        self.assertContains(response, 'Antecedentes')

    def test_user_cannot_view(self):
        self.client.force_login(self.user_cannot_view)
        url = '/beneficiarios/' + str(self.beneficiario.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

        self.user_cannot_view.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        response = self.client.get(url)

        self.assertContains(response, self.beneficiario.nombre)
        self.assertContains(response, self.beneficiario.edad)
        self.assertContains(response, '/beneficiarios/' + str(self.beneficiario.id) + '/antecedentes/registrar', 0)

        self.create_antecedentes()

        response = self.client.get(url)
        self.assertContains(response, 'Antecedentes')


class ViewDiagnosticoTest(TestCase):  # NEF-98
    def setUp(self):
        self.user_can_view = User.objects.create_user(username="usercanview", email=None, password=None)
        self.user_cannot_view = User.objects.create_user(username="usercannotview", email=None, password=None)
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="add_antecedentes"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="add_microalbuminuria"))
        self.user_can_view.user_permissions.add(Permission.objects.get(codename="add_quimicasanguinea"))

        self.beneficiario = \
            Beneficiario.objects.create(fecha_registro=datetime.now(timezone.utc),
                                        apellido_paterno="Pérez",
                                        apellido_materno="García",
                                        nombre="Camanei",
                                        sexo=False,
                                        fecha_nacimiento=date(1996, 12, 8),
                                        telefono="1457854887",
                                        celular="4611785774",
                                        correo="correo@correo.com",
                                        activo_laboralmente=True,
                                        nucleo_familiar="Solo",
                                        vivienda_propia=False,
                                        escolaridad="PRI")

    def test_has_perm(self):
        self.rqs = QuimicaSanguinea.objects.create(beneficiario=self.beneficiario,
                                                   doctor="Doc", metodo="normal", glucosa=1,
                                                   max_glucosa=1, min_glucosa=1, urea=1,
                                                   max_urea=1, min_urea=1, bun=1,
                                                   max_bun=1, min_bun=1, creatinina=1.02,
                                                   max_creatinina_h=1, min_creatinina_h=1,
                                                   max_creatinina_m=1, min_creatinina_m=1)

        self.client.force_login(self.user_can_view)
        url_micro = '/beneficiarios/' + str(self.beneficiario.id) + '/microalbuminuria/registrar'
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
        response = self.client.post(url_micro, data)

        quimica = QuimicaSanguinea.objects.latest("id")
        micro = Microalbuminuria.objects.latest("id")

        url = '/beneficiarios/' + str(self.beneficiario.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.beneficiario.nombre)
        self.assertContains(response, "CKD-EPI")
        self.assertContains(response, "MDRD")

    def test_has_not_perm(self):
        self.rqs = QuimicaSanguinea.objects.create(beneficiario=self.beneficiario,
                                                   doctor="Doc", metodo="normal", glucosa=1,
                                                   max_glucosa=1, min_glucosa=1, urea=1,
                                                   max_urea=1, min_urea=1, bun=1,
                                                   max_bun=1, min_bun=1, creatinina=1.02,
                                                   max_creatinina_h=1, min_creatinina_h=1,
                                                   max_creatinina_m=1, min_creatinina_m=1)

        self.client.force_login(self.user_can_view)
        url_micro = '/beneficiarios/' + str(self.beneficiario.id) + '/microalbuminuria/registrar'
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
        response = self.client.post(url_micro, data)

        self.client.force_login(self.user_cannot_view)

        url = '/beneficiarios/' + str(self.beneficiario.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class BeneficiarioCreateTest(TestCase):  # NEF-29
    def setUp(self):
        self.user_can_create = User.objects.create_user(username="usercancreate",
                                                        email=None, password=None)
        self.user_can_not_create = User.objects.create_user(username="usercantcreate",
                                                            email=None, password=None)
        self.user_can_create.user_permissions.add(Permission.objects.get(codename="add_antecedentes"))
        self.user_can_create.user_permissions.add(Permission.objects.get(codename="add_beneficiario"))
        self.beneficiario = Beneficiario.objects.create(fecha_registro=datetime.now(timezone.utc),
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
                                                        escolaridad="PRI")
        self.jornada = Jornada.objects.create(nombre="piloto",
                                              fecha="2019-03-07",
                                              localidad="Queretarock",
                                              municipio="Qrock",
                                              estado="Qro")

    def test_create_model_exist(self):
        exists = Beneficiario.objects.filter(nombre='Karla').exists()
        self.assertEqual(exists, True)

    def test_user_can_create(self):
        self.client.force_login(self.user_can_create)
        url = '/beneficiarios/registrar'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_create(self):
        self.client.force_login(self.user_can_not_create)
        url = '/beneficiarios/registrar'
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_beneficiario_jornada_register_success(self):
        self.client.force_login(self.user_can_create)
        data = {
            'fecha_registro': '2019-03-07',
            'apellido_paterno': "Pérez",
            'apellido_materno': "Suárez",
            'nombre': "Felipe",
            'sexo': False,
            'fecha_nacimiento': '1998-03-07',
            'telefono': "1457854887",
            'celular': "4611785774",
            'correo': "correo@correo.com",
            'afroamericano': True,
            'diabetico_hipertenso': 1,
            'activo_laboralmente': True,
            'nucleo_familiar': "Solo",
            'vivienda_propia': False,
            'escolaridad': "PRI",
            'nota': "joj",
            'jornada': self.jornada.id,
        }
        response = self.client.post('/'+str(self.jornada.id)+'/beneficiarios/registrar', data)
        self.assertEqual(response.status_code, 302)
        exists = Beneficiario.objects.filter(nombre='Felipe').exists()
        self.assertEqual(exists, True)

    def test_beneficiario_jornada_register_fail(self):  # NEF-21
        self.client.force_login(self.user_can_create)
        data = {
            'fecha_registro': '2019-03-07',
            'apellido_paterno': "Pérez",
            'apellido_materno': "Suárez",
            'nombre': "Felipe",
            'sexo': False,
            'fecha_nacimiento': '1998-03-07',
            'telefono': "1457854887",
            'celular': "4611785774",
            'correo': "correo@correo.com",
            'afroamericano': True,
            'diabetico_hipertenso': 1,
            'activo_laboralmente': True,
            'nucleo_familiar': "Solo",
            'vivienda_propia': False,
            'escolaridad': "PRI",
            'nota': "joj",
            'jornada': 10,
        }
        response = self.client.post('/'+str(self.jornada.id)+'/beneficiarios/registrar', data)
        exists = Beneficiario.objects.filter(nombre='Felipe').exists()
        self.assertEqual(exists, False)


class BeneficiarioRecordTest(TestCase):  # NEF-36

    def setUp(self):
        beneficiario = Beneficiario.objects.create(
            apellido_paterno="a",
            apellido_materno="a",
            nombre="a",
            sexo=True,
            fecha_nacimiento=date(1996, 12, 8),
            telefono="a4344134",
            celular="a434324",
            correo="example@gamil.com",
            activo_laboralmente=True,
            nucleo_familiar='Nucleo bien bonito',
            vivienda_propia=True)
        beneficiario.save()

        self.user = User.objects.create_user(username="userrepo", email=None, password=None)

    def testBeneficiarioRecord_no_perms(self):  # NEF-36
        loginresponse = self.client.force_login(self.user)
        self.beneficiario = Beneficiario.objects.get(nombre="a")
        if loginresponse:
            response = self.client.get('/beneficiarios/'+str(self.beneficiario.id)+'/expediente')
            self.assertEqual(response.status_code, 403)

    def testBeneficiarioRecord_view_perms(self):  # NEF-36
        loginresponse = self.client.force_login(self.user)
        self.user.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        self.beneficiario = Beneficiario.objects.get(nombre="a")
        if loginresponse:
            response = self.client.get('/beneficiarios/'+str(self.beneficiario.id)+'/expediente')
            self.assertEqual(response.status_code, 200)


class ModifyBeneficiarioTest(TestCase):  # NEF-31

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
        self.user_cannot_modify.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        self.user_cannot_modify.user_permissions.add(Permission.objects.get(codename="view_jornada"))

        self.user_can_modify = User.objects.create_user(username="usercanmodify", email=None, password=None)
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="view_beneficiario"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="view_jornada"))
        self.user_can_modify.user_permissions.add(Permission.objects.get(codename="change_beneficiario"))

    def test_admin_modify(self):
        self.client.force_login(self.user_can_modify)
        response = self.client.get('/beneficiarios/' + str(self.beneficiario.pk), follow=True)
        self.assertContains(response, "Editar")

    def test_not_admin_modify(self):
        self.client.force_login(self.user_cannot_modify)
        response = self.client.get('/beneficiarios/' + str(self.beneficiario.pk), follow=True)
        self.assertNotContains(response, "Editar")
