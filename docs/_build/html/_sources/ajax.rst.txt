Ajax Module
===========
    The documentation for :any:`admin_kit.ajax` module. The module has only one class
    :class:`Ajax<admin_kit.ajax.Ajax>`. So we will go through its attributes
    , methods and their functionality.


Attributes
----------

* .. py:attribute:: response_type

    The response type of the ajax class. Its defaults to ``json``, where its jsonifies the 
    output python object. It also accepts ``text`` where it converts the output to a string
    and is sent as the response.

* .. py:attribute:: unique

    It defaults to ``False``, if its ``True`` then the key will be unique to a class.
    Hence different Ajax classes with the same key can be registered.

Methods
-------

* .. py:function:: run(self, request)
   
    The main method that will be executed for generating response for an Ajax request.
    This is method should be overided by the child class.

.. note::

    The remainder methods are **internal**. So should be overrided only if necessary.
    
* .. py:function:: format_response(self, output)

    This method formats the return value of :any:`run` method based on ``response_type`` attribute.
    If it is ``json``, then it converts the output to json, else it renders it in ``text`` format.

* .. py:function:: route(self, request)

    This is the core function, that calls :any:`run` method and then passes the output to
    :any:`format_response` method and returns it. This method is executed when the
    :any:`admin_kit site<admin_kit.sites.AdminKitSite>` figures out the ``ajax_class`` based on the request.

* .. py:classmethod:: generate_key(cls, key)

    Generates the key based on the configuration of Ajax Class. If the ``unique`` attribute is set
    , it prepends the ``key`` with the slug form of its class name.

    This method is called in the :any:`register<admin_kit.site.register>` function for ``key`` and 
    ``ajax_class`` mapping.

    **Example**

    .. code-block:: python

        # ajax.py

        from admin_kit import ajax

        class TestAjax(ajax.Ajax):
            ...
        
        class UniqueTestAjax(ajax.Ajax):
            unique = True
            ...

        TestAjax.generate_key('key')
        # `key`

        UniqueTestAjax.generate_key('key')
        # `unique-test-ajax-key`

    To access this Ajax class in ``models``, Its slugged key name has to be used. In the above Example
    to map to  ``UniqueTestAjax`` class, ``unique-test-ajax-key`` key should be used in ``models``
    file.

