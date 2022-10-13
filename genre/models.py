from django.db import models
from django.urls import reverse

# Create your models here.

class Genre(models.Model):
    genre_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255,blank=True)
    genre_image = models.ImageField(upload_to='photo/genres',blank=True)

    def get_url(self):
        return reverse('books_by_genre',args=[self.slug])

    def __str__(self):
        return self.genre_name
