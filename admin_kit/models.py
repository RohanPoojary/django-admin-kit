from django.db import models as dj_models
from django.core import exceptions
from django import forms

from . import fields

__all__ = ['BaseField', 'MultiSelectField']


class BaseField(dj_models.Field):
    """
    The Base model field of Admin-Kit models. This inherits Django's models.Field class.

    """

    def __init__(self, kit_config=None, ajax_source=None, ajax_target=None,
                 ajax_subscribe=False, *args, **kwargs):
        """
        kit_config :: dict
            The config map containing the parameters and their values
        ajax_source :: str
            The source value from which the values are retrieved
        ajax_target :: str
            The target value to which the values will be filled to
        ajax_subscribe ::  bool
            If True, then with every change in ``ajax_target``,
            it fills corresponding ``ajax_source``
        """

        self.ajax_source = ajax_source
        self.ajax_target = ajax_target
        self.ajax_subscribe = ajax_subscribe
        self.kit_config = dict()
        if kit_config:
            self.kit_config = kit_config

        super(BaseField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        """
        Deconstructs the field to a tuple of 4 elements. This is used to recreate the same
        object.
        """
        name, path, args, kwargs = super(BaseField, self).deconstruct()
        kwargs['ajax_source'] = self.ajax_source
        kwargs['ajax_target'] = self.ajax_target
        kwargs['ajax_subscribe'] = self.ajax_subscribe

        kwargs['kit_config'] = self.kit_config
        return name, path, args, kwargs

    def value_to_string(self, obj):
        """
        Converts the value of the object to a string
        """
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def from_db_value(self, value, expression, connection, context):
        """
        Returns value from the database. inherited models should override this
        """
        return value

    def validate(self, value, model_instance):
        """
        To validate the value of a model instance. Inherited models should override this
        """
        pass

    def formfield(self, form_class, choices_form_class=None, **kwargs):
        """
        Returns the form object to be used for rendering.
        """
        defaults = {
            'required': not self.blank,
            'label': self.verbose_name,
            'help_text': self.help_text,

            'ajax_source': self.ajax_source,
            'ajax_target': self.ajax_target,
            'ajax_subscribe': self.ajax_subscribe,

            'kit_config': self.kit_config
        }

        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()
        if self.choices:
            include_blank = (self.blank or
                             not (self.has_default() or 'initial' in kwargs))
            defaults['choices'] = self.get_choices(include_blank=include_blank)
            defaults['coerce'] = self.to_python
            if self.null:
                defaults['empty_value'] = None
            if choices_form_class is not None:
                form_class = choices_form_class
            else:
                form_class = form_class
        defaults.update(kwargs)
        return form_class(**defaults)


class MultiSelectField(BaseField):
    """
    The Multiselect model field of Admin-Kit, which allows users to create
    multi select ajax fields.

    """

    def __init__(self, seperator=',', *args, **kwargs):
        """
        seperator :: str
            The selected fields will be joined by ``seperator`` and stored in the database.
        """
        self.max_length = kwargs.pop('max_length', None)
        self.seperator = seperator
        super(MultiSelectField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        if self.max_length:
            return 'varchar(%s)' % self.max_length
        return 'longtext'

    def deconstruct(self):
        name, path, args, kwargs = super(MultiSelectField, self).deconstruct()
        if self.max_length:
            kwargs['max_length'] = self.max_length
        if self.seperator != ',':
            kwargs['seperator'] = self.seperator
        return name, path, args, kwargs

    def get_prep_value(self, value):
        if isinstance(value, list):
            return self.seperator.join(value)
        return value

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value.split(self.seperator)
        return value

    def formfield(self, **kwargs):
        if not self.choices:
            self.choices.append(('', '---------'))
        defaults = {
            'form_class': fields.MultiSelectField,
            'seperator': self.seperator,
            'choices': self.choices,
        }
        defaults.update(kwargs)
        return super(MultiSelectField, self).formfield(**defaults)
