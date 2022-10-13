from django.urls import path

from .import views
urlpatterns=[
   path('',views.bookstore,name='bookstore'),
   path('genre/<slug:genre_slug>/',views.bookstore,name='books_by_genre'),
   path('genre/<slug:genre_slug>/<slug:book_slug>/',views.book_detail,name='book_detail'),
   path('search/',views.search,name='search'),
   path('submit_review/<int:book_id>/',views.submit_review,name='submit_review'),
   path('upload/', views.upload, name='upload'),
]
