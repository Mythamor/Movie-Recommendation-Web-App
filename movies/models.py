from django.db import models
from django.contrib import admin


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(default=862)
    title = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    view_count = models.IntegerField(default=0)


    def __str__(self):
        """Return a formatted repr of the movie
        """
        return f"{self.title} - {', '.join(genre.name for genre in self.genres.all())}"

    def save_genres(self, genres):
        # Split genres string into a list using '|'
        genre_list = genres.split('|')
        # Create Genre objects or retrieve existing ones
        genre_objects = [Genre.objects.get_or_create(name=genre)[0] for genre in genre_list]
        # Set the genres for the movie
        self.genres.set(genre_objects)
