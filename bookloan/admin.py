from django.contrib import admin

from .models import Bookloan, BookloanBook , Payment
# Register your models here.

class BookloanBookInline(admin.TabularInline):
    model = BookloanBook
    readonly_fields = ('user','book','quantity','bookloandone')
    extra= 0

class BookloanAdmin(admin.ModelAdmin):
    list_display    =   ['bookloan_number','full_name', 'phone','email','is_bookloan', 'created_at','status','return_date']
    list_filter = ['status','is_bookloan']
    search_fields = ['bookloan_number','first_name','last_name','phone','email']
    list_per_page = 20
    inlines = [BookloanBookInline]


admin.site.register(Bookloan,BookloanAdmin)
admin.site.register(BookloanBook)
admin.site.register(Payment)
