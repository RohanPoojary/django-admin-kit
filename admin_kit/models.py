from django.db import models as dj_models
from django.core import exceptions
from django import forms

from .import fields


class MultiSelectField(dj_models.Field):

    def __init__(self, seperator=',', *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 100)
        self.ajax_source = kwargs.pop('ajax_source', None)
        self.seperator = seperator
        super(MultiSelectField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'varchar(%s)' % self.max_length

    def deconstruct(self):
        name, path, args, kwargs = super(MultiSelectField, self).deconstruct()
        del kwargs['max_length']
        kwargs['ajax_source'] = self.ajax_source

        if self.seperator != ',':
            kwargs['seperator'] = self.seperator
        return name, path, args, kwargs

    def value_to_string(self, obj):
        # print('val-to-string:', obj)
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def from_db_value(self, value, expression, connection, context):
        # print('from-db:', value)
        # if isinstance(value, str):
        #     return value.split(self.seperator)
        return value

    def get_prep_value(self, value):
        # print('get-prep-value:', value)
        if isinstance(value, list):
            return self.seperator.join(value)
        return value

    def to_python(self, value):
        # print('to-python:', value)
        if value is None:
            return None
        if isinstance(value, str):
            return value.split(self.seperator)
        return value

    def validate(self, value, model_instance):
        pass

    def formfield(self, **kwargs):
        if not self.choices:
            self.choices.append(('', '---------'))
        defaults = {
            'seperator': self.seperator,
            'coerce': self.to_python,
            'choices': self.choices,
            'ajax_source': self.ajax_source
        }
        defaults.update(kwargs)
        return fields.MultiSelectField(**defaults)
