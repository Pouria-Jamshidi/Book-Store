from django.urls import path
from core.views import home, NewBook, NewAuthorView, NewGenreView, book_detail, BookScoreView, NavbarView, home_genre, home_author, download_book, Book_wishlist_cbv, search_result_fbv

urlpatterns = [
    path('', home, name='home'),
    path('genre/<int:genre_id>/', home_genre, name='home_genre'),
    path('author/<int:author_id>/', home_author, name='home_author'),
    path('search/', search_result_fbv, name='search_result'),
    path('books/newbook/', NewBook.as_view(), name='newbook'),
    path('author/new/', NewAuthorView.as_view(), name='newauthor'),
    path('genre/new/', NewGenreView.as_view(), name='newgenre'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('book/score/<int:book_id>/', BookScoreView.as_view(), name='book_score'),
    path('book/wishlist/<int:book_id>/', Book_wishlist_cbv.as_view(), name='book_wishlist'),
    path('book/download/<int:book_id>/', download_book, name='download_book'),
    path('navbar/items/', NavbarView.as_view(), name='navbar_items'),
]
