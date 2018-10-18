''' Django views is here'''
from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from .models import Book, BookInstance, Author
from .forms import RenewBookForm

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

@permission_required("catalog.can_mark_returned")
def renew_book_librarian(request, pk):
    ''' Форма для ввода даты возврата книги'''
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method =='POST':
        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = date.today() + timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    return render(request, 'catalog/book_renew_librarian.html', context={'form': form, 'book_inst': book_inst})

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
