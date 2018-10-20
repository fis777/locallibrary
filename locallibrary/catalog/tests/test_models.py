''' Tests our models '''
from django.test import TestCase
from catalog.models import Author

class AuthorModelTest(TestCase):
    ''' Tests Author model'''

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name="Doe", last_name="John")

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_author__str__(self):
        author = Author.objects.get(id=1)
        author_full_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEqual(author_full_name, str(author))

    def test_author_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')
