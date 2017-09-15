from django.test import TestCase
from .models import Book

class MultiSelectTestCase(TestCase):
    def setUp(self):
        Book.objects.create(name='The Dummy Book', genres=['thriller', 'fantasy'])

    def test_model_creation(self):
        book = Book.objects.get()
        self.assertEqual(book.name, 'The Dummy Book')
        self.assertEqual(book.genres, 'thriller$fantasy')