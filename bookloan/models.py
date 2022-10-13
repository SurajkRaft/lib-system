from django.db import models
from accounts.models import Account
from bookstore.models import Book, Variation
from django.utils import timezone
# Create your models here.

class Bookloan(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Returned','Returned'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    bookloan_number = models.CharField(max_length=20)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    bookloan_note = models.CharField(max_length=100)
    status = models.CharField(max_length=15,choices=STATUS,default='New')
    ip=models.CharField(blank=True,max_length=20)
    is_bookloan = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    late_charge = models.IntegerField(default=False)
    actual_return_date = models.DateTimeField(null=True)
    remaining_days=models.IntegerField(default=False)
    return_date = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name

class BookloanBook(models.Model):
    bookloan = models.ForeignKey(Bookloan, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL,blank=True,null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    is_bookloan = models.BooleanField(default=False)
    bookloandone = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.book_title

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    bookloan_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.payment_id
