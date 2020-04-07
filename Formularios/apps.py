from django.apps import AppConfig


class FormulariosConfig(AppConfig):
    name = 'Formularios'

    def ready(self):
        from . import signals
        return super().ready()
