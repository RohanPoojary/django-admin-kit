Form Widgets
============
    The documentation for :any:`admin_kit.widgets` module.

SelectMultipleWidget
--------------------
    :class:`MultiSelectField<admin_kit.widgets.SelectMultipleWidget>` is the widget used for Multi Select.
    It inherits :any:`Django SelectMultiple Widget<django.forms.widgets>` class.

    The widget doesnt take any new parameters. It just adds the initial value of that widget
    to ``data-kit-config`` attribute.

SelectWidget
------------
    :class:`SelectWidget<admin_kit.widgets.SelectWidget>` is the widget used for Select.
    It inherits :any:`Django Select Widget<django.forms.widgets>` class. This widget is 
    similar to :class:`MultiSelectField<admin_kit.widgets.SelectMultipleWidget>`.