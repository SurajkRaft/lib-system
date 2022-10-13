from django.shortcuts import render, redirect, get_object_or_404
from bookstore.models import Book , Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, book_id):
    current_user = request.user
    book= Book.objects.get(id=book_id)
    # if user is_authenticated
    if current_user.is_authenticated:
        book_variation = []
        if request.method =='POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(book=book,variation_category__iexact=key, variation_value__iexact=value)
                    book_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(book=book, user=current_user).exists()
        if is_cart_item_exists:
            cart_item =CartItem.objects.filter(book=book, user=current_user)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variations =  item.variations.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

            if book_variation in ex_var_list:
                index=ex_var_list.index(book_variation)
                item_id = id[index]
                item = CartItem.objects.get(book=book,id=item_id)
                item.quantity+=1
                item.save()

            else:
                item = CartItem.objects.create(book=book,quantity=1,user=current_user)
                if len(book_variation)>0:
                    item.variations.clear()
                    item.variations.add(*book_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                book=book,
                quantity=1,
                user = current_user,
            )
            if len(book_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*book_variation)
            cart_item.save()
        return redirect('cart')
   # if user not authenticated
    else:
        book_variation = []
        if request.method =='POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(book=book,variation_category__iexact=key, variation_value__iexact=value)
                    book_variation.append(variation)
                except:
                    pass

        try:
            # get the cart  using cart id  present in the session
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
            cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(book=book, cart=cart).exists()
        if is_cart_item_exists:
            cart_item =CartItem.objects.filter(book=book, cart=cart)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variations =  item.variations.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)
            print(ex_var_list)
            print(id)

            if book_variation in ex_var_list:
                index=ex_var_list.index(book_variation)
                item_id = id[index]
                item = CartItem.objects.get(book=book,id=item_id)
                item.quantity+=1
                item.save()

            else:
                item = CartItem.objects.create(book=book,quantity=1,cart=cart)
                if len(book_variation)>0:
                    item.variations.clear()
                    item.variations.add(*book_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                book=book,
                quantity=1,
                cart = cart,
            )
            if len(book_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*book_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request,book_id,cart_item_id):

    book = get_object_or_404(Book, id=book_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(book=book, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(book=book, cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,book_id,cart_item_id):
    book = get_object_or_404(Book,id=book_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(book=book,user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(book=book,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items = None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart= Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.book.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quanity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'bookstores/cart.html',context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        #cart= Cart.objects.get(cart_id = _cart_id(request))
        #cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart= Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.book.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass

    context={
        'total' : total,
        'quanity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request,'bookstores/checkout.html',context)
