from django.shortcuts import render
from bookstore.models import Book
def home(request):
    books = Book.objects.all().filter(is_available=True)
    context={
        'books':books,
    }
    return render(request,'home.html',context)
