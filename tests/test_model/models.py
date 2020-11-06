from django.db import models
from admin_kit.models import MultiSelectField, SelectField

class Book(models.Model):
    name = models.CharField(max_length=20)
    GENRES_CHOICES = (
        ('thriller', 'thriller'),
        ('philosophy', 'philosophy')
    )
    main_genre = SelectField(choices=GENRES_CHOICES)
    genres = MultiSelectField(max_length=20, choices=GENRES_CHOICES)


class Book2(models.Model):
    name = models.CharField(max_length=20)
    GENRES_CHOICES = (
        ('thriller', 'thriller'),
        ('philosophy', 'philosophy')
    )
    genres = MultiSelectField(choices=GENRES_CHOICES, seperator='$')
