from django.urls import path

from .import views
urlpatterns=[
   path('order_bookloan/',views.order_bookloan,name='order_bookloan'),
   path('confirm_bookloan/',views.confirm_bookloan, name='confirm_bookloan'),
   path('bookloan_order_complete/', views.bookloan_order_complete,name='bookloan_order_complete'),
   path('payments/',views.payments,name='payments'),
   path('payment_complete/',views.payment_complete,name='payment_complete'),
   
]
