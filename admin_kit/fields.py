import json

from django import forms
from .widgets import SelectMultipleWidget

__all__ = ['MultiSelectField']

class MultiSelectField(forms.Field):

    def __init__(self, seperator=',', choices=[['', '']], *args, **kwargs):

        self.seperator = seperator
        self.choices = choices
        

        self.ajax_source = kwargs.pop('ajax_source', None)
        self.ajax_target = kwargs.pop('ajax_target', None)
        self.ajax_subscribe = kwargs.pop('ajax_subscribe', False)

        self.kit_config = kwargs.pop('kit_config', dict())

        self.widget = kwargs.pop('widget', SelectMultipleWidget(choices=choices))
        self.required = kwargs.pop('required', False)
        # self.widget.choices = self.choices
        self._coerce = kwargs.pop('coerce', None)

        super(MultiSelectField, self).__init__(self, *args, **kwargs)

    def prepare_value(self, value):
        if self._coerce:
            value = self._coerce(value)
        # print('field-prepare:', value)
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return value.split(self.seperator)
        return value

    def to_python(self, value):
        # print('field-to-python:', value)
        if isinstance(value, str):
            return list(map(str.strip, value.split(self.seperator)))
        return value

    def widget_attrs(self, widget):
        attrs = super(MultiSelectField, self).widget_attrs(widget)

        kit_config = self.kit_config.copy()
        
        if self.ajax_source:
            kit_config['ajax-source'] = self.ajax_source
        if self.ajax_target:
            kit_config['ajax-target'] = self.ajax_target
        if self.ajax_subscribe:
            kit_config['ajax-subscribe'] = self.ajax_subscribe
        
        attrs['data-kit-config'] = json.dumps(kit_config)

        return attrs

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        # print('field-clean:', value)
        return value
