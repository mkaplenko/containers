__author__ = 'mkaplenko'

from wtforms.widgets import TextInput
from wtforms.widgets.core import HTMLString


class DatePicker(TextInput):
    def __init__(self, input_type=None, date_format='YYYY-MM-DD'):
        super(DatePicker, self).__init__(input_type)
        self.date_format = date_format

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        return HTMLString('<input %s data-uk-datepicker="{format:\'YYYY-MM-DD\'}">' % self.html_params(name=field.name, **kwargs))
