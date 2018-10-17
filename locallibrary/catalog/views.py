''' Django views is here'''
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book, BookInstance, Author

def index(request):
    ''' Отображение главной страницы '''
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a')
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_visits': num_visits})

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

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    '''Generic class based view listing book on loan current user'''
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedBooksListView(PermissionRequiredMixin, ListView):
    permission_required = "catalog.can_mark_returned"
    model = BookInstance
    template_name = 'catalog/bookinstance_list_loaned_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
