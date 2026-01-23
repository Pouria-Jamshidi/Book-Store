from django import forms

from BookStore.settings import BASE_DIR
from core.models import Book


class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'genre', 'author', 'cover', 'file', 'price']
        widgets = {
        #     widgets need to be filled
        }

