Model Fields
=============
    The documentation for :any:`admin_kit.models` module.
    Currently, the module provides only one field, new fields will be added in future releases.

MultiSelectField
----------------
    :class:`MultiSelectField<admin_kit.models.MultiSelectField>` provides Multi Selecting features. It
    internally by default stores in a ``TextField`` and the values are seperated by ``,``.

    **Parameters**

        It accepts all the :any:`django model parameters<django.db.models.fields>`. Below are the additional parameters or special
        behaviour for a parameter.

    * ``seperator``
            The default is ``,``. This value will be used as a delimiter while storing the selected values.
    
    * ``max_length``
            Default is ``null``. If this is set, then ``varchar(max_length)`` will be used for storage
            by default ``TextField`` is used for storage.

    * ``choices``
            The choices used for storage. This field is optional as the choices can be from an ajax
            class

    * ``ajax_source``
            The ``key`` name used while registering inherited :class:`admin_kit.ajax.Ajax` class.
            The return of its ``run`` method will be used as choices.

    * ``ajax_target``
            This will be of the form ``key_name:target_field``. On every change in its input, it hits
            the inherited :class:`admin_kit.ajax.Ajax` class mapped to the specified ``key_name``.
            If ``target_field`` is specified then it sets the value of specified model field to
            api's return value.

            The selected values will be passed as ``q[]`` query list parameter.

            **Example**

            .. code-block:: python
            
                # ajax.py

                import admin_kit

                class SelectedGenresAjax(admin_kit.ajax.Ajax):
                    response_type = 'text'

                    def run(self, request):
                        query = request.GET.getlist('q[]')
                        response = ','.join(query)
                        return response

                admin_kit.site.register('selected-genres', SelectedGenresAjax)

            This ajax class, joins query list ``q[]`` values with ``,`` and returns
            it in text format.

            .. code-block:: python

                # models.py

                from admin_kit.models import MultiSelectField

                class Book(models.Model):
                    name = models.CharField(max_length=100)
                    GENRES = (
                        ('thriller', 'thriller'),
                        ('sci-fi', 'sci-fi'),
                        ('fictional', 'fictional'),
                        ('fantasy', 'fantasy'),
                        ('philosophy', 'philosophy')
                    )

                    genres = MultiSelectField(verbose_name='Valid Genres', choices=GENRES,
                                              ajax_target='selected-genres:selectedValues')
                    selectedValues = models.TextField(verbose_name='Selected Values')

            Hence for every change in ``genres`` field, the selected values will be sent to ajax class
            mapped to key: ``selected-genres`` which is ``SelectedAjax`` and its return will be filled
            to ``selectedValues`` field.

            As you can notice the ``target_field`` of ``ajax_target`` parameter need not be from
            :any:`admin_kit.models` module.

    * ``ajax_subscribe``
            This parameter is paired with ``ajax_source`` parameter and is set to ``False``. If
            it is ``True``, then this field is linked to every other field with its ``ajax_source``
            value same as its linked ``ajax_target`` value.

            But it wont be linked to fields which have ``target_field`` specified in its ``ajax_target``
            parameter.

            **Example**

            .. code-block:: python

                # ajax.py

                class GenresAjax(ajax.Ajax):
                    def run(self, request):
                        query = request.GET.getlist('q[]')
                        response = list(zip(query, query))
                        return response

            This ajax class zips the selected query and returns it back.

            .. code-block:: python

                # models.py               

                class Book(models.Model):
                    ...
                    genres = MultiSelectField(verbose_name='Valid Genres', choices=GENRES,
                                            ajax_target='genres')
                    chosen_fields = MultiSelectField(seperator=',', ajax_source='genres',
                                                     ajax_subscribe=True)
            
            Here ``chosen fields`` will have choices dynamically filled whenever ``genres`` field
            is modified. And the choices for ``chosen_fields`` will be from return of the ``GenresAjax``
            class.
    
    * ``kit_config``
            This defaults to ``None``. Instead of passing ``ajax_source``, ``ajax_target`` and
            ``ajax_subscribe`` seperately, one can specify them in a dictionary and can be passed
            to this parameter.

            **Example**

            .. code-block:: python

                # models.py               

                class Book(models.Model):
                    ...
                    genres = MultiSelectField(verbose_name='Valid Genres',
                                              ajax_source='genres', ajax_subscribe=True,
                                              ajax_target='selected-genres:selectedValues')

            Is equivalent to

            .. code-block:: python

                # models.py               

                class Book(models.Model):
                    ...
                    kit_config = {
                        'ajax-source': 'genres',
                        'ajax-subscribe': True,
                        'ajax-target': 'selected-genres:selectedValues'
                    }
                    genres = MultiSelectField(verbose_name='Valid Genres', choices=GENRES,
                                              kit_config=kit_config)

            .. note::
                    
                    Make sure the *key names* are **hiphen seperated** and not *underscore* seperated.