from django.contrib import admin
from .models import Genre
# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('genre_name',)}
    list_display = ('genre_name','slug')
admin.site.register(Genre,GenreAdmin)
