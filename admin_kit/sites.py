from weakref import WeakSet
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static

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
        from django.shortcuts import render
        return render(request, 'admin_kit/ping.html')

    def base_js(self, request):
        from django.shortcuts import render
        base_index = request.path.rfind('base.js')
        app_url = request.path[:base_index-1]
        enable_dup = True
        try:
            from django.conf import settings
            enable_dup = not settings.KIT_DISABLE_DUPLICATE
        except AttributeError:
            enable_dup = True
        return render(request, 'admin_kit/base.js', context={"app": app_url, "duplicate": enable_dup}, content_type="text/javascript")

    def register(self, key, ajax_class):
        """
        The function registers, ``ajax_class`` in order to create an Ajax API. 
        """

        from .ajax import Ajax
        key = Ajax.generate_key(key, ajax_class)
        self._registry[key] = ajax_class()

    def ajax(self, request, key):
        from .ajax import Ajax
        response = Ajax.route(request, self._registry[key], )
        return response

    def get_urls(self):
        from django.conf.urls import url
        from django.conf import settings

        urlpatterns = [
            url(r'^ajax/(?P<key>.*)/', self.ajax, name='ajax'),
            url(r'base.js/', self.base_js, name='base_js')
        ]

        if settings.DEBUG:
            urlpatterns += [url(r'^ping', self.ping, name='ping')]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'admin_kit', self.name

site = AdminKitSite()
