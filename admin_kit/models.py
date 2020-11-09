"""
    Admin Kit Models module

"""

from django.db import models as dj_models
import base64
from .sites import AdminKitSite

from . import fields
from .sites import site

__all__ = ['BaseField', 'MultiSelectField', 'SelectField']

def generate_choices_hash(choices):
    base64_encode = base64.b64encode(str(list(choices)).encode("utf8"))
    decode_message = base64_encode.decode("ascii") 
    if len(decode_message) > 50:
        mid = int(len(decode_message) / 2)
        decode_message = decode_message[mid-25:mid+25]
    return decode_message


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
        if kwargs.get("choices", None) and not ajax_source:
            hash_key = generate_choices_hash(kwargs["choices"])
            ajax_source = "__" + hash_key
            site.set_choice(hash_key, kwargs["choices"])
            kwargs.pop("choices")

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

    def from_db_value(self, value, *args, **kwargs):
        """
        Returns value from the database. inherited models should override this
        """
        return value

    def validate(self, value, model_instance):
        """
        To validate the value of a model instance. Inherited models should override this
        """
        pass

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
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

    choices = [('', '---------')]


    def __init__(self, seperator=',', *args, **kwargs):
        """
        seperator :: str
            The selected fields will be joined by ``seperator`` and stored in the database.
        """
        self.max_length = kwargs.pop('max_length', None)
        self.seperator = seperator
        super(MultiSelectField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        """
        Sets `db_type` to either varchar or longtext depending on `max_length`
        """
        if self.max_length:
            return 'varchar(%s)' % self.max_length
        return 'longtext'

    def deconstruct(self):
        """
        Deconstructs MultiSelect Field
        """
        name, path, args, kwargs = super(MultiSelectField, self).deconstruct()
        if self.max_length:
            kwargs['max_length'] = self.max_length
        if self.seperator != ',':
            kwargs['seperator'] = self.seperator
        return name, path, args, kwargs

    def get_internal_type(self):
        return "SelectField"

    def get_prep_value(self, value):
        """
        Converts value to a string
        """
        if isinstance(value, list):
            return self.seperator.join(value)
        return value

    def value_to_string(self, obj):
        """
        Return a string value of this field from the passed obj.
        This is used by the serialization framework.
        """
        return str(self.value_from_object(obj))

    def to_python(self, value):
        """
        Converts the string value to a list
        """
        if value is None:
            return None
        if isinstance(value, list):
            return value
        return value.split(self.seperator)

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        """
        Sets form to be used for rendering
        """
        defaults = {
            'form_class': form_class or fields.MultiSelectField,
            'choices_form_class': choices_form_class or fields.MultiSelectField,
            'seperator': self.seperator,
            'choices': self.choices,
        }
        defaults.update(kwargs)
        return super(MultiSelectField, self).formfield(**defaults)


class SelectField(BaseField):
    """
    The Select model field of Admin-Kit, which allows users to create
    select ajax fields.

    """
    choices = [('', '---------')]

    def __init__(self, *args, **kwargs):
        """
        Initializes SelectField
        """
        self.max_length = kwargs.pop('max_length', None)
        super(SelectField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        """
        Sets `db_type` to either varchar or longtext depending on `max_length`
        """
        if self.max_length:
            return 'varchar(%s)' % self.max_length
        return 'longtext'

    def get_internal_type(self):
        return "SelectField"

    def deconstruct(self):
        """
        Deconstructs SelectField
        """
        name, path, args, kwargs = super(SelectField, self).deconstruct()
        if self.max_length:
            kwargs['max_length'] = self.max_length
        return name, path, args, kwargs

    def value_to_string(self, obj):
        """
        Return a string value of this field from the passed obj.
        This is used by the serialization framework.
        """
        return str(self.value_from_object(obj))

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        """
        Sets form to be used for rendering
        """
        defaults = {
            'form_class': form_class or fields.SelectField,
            'choices_form_class': choices_form_class or fields.SelectField,
            'choices': self.choices,
            'initial': 'initial',
        }
        defaults.update(kwargs)
        return super(SelectField, self).formfield(**defaults)
