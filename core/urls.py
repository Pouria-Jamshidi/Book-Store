from django.urls import path
from core.views import home, NewBook, book_detail

urlpatterns = [
    path('', home, name='home'),
    path('/books/newbook/', NewBook.as_view(), name='newbook'),
    path('/book/<int:book_id>/', book_detail, name='book_detail'),
]