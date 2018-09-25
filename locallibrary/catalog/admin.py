from django.contrib import admin
from .models import Book, Author, Genre, BookInstance, Language

# Register your models here.

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Language)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
