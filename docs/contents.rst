Contents
========

Models
------
.. automodule:: admin_kit.models
    :members:

Fields
------
.. automodule:: admin_kit.fields
    :members:

Widgets
-------
.. automodule:: admin_kit.widgets
    :members:

Site
----
.. automodule:: admin_kit.sites
    :members:

.. method:: admin_kit.site.register(key, ajax_class)

    Registers the ``ajax_class`` for ajax behaviour. This is same as :any:`admin_kit.sites.AdminKitSite.register` method

    key :: str
        This is the *key* that will be used in models for binding
    ajax_class :: class
        The ajax class that inherits :class:`admin_kit.ajax.Ajax` 

Ajax
----
.. automodule:: admin_kit.ajax
    :members:
