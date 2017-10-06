import json
from django.forms.widgets import SelectMultiple

__all__ = ['SelectMultipleWidget']

class SelectMultipleWidget(SelectMultiple):
    """
    MultiSelect Widget which inherits Django's SelectMultiple widget
    
    """

    template_name = 'admin_kit/widgets/select.html'
    option_template_name = 'admin_kit/widgets/select_option.html'

    class Media:
        css = {
            'all': ('admin_kit/css/select.css', )
        }

    def __init__(self, *args, **kwargs):
        super(SelectMultipleWidget, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'admin-kit admin-kit-select'

        kit_config = json.loads(context['widget']['attrs']['data-kit-config'])
        kit_config['init-value'] = ','.join(context['widget']['value'])
        context['widget']['attrs']['data-kit-config'] = json.dumps(kit_config)

        return context
