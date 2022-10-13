from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
from carts.models import CartItem
from .forms import BookloanForm
from .models import BookloanBook, Bookloan , Payment
from bookstore.models import Book
import datetime
from datetime import timedelta

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.
import json
import speech_recognition as sr


def payments(request):
    body = json.loads(request.body)
    bookloan_id = body['orderID']
    bookloan = Bookloan.objects.get(user=request.user, bookloan_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        bookloan_id = body['orderID'],
        payment_method = body['payment_method'],
        amount_paid = bookloan.late_charge,
        status = body['status'],
    )
    payment.save()
    bookloan.is_paid = True
    bookloan.actual_return_date = datetime.date.today()
    bookloan.is_returned = True
    bookloan.save()

    data = {
        'bookloan_id':bookloan_id,
        'transID':payment.payment_id,
    }
    return JsonResponse(data)

def confirm_bookloan(request):

    if request.method =='POST':
        bookloan_number= request.POST['bookloan_number']
        print(bookloan_number)
        print(request.user)
        bookloan = Bookloan.objects.get(user=request.user, is_bookloan=False, bookloan_number= bookloan_number)
        bookloan.is_bookloan = True
        bookloan.save()

        # move the cart item to the BookloanBook
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            bookloanbook =BookloanBook()
            bookloanbook.bookloan_id =bookloan.id
            bookloanbook.user_id = request.user.id
            bookloanbook.book_id = item.book_id
            bookloanbook.quantity = item.quantity
            bookloanbook.bookloandone = True
            bookloanbook.save()

            cart_item = CartItem.objects.get(id=item.id)
            book_variation = cart_item.variations.all()
            bookloanbook = BookloanBook.objects.get(id=bookloanbook.id)
            bookloanbook.variations.set(book_variation)
            bookloanbook.save()
        #Reduce the quantity of the bookd books

            book = Book.objects.get(id=item.book_id)
            book.stock -=item.quantity
            book.save()


        # clear cart
        CartItem.objects.filter(user=request.user).delete()

        # send loaned booked confirmation
        mail_subject='Thank you for your Book Loan order!'
        message=render_to_string('bookloan/order_received_email.html',{
        'user':request.user,
        'bookloan':bookloan,
        })
        to_email=request.user.email
        send_email=EmailMessage(mail_subject,message,to=[to_email])
        send_email.send()

        b_order = Bookloan.objects.get(bookloan_number=bookloan_number, is_bookloan=True)
        b_loaned_books = BookloanBook.objects.filter(bookloan_id=b_order.id)
        print(b_loaned_books)
        # send confiration page
        context ={
            'bookloanbook':bookloanbook,
            'b_loaned_books':b_loaned_books,
        }

    return render(request,'bookloan/bookloan_order_complete.html',context)




def order_bookloan(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    print(cart_items)
    # if the cart count is less than or equal to zero, the redirect back to book Store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count= cart_items.count()
    if cart_count <=0:
        return redirect('bookstore')

    if request.method =='POST':
        form = BookloanForm(request.POST)
        if form.is_valid():
            # store all information in bookloan
            data = Bookloan()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.ip = request.META.get('REMOTE_ADDR')
            data.bookloan_note = form.cleaned_data['bookloan_note']
            data.return_date=datetime.date.today()+timedelta(days=10)
            data.save()
            # generate bookloan number
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            bookloan_number = current_date + str(data.id)
            data.bookloan_number = bookloan_number
            data.save()
            bookloan = Bookloan.objects.get(user=current_user, is_bookloan=False, bookloan_number=bookloan_number)
            context={
                'bookloan':bookloan,
                'cart_items':cart_items,
            }
            return render(request,'bookloan/confirmbook.html',context)
        else:
            return redirect('checkout')


def bookloan_order_complete(request):
    return render(request, 'bookloan/bookloan_order_complete.html')


def payment_complete(request):

    bookloan_number = request.GET.get('bookloan_id')
    transID = request.GET.get('payment_id')
    context ={
        'bookloan_number':bookloan_number,
        'transID':transID,
    }
    return render(request, 'bookloan/payment_complete.html',context)
