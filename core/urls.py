from django.urls import path
from core.views import home, NewBook, NewAuthorView, NewGenreView, book_detail

urlpatterns = [
    path('', home, name='home'),
    path('/books/newbook/', NewBook.as_view(), name='newbook'),
    path('/author/new/',NewAuthorView.as_view(), name='newauthor'),
    path('/genre/new/',NewGenreView.as_view(), name='newgenre'),
    path('/book/<int:book_id>/', book_detail, name='book_detail'),
]