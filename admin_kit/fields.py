from django import forms
from .widgets import SelectMultipleWidget

__all__ = ['MultiSelectField']

class MultiSelectField(forms.Field):

    def __init__(self, seperator=',', choices=[['', '']], *args, **kwargs):

        self.seperator = seperator
        self.choices = choices

        self.ajax_source = kwargs.pop('ajax_source', None)
        self.ajax_target = kwargs.pop('ajax_target', None)
        ajax_subscribe = kwargs.pop('ajax_subscribe', False)

        self.widget = kwargs.pop('widget', SelectMultipleWidget(choices=choices, ajax_subscribe=ajax_subscribe))
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
        if self.ajax_source:
            attrs['data-ajax-source'] = self.ajax_source
        if self.ajax_target:
            attrs['data-ajax-target'] = self.ajax_target
        return attrs

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        # print('field-clean:', value)
        return value