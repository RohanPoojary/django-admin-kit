"""
    Admin Kit Fields module

"""

import json
from django import forms
from .widgets import SelectWidget, SelectMultipleWidget

__all__ = ['BaseField', 'MultiSelectField', 'SelectField']


class BaseField(forms.Field):
    """
    The Base Field for form fields

    """

    def __init__(self, kit_config=None, ajax_source=None, default_value=None,  identifier=None, source_router=None,
                 *args, **kwargs):
        """
        kit_config :: dict
            The config map containing the parameters and their values
        ajax_source :: str
            The source value from which the values are retrieved
        """
        self.ajax_source = ajax_source
        self.identifier = identifier
        self.source_router = source_router
        self.default_value = default_value
        self.kit_config = dict()
        if kit_config:
            self.kit_config = kit_config
        super(BaseField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        """
        This will add ``data-kit-config`` attibute to the widget
        """
        attrs = super(BaseField, self).widget_attrs(widget)
        kit_config = self.kit_config.copy()

        if self.ajax_source:
            kit_config['ajax-source'] = self.ajax_source
        if self.identifier:
            kit_config['identifier'] = self.identifier
        if self.default_value:
            kit_config['default_value'] = self.default_value
        if self.source_router:
            kit_config['source_router'] = self.source_router
        attrs['data-kit-config'] = json.dumps(kit_config)

        return attrs


class MultiSelectField(BaseField):
    """
    This field is used to create MultiSelect Form fields.

    """
    widget = SelectMultipleWidget

    def __init__(self, seperator=',', choices=(), *args, **kwargs):

        self.seperator = seperator
        if 'coerce' in kwargs:
            self._coerce = kwargs.pop('coerce')
        super(MultiSelectField, self).__init__(*args, **kwargs)
        self.choices = choices or [['', '']]
        self.widget.choices = self.choices

    def prepare_value(self, value):
        value = super(MultiSelectField, self).prepare_value(value)
        if hasattr(self, '_coerce'):
            value = self._coerce(value)
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return value.split(self.seperator)
        return value

    def to_python(self, value):
        value = super(MultiSelectField, self).to_python(value)
        if isinstance(value, str):
            return list(map(str.strip, value.split(self.seperator)))
        return value


class SelectField(BaseField):
    """
    This field is used to create MultiSelect Form fields.

    """
    widget = SelectWidget

    def __init__(self, choices=(), *args, **kwargs):
        """
        Intializes SelectField
        """
        if 'coerce' in kwargs:
            kwargs.pop('coerce')
        super(SelectField, self).__init__(*args, **kwargs)
        self.choices = choices or [['', '']]
        self.widget.choices = self.choices
