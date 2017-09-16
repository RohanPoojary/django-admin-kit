from django.db import models as dj_models
from django.core import exceptions
from django import forms

from . import fields

__all__ = ['BaseField', 'MultiSelectField']

class BaseField(dj_models.Field):

    def __init__(self, *args, **kwargs):
        self.ajax_source = kwargs.pop('ajax_source', None)
        self.ajax_target = kwargs.pop('ajax_target', None)
        self.ajax_subscribe = kwargs.pop('ajax_subscribe', False)

        self.kit_config = kwargs.pop('kit_config', {})

        super(BaseField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(BaseField, self).deconstruct()
        kwargs['ajax_source'] = self.ajax_source
        kwargs['ajax_target'] = self.ajax_target
        kwargs['ajax_subscribe'] = self.ajax_subscribe

        kwargs['kit_config'] = self.kit_config
        return name, path, args, kwargs

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        return value

    def to_python(self, value):
        return value

    def from_db_value(self, value, expression, connection, context):
        return value

    def validate(self, value, model_instance):
        pass

    def formfield(self, form_class, choices_form_class=None, **kwargs):
        defaults = {
            'coerce': self.to_python,
            'ajax_source': self.ajax_source,
            'ajax_target': self.ajax_target,
            'ajax_subscribe': self.ajax_subscribe,

            'kit_config': self.kit_config
        }
        defaults.update(kwargs)
        return form_class(**defaults)


class MultiSelectField(BaseField):

    def __init__(self, seperator=',', *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 100)
        self.seperator = seperator
        super(MultiSelectField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'varchar(%s)' % self.max_length

    def deconstruct(self):
        name, path, args, kwargs = super(MultiSelectField, self).deconstruct()
        del kwargs['max_length']
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
