"""
    Admin Kit apps module.
    This autodiscovers modules

"""

from django.apps import AppConfig

class AdminKitConfig(AppConfig):
    """
    App Config that auto discovers ajax module
    """
    name = 'admin_kit'

    def ready(self):
        super().ready()
        self.module.autodiscover()
