from django.urls import path

from .import views
urlpatterns=[
   path('register/',views.register,name='register'),
   path('login/',views.login,name='login'),
   path('logout/',views.logout,name='logout'),
   path('dashboard/',views.dashboard,name='dashboard'),
   path('',views.dashboard,name='dashboard'),
   path('activate/<uidb64>/<token>/',views.activate,name='activate'),
   path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
   path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
   path('resetPassword/',views.resetPassword,name='resetPassword'),

   path('edit_profile/',views.edit_profile,name='edit_profile'),
   path('change_password/',views.change_password,name='change_password'),
   path('view_profile/',views.view_profile,name='view_profile'),

   path('my_books_ordered/',views.my_books_ordered,name='my_books_ordered'),
   path('my_books_ordered_details/<int:bookloan_number>/',views.my_books_ordered_details,name='my_books_ordered_details'),
   path('my_books_returned/',views.my_books_returned,name='my_books_returned'),
   path('my_books_returned_transaction/',views.my_books_returned_transaction,name='my_books_returned_transaction'),
   path('return_book/<int:bookloan_number>/',views.return_book,name='return_book'),



]
