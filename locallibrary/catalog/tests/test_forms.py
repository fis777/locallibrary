import datetime
from django.test import TestCase
from catalog.forms import RenewBookForm

class RenewBookFormTest(TestCase):
    ''' тесты формы ввода даты возврата книги'''

    def test_renewal_date_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 week (default is 3)')

    def test_renewal_date_is_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renewal_date_is_far_ahead(self):
        date = datetime.date.today() + datetime.timedelta(weeks=5)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renewal_date_is_today(self):
        date = datetime.date.today()
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_renewal_date_is_three_week(self):
        date = datetime.date.today() + datetime.timedelta(weeks=3)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())
