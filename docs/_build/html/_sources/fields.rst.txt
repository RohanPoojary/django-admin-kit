Form Fields
===========
    The documentation for :any:`admin_kit.fields` module.

MultiSelect Form Field
----------------------
    :class:`MultiSelectField<admin_kit.fields.MultiSelectField>` provides Multi Selecting features.
    It is same as :doc:`models.MultiSelectField<models>`, but is used in :any:`Django Admin Forms<django.contrib.admin>`

    **Parameters**

    * ``seperator``
            The default is ``,``. This value will be used as a delimiter while storing the selected values.

    * ``choices``
            The choices used for rendering. This field is optional as the choices can be from an ajax
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

    * ``ajax_subscribe``
            This parameter is paired with ``ajax_source`` parameter and is set to ``False``. If
            it is ``True``, then this field is linked to every other field with its ``ajax_source``
            value same as its linked ``ajax_target`` value.

            But it wont be linked to fields which have ``target_field`` specified in its ``ajax_target``
            parameter.
    
    * ``kit_config``
            This defaults to ``None``. Instead of passing ``ajax_source``, ``ajax_target`` and
            ``ajax_subscribe`` seperately, one can specify them in a dictionary and can be passed
            to this parameter.

            **Example**

            .. code-block:: python

                # admin.py

                ...
                from admin_kit.fields import MultiSelectField

                class BookForm(forms.ModelForm):
                    model = Book
                    selected_fields = MultiSelectField(ajax_source='genres', ajax_subscribe=True)
                    fields = ('name', 'genres')

                 class BookAdmin(nested_admin.NestedStackedInline):
                    model = Book
                    form = BookForm
                
            is equivalent to

            .. code-block:: python

                # admin.py

                ...
                from admin_kit.fields import MultiSelectField

                class BookForm(forms.ModelForm):
                    model = Book
                    kit_config = {
                            'ajax-source': 'genres',
                            'ajax-subscribe': True
                    }
                    selected_fields = MultiSelectField(kit_config=kit_config)
                    fields = ('name', 'genres')

                class BookAdmin(nested_admin.NestedStackedInline):
                    model = Book
                    form = BookForm

            .. note::
                
                Make sure the key names are **hiphen seperated**.


Select Form Field
-----------------
    :class:`SelectField<admin_kit.fields.SelectField>` provides Selecting features. It is similar
    to :class:`MultiSelectField<admin_kit.fields.MultiSelectField>`, but provides a single value to select.

    
    **Parameters**

    * ``choices``
           
    * ``ajax_source``
          
    * ``ajax_target``
           
    * ``ajax_subscribe``
           
    * ``kit_config``
            