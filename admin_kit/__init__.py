from django.utils.module_loading import autodiscover_modules
from . import widgets, fields, models
from .sites import site
from . import ajax

__all__ = [
    'widgets', 'fields', 'models', 'site', 'autodiscover', 'ajax'
]

def autodiscover():
    autodiscover_modules('ajax', register_to=site)


default_app_config = 'admin_kit.apps.AdminKitConfig'
