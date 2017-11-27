from django.db import models
from admin_kit.models import MultiSelectField

class Book(models.Model):
    name = models.CharField(max_length=20)
    GENRES_CHOICES = (
        ('thriller', 'thriller'),
        ('philosophy', 'philosophy')
    )
    genres = MultiSelectField(max_length=20, choices=GENRES_CHOICES)

class Book2(models.Model):
    name = models.CharField(max_length=20)
    GENRES_CHOICES = (
        ('thriller', 'thriller'),
        ('philosophy', 'philosophy')
    )
    genres = MultiSelectField(max_length=20, choices=GENRES_CHOICES, seperator='$')
