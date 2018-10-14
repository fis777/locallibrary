''' Django views is here'''
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, BookInstance, Author

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

class BookListView(ListView):
    '''Отображение списка книг'''
    model = Book
    paginate_by = 10

class BookDetailView(DetailView):
    ''' Отображение подробной информации о книге '''
    model = Book

class AuthorListView(ListView):
    '''Отображение списка авторов'''
    model = Author

class AuthorDetailView(DetailView):
    ''' Отображение подробной информации о авторе '''
    model = Author
