Documentation
=============

.. automodule:: admin_kit
    :members:
.. automodule:: admin_kit.apps
    :members:
.. automodule:: admin_kit.ajax
    :members:
.. automodule:: admin_kit.models
    :members:
.. automodule:: admin_kit.fields
    :members:
.. automodule:: admin_kit.widgets
    :members:

.. py:function:: admin_kit.site.register(self, key, ajax_class)

    Registers the ``ajax_class`` for ajax behaviour

    key :: str
        This is the *key* that will be used in models for binding
    ajax_class :: class
        The ajax class that inherits :class:`admin_kit.ajax.Ajax` 

