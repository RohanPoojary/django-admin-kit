from django.db import models
from admin_kit.models import MultiSelectField

class Book(models.Model):

    name = models.CharField(max_length=100)
    GENRES = (
        ('thriller', 'thriller'),
        ('sci-fi', 'sci-fi'),
        ('fictional', 'fictional'),
        ('fantasy', 'fantasy'),
        ('philosophy', 'philosophy')
    )

    genres = MultiSelectField(max_length=100, seperator='$', choices=GENRES)
    # genres = MultiSelectField(max_length=100, seperator='$', choices=GENRES)


    def __str__(self):
        return self.name