from weakref import WeakSet
from django.http import HttpResponse
from django.shortcuts import render

all_sites = WeakSet()

__all__ = ['AdminKitSite', 'site']

class AdminKitSite:
    """
    The main AdminKitSite that routes and process url requests.
    
    """
    def __init__(self, name='admin_kit'):
        self._registry = {}
        self.name = name
        all_sites.add(self)

    def ping(self, request):
        return render(request, 'admin_kit/ping.html')

    def register(self, key, admin_class):
        from .ajax import Ajax
        key = Ajax.generate_key(key, admin_class)
        self._registry[key] = admin_class()

    def ajax(self, request, key):
        from .ajax import Ajax
        response = Ajax.route(request, self._registry[key], )
        return response

    def get_urls(self):
        from django.conf.urls import url, include
        from django.contrib.contenttypes import views as contenttype_views

        # Admin-site-wide views.
        urlpatterns = [
            url(r'^ping', self.ping, name='ping'),
            url(r'^ajax/(?P<key>.*)/', self.ajax, name='ajax')
        ]

        # valid_app_labels = []

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        # if valid_app_labels:
        #     regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
        #     urlpatterns += [
        #         url(regex, wrap(self.app_index), name='app_list'),
        #     ]
        return urlpatterns

    @property
    def urls(self):
        from django.contrib import admin
        return self.get_urls(), 'admin_kit', self.name

site = AdminKitSite()
