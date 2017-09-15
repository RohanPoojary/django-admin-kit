from django.contrib import admin
from .models import Author, Book

class BookAdmin(admin.StackedInline):
    model = Book
    extra = 0

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author
    inlines = [BookAdmin]