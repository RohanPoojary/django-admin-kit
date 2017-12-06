from django.contrib import admin
from django import forms
import nested_admin 

from .models import Author, Book
# Register your models here.

class BookForm(forms.ModelForm):
    description = forms.CharField()

    class Meta:
        model = Book
        fields = '__all__'


class BookAdmin(nested_admin.NestedStackedInline):
    model = Book
    extra = 0
    form = BookForm

class AuthorAdmin(nested_admin.NestedModelAdmin):
    model = Author
    inlines = [BookAdmin]


admin.site.register(Author, AuthorAdmin)
