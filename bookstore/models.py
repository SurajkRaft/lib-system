from django.db import models
from genre.models import Genre
from  django.urls import reverse
from accounts.models import Account
# Create your models here.

class Book(models.Model):
    book_title      = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    author_name     = models.CharField(max_length=200, blank=True)
    publisher_name  = models.CharField(max_length=200, blank=True)
    price           = models.IntegerField(default=1,blank=True)
    Images          = models.ImageField(upload_to='photos/books')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    genre           = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('book_detail', args=[self.genre.slug,self.slug])

    def __str__(self):
        return self.book_title

class ReviewRating(models.Model):
     books = models.ForeignKey(Book, on_delete=models.CASCADE)
     user = models.ForeignKey(Account, on_delete=models.CASCADE)
     subject = models.CharField(max_length=100,blank = True)
     review = models.TextField(max_length = 500,blank=True)
     rating = models.FloatField()
     ip = models.CharField(max_length=20, blank=True)
     status = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str(self):
         return self.subject

class VariationManager(models.Manager):
    def editions(self):
        return super(VariationManager,self).filter(variation_category='edition', is_active=True)
    def types(self):
        return super(VariationManager,self).filter(variation_category='type', is_active=True)


variation_category_choice=(
    ('edition','edition'),
    ('type','type'),
)



class Variation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    objects = VariationManager()
    def __str__(self):
        return self.variation_value


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    # user = models.ForeignKey(User, related_name="messages" ,on_delete=models.CASCADE

    def __str__(self):
        return self.message
