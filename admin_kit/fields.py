import json

from django import forms
from .widgets import SelectMultipleWidget

__all__ = ['MultiSelectField']

class BaseField(forms.Field):
    """
    The Base Field for form fields
    """

    def __init__(self, *args, **kwargs):

        self.ajax_source = kwargs.pop('ajax_source', None)
        self.ajax_target = kwargs.pop('ajax_target', None)
        self.ajax_subscribe = kwargs.pop('ajax_subscribe', False)

        self.kit_config = kwargs.pop('kit_config', dict())
        super(BaseField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(BaseField, self).widget_attrs(widget)
        kit_config = self.kit_config.copy()

        if self.ajax_source:
            kit_config['ajax-source'] = self.ajax_source
        if self.ajax_target:
            kit_config['ajax-target'] = self.ajax_target
        if self.ajax_subscribe:
            kit_config['ajax-subscribe'] = self.ajax_subscribe

        attrs['data-kit-config'] = json.dumps(kit_config)

        return attrs


class MultiSelectField(BaseField):
    """
    This field is used to create MultiSelect Form fields.

    """
    widget = SelectMultipleWidget

    def __init__(self, seperator=',', choices=(), *args, **kwargs):

        self.seperator = seperator
        self._coerce = kwargs.pop('coerce', None)
        super(MultiSelectField, self).__init__(*args, **kwargs)
        self.choices = choices or [['', '']]
        self.widget.choices = self.choices


    def prepare_value(self, value):
        value = super(MultiSelectField, self).prepare_value(value)
        if self._coerce:
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
