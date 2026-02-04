from email.policy import default

from django import forms
from core.models import Book, Author, Genre, NavbarGenre
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator


class NewBookForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(),required=True, widget= forms.Select(attrs={'class':'form-select'}))
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(),required=True, widget = forms.SelectMultiple(attrs={'class':'form-select'}))
    file = forms.FileField(validators=[FileExtensionValidator(['pdf'])],required=True , widget=forms.FileInput(attrs={'class': 'form-control rounded-start rounded-end-0', 'id':'file'}))
    cover = forms.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],required=True, widget=forms.FileInput(attrs={'class': 'form-control rounded-start rounded-end-0', 'id':'cover'}))


    class Meta:
        model = Book
        fields = ['title', 'description', 'genre', 'author', 'cover', 'file', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded-start rounded-end-0', 'id':'title'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-start rounded-end-0', 'id':'description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'id':'price'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file.size > 50*1024*1024:
            raise ValidationError('حجم فایل نباید بیشتر از 50 مگابایت باشد')

        return file

    def clean_cover(self):
        cover = self.cleaned_data.get('cover')

        if cover.size > 5*1024*1024:
            raise ValidationError('حجم کاور نباید بیشتر از 5 مگابایت باشد')
        return cover

class NewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

        labels = {
            'name':"نام نویسنده"
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-start rounded-end-0', 'id':'name'}),
        }


class NewGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

        labels = {
            'name':"اسم ژانرا"
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-start rounded-end-0', 'id':'name'}),
        }

class NavbarForm(forms.Form):

    MAX_ITEMS = 14

    # DYNAMIC FIELD MAKING
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(1, self.MAX_ITEMS + 1):
            # Genre field
            self.fields[f'genre{i}'] = forms.ModelChoiceField(
                queryset=Genre.objects.all(),
                widget=forms.Select(attrs={'class': 'form-select rounded-start rounded-end-0'}),
                required=False,
                label= 'آیتم شماره {} نوار ناوبری'.format(i),
            )

    def clean(self):
        cleaned = super().clean()

        chosen = [
            cleaned.get(f'genre{i}')
            for i in range(1, self.MAX_ITEMS + 1)
            if cleaned.get(f'genre{i}') is not None
        ]

        if len(chosen) != len(set(chosen)):
            raise ValidationError(
                "یک ژانر نمی‌تواند در بیش از یک جایگاه باشد."
            )

        return cleaned