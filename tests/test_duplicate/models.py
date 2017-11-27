from django.db import models
from admin_kit.models import MultiSelectField

class Author(models.Model):
    name = models.CharField(max_length=30)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    GENRES_CHOICES = (
        ('thriller', 'thriller'),
        ('philosophy', 'philosophy')
    )
    genres = MultiSelectField(max_length=20, choices=GENRES_CHOICES)
