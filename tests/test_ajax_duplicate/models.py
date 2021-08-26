from django.db import models

from admin_kit.models import MultiSelectField, SelectField

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    GENRES = (
        ('thriller', 'thriller'),
        ('sci-fi', 'sci-fi'),
        ('fictional', 'fictional'),
        ('fantasy', 'fantasy'),
        ('philosophy', 'philosophy')
        )
    genres = MultiSelectField(verbose_name='Valid Genres', choices=GENRES,
                              kit_config={'identifier': 'id_genres'})
    filteredGenresConfig = {
        'source_router': 'genres-ajax-genres',
        'ajax-source': 'id_genres',
    }
    filteredGenres = SelectField(kit_config=filteredGenresConfig, blank=True)

    def __str__(self):
        return self.name
