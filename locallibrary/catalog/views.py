from django.shortcuts import render
from django.db.models import Manager
from .models import Book, BookInstance, Author, Genre

class objects(Manager):
    pass

# Create your views here.
def index(request):
    ''' Отображение главной страницы '''
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a')
    num_authors = Author.objects.count()

    return render(request, 'index.html', 
                    context={'num_books': num_books,
                            'num_instances': num_instances,
                            'num_instances_available': num_instances_available,
                            'num_authors': num_authors})

