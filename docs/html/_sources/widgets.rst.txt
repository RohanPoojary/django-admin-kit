Form Widgets
============
    The documentation for :any:`admin_kit.widgets` module.

SelectMultipleWidget
--------------------
    :class:`MultiSelectField<admin_kit.widgets.SelectMultipleWidget>` is the widget used for Multi Select.
    It inherits :any:`Django SelectMultiple Widget<django.forms.widgets>` class.

    The widget doesnt take any new parameters. It just adds the initial value of that widget
    to ``data-kit-config`` attribute.