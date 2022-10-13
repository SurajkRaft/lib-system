from django.contrib import admin
from .models import Book, ReviewRating, Variation
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display    = ('book_title', 'author_name', 'publisher_name', 'genre', 'stock','modified_date', 'is_available')
    prepopulated_fields = {'slug':('book_title',)}
class VariationAdmin(admin.ModelAdmin):
    list_display = ('book','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter =('book','variation_category','variation_value')

admin.site.register(Book, BookAdmin)
admin.site.register(ReviewRating)
admin.site.register(Variation, VariationAdmin)
