from datetime import date, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    ''' Форма ввода даты возврата кнги'''
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 week (default is 3)")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > date.today() + timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        return data
