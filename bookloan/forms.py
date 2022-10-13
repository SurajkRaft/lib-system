
from django import forms
from .models import Bookloan


class BookloanForm(forms.ModelForm):
    class Meta:
        model = Bookloan
        fields =['first_name','last_name','phone','email','bookloan_note']
