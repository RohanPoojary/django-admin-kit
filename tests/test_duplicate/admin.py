from django.contrib import admin
from .models import Author, Book

class BookAdmin(admin.StackedInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    model = Author
    inlines = [BookAdmin]

admin.site.register(Author, AuthorAdmin)