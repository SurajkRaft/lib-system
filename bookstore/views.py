from django.shortcuts import render , get_object_or_404, redirect
from .models import Book, ReviewRating
from genre.models import Genre
from django.core.paginator  import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse ,JsonResponse
from django.db.models import Q
from django.contrib import messages

from .forms import ReviewForm
from carts.models import CartItem
from carts.views import _cart_id


# imports for voice
import os
from .models import Chat
import speech_recognition as sr

# Create your views here.
def bookstore(request, genre_slug=None):
    genres = None
    books =None
    if genre_slug !=None:
        genres = get_object_or_404(Genre, slug = genre_slug)
        books = Book.objects.filter(genre = genres, is_available=True)
        paginator = Paginator(books,2)
        page = request.GET.get('page')
        paged_books = paginator.get_page(page)
        book_count = books.count()
    else:
        books = Book.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(books,3)
        page = request.GET.get('page')
        paged_books = paginator.get_page(page)
        book_count = books.count()
    context={
        'books':paged_books,
        'book_count':book_count,
    }

    return render(request,'bookstores/bookstore.html',context)

def book_detail(request, genre_slug, book_slug):
    try:
        single_book = Book.objects.get(genre__slug=genre_slug, slug=book_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), book=single_book).exists()

    except Exception as e:
        raise e
    context={
        'single_book':single_book,
        'in_cart':in_cart,

    }
    return render(request,'bookstores/book_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            books = Book.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(book_title__icontains=keyword) |Q(author_name__icontains=keyword)|Q(publisher_name__icontains=keyword))
            if 'keyword' in request.GET and request.GET['keyword']:
                page = request.GET.get('page')
                keyword = request.GET['keyword']
                paginator = Paginator(books,2)
            paged_books = paginator.get_page(page)
            book_count = books.count()
            context ={
            'books':paged_books,
            'book_count':book_count,
            'keyword': keyword,
             }
    return render(request,'bookstores/bookstore.html',context)

def submit_review(request, book_id):
    url = request.META.get('HTTP_REFERER')
    if request.method=='POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,books__id=book_id)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you! your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.book_id=book_id
                data.user_id=request.user
                data.save()
                messages.success(request,'Thank you ! Your review has been submitted.')
                return redirect(url)

def upload(request):
    customHeader = request.META['HTTP_MYCUSTOMHEADER']
    filename = str(Chat.objects.count())
    filename = filename + "name" + ".wav"
    uploadedFile = open(filename, "wb")
    # the actual file is in request.body
    uploadedFile.write(request.body)
    uploadedFile.close()
    r = sr.Recognizer()
    harvard = sr.AudioFile(filename)
    with harvard as source:
        audio = r.record(source)
    msg = r.recognize_google(audio)
    os.remove(filename)
    keyword = msg
    data = {
        'search_value':keyword,
        }
    return JsonResponse(data)
