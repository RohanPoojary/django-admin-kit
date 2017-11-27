"""
    Admin Kit Sites module

"""

from weakref import WeakSet

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
        """
        Ping method is used to ping admin_kit ajax

        """
        from django.shortcuts import render
        return render(request, 'admin_kit/ping.html')

    def base_js(self, request):
        """
        Renders the base.js file that handles ajax calls

        """
        from django.shortcuts import render
        base_index = request.path.rfind('base.js')
        app_url = request.path[:base_index-1]
        enable_dup = True
        try:
            from django.conf import settings
            enable_dup = not settings.KIT_DISABLE_DUPLICATE
        except AttributeError:
            enable_dup = True
        return render(request, 'admin_kit/base.js',
                      context={"app": app_url, "duplicate": enable_dup},
                      content_type="text/javascript")

    def register(self, key, ajax_class):
        """
        Registers the ``ajax_class`` for ajax behaviour

        key :: str
            This is the *key* that will be used in models for binding
        ajax_class :: class
            The ajax class that inherits :class:`admin_kit.ajax.Ajax`

        """
        key = ajax_class.generate_key(key)
        self._registry[key] = ajax_class()

    def ajax(self, request, key):
        """
        Calls route method

        """
        response = self._registry[key].route(request)
        return response

    def get_urls(self):
        """
        Returns the list of urls of admin_kit

        """
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
        """
        The actual property used by django for routing requests

        """
        return self.get_urls(), 'admin_kit', self.name

site = AdminKitSite()
