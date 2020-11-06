from django.test import TestCase
from .models import *
from admin_kit.models import generate_choices_hash

class TestModule(TestCase):

    def setUp(self):
        Book.objects.create(name="BookA", genres='thriller', main_genre='thriller')
        Book.objects.create(name="BookB", genres=['thriller', "philosophy"], main_genre='philosophy')
        Book2.objects.create(name="BookA", genres=['thriller', "philosophy"])

    def test_book(self):
        """Animals that can speak are correctly identified"""
        bookA = Book.objects.get(name="BookA")
        bookB = Book.objects.get(name="BookB")
        self.assertEqual(bookA.genres, 'thriller')
        self.assertEqual(bookA.main_genre, 'thriller')
        self.assertEqual(bookB.genres, 'thriller,philosophy')
        self.assertEqual(bookB.main_genre, 'philosophy')

    def test_consistency(self):
        choices = [('choice1', 'choice1'), ('choice2', 'choice2')]
        hash1 = generate_choices_hash(choices)
        self.assertEqual(hash1, generate_choices_hash(choices))

    def test_book2(self):
        """Animals that can speak are correctly identified"""
        bookA = Book2.objects.get(name="BookA")
        self.assertEqual(bookA.genres, 'thriller$philosophy')

