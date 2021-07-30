"""
    Admin Kit Widgets module

"""

import json
from django.forms.widgets import SelectMultiple, Select

__all__ = ['SelectMultipleWidget', 'SelectWidget']


class SelectMultipleWidget(SelectMultiple):
    """
    MultiSelect Widget which inherits Django's SelectMultiple widget

    """

    template_name = 'admin_kit/widgets/select.html'
    option_template_name = 'admin_kit/widgets/select_option.html'

    class Media:
        """
        This class adds css required for admin_kit's widget

        """
        css = {
            'all': ('admin_kit/css/select.css',)
        }

    def get_context(self, name, value, attrs):
        """
        Adds appropriate attributes to widget context
        """
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'admin-kit admin-kit-select'

        kit_config = json.loads(context['widget']['attrs']['data-kit-config'])
        kit_config['init-value'] = ','.join(context['widget']['value'])
        context['widget']['attrs']['data-kit-config'] = json.dumps(kit_config)

        return context


class SelectWidget(Select):
    """
    MultiSelect Widget which inherits Django's Select widget

    """

    def get_context(self, name, value, attrs):
        """
        Adds appropriate attributes to widget context
        """
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'admin-kit admin-kit-select'
        kit_config = json.loads(context['widget']['attrs']['data-kit-config'])
        kit_config['init-value'] = ','.join(context['widget']['value'])
        context['widget']['attrs']['data-kit-config'] = json.dumps(kit_config)
        return context
