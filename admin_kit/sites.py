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

    def js_config(self, request):
        """
        Renders the config.js file which configures global variables

        """
        from django.shortcuts import render
        base_index = request.path.rfind('js_config')
        app_url = request.path[:base_index - 1]
        enable_dup = True
        try:
            from django.conf import settings
            enable_dup = not settings.KIT_DISABLE_DUPLICATE
        except AttributeError:
            enable_dup = True
        return render(request, 'admin_kit/config.js',
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
        kwargs = {}
        kwargs["query_list"] = request.GET.getlist('q[]')
        kwargs["query"] = request.GET.get('q')
        kwargs["query_key"] = key

        if key.startswith("__"):
            key = key.lstrip("__")
            kwargs["query_key"] = key
            response = self.internal_site.route(request, **kwargs)
        else:
            response = self._registry[key].route(request, **kwargs)

        return response

    def get_urls(self):
        """
        Returns the list of urls of admin_kit

        """
        from django.conf.urls import url
        from django.conf import settings

        urlpatterns = [
            url(r'^ajax/(?P<key>.*)/', self.ajax, name='ajax'),
            url(r'js_config/', self.js_config, name='js_config')
        ]

        if settings.DEBUG or hasattr(settings, 'TEST_MODE'):
            urlpatterns += [url(r'^ping', self.ping, name='ping')]

        return urlpatterns

    @property
    def urls(self):
        """
        The actual property used by django for routing requests

        """
        return self.get_urls(), 'admin_kit', self.name


site = AdminKitSite()
