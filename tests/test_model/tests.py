from django.test import TestCase
from .models import *

class TestModule(TestCase):

    def setUp(self):
        Book.objects.create(name="BookA", genres='thriller')
        Book.objects.create(name="BookB", genres=['thriller', "philosophy"])
        Book2.objects.create(name="BookA", genres=['thriller', "philosophy"])

    def test_book(self):
        """Animals that can speak are correctly identified"""
        bookA = Book.objects.get(name="BookA")
        bookB = Book.objects.get(name="BookB")
        self.assertEqual(bookA.genres, 'thriller')
        self.assertEqual(bookB.genres, 'thriller,philosophy')


    def test_book2(self):
        """Animals that can speak are correctly identified"""
        bookA = Book2.objects.get(name="BookA")
        self.assertEqual(bookA.genres, 'thriller$philosophy')
