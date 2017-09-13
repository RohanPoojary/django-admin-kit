from django.forms.widgets import SelectMultiple

BASE_JS = ('admin_kit/js/ajax.js', )

class SelectMultipleWidget(SelectMultiple):
    template_name = 'admin_kit/widgets/select.html'
    option_template_name = 'admin_kit/widgets/select_option.html'

    class Media:
        css = {
            'all': ('admin_kit/css/select.css', )
        }

        js = BASE_JS

    def __init__(self, *args, **kwargs):
        super(SelectMultipleWidget, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'admin-kit admin-kit-select'
        context['widget']['attrs']['data-ajax-value'] = ','.join(context['widget']['value'])
        return context