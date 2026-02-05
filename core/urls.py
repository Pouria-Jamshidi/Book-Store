from django.urls import path
from core.views import home, NewBook, NewAuthorView, NewGenreView, book_detail, BookScoreView, NavbarView, home_genre

urlpatterns = [
    path('', home, name='home'),
    path('genre/<int:genre_id>/', home_genre, name='home_genre'),
    path('books/newbook/', NewBook.as_view(), name='newbook'),
    path('author/new/',NewAuthorView.as_view(), name='newauthor'),
    path('genre/new/',NewGenreView.as_view(), name='newgenre'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('book/like/<int:book_id>/', BookScoreView.as_view(), name='book_score'),
    path('navbar/items/', NavbarView.as_view(), name='navbar_items'),
]