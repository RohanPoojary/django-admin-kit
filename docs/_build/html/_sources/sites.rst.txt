Sites Module
============
    The documentation of :any:`admin_kit.sites` module. The module has only class
    :class:`AdminKitSite<admin_kit.sites.AdminKitSite>` which is the root site of the app.

    This site object is aliased to ``admin_kit.site``. So it can accessed through the same

Site Methods
------------

* .. py:function:: register(key, ajax_class)

    key :: str
        This is the *key* that will be used in models for binding
    ajax_class :: class
        The ajax class that inherits :class:`admin_kit.ajax.Ajax` 

    This method is used to bind an ``ajax_class`` to a ``key``.

    .. note::

        If ``unique`` attribute of ``ajax_class`` is ``True``, remember to prepend its slugname
        to the ``key``.

