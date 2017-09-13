from django.apps import AppConfig


class AdminKitConfig(AppConfig):
    name = 'admin_kit'

    def ready(self):
        super().ready()
        self.module.autodiscover()
