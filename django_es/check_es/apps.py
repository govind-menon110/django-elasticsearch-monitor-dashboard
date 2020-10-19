from django.apps import AppConfig


class CheckEsConfig(AppConfig):
    name = 'check_es'
    def ready(self):
        from . import update_es
        update_es.update_db()
