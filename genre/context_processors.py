# this is python function, it takes request as an argument and return the disctionary of data as a context
from .models import Genre

def menu_links(request):
    links = Genre.objects.all()
    return dict(links=links)
