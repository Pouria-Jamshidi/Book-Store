from django.urls import path
from core.views import home, NewBook, NewAuthorView, NewGenreView, book_detail, BookScoreView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),
    path('/books/newbook/', NewBook.as_view(), name='newbook'),
    path('/author/new/',NewAuthorView.as_view(), name='newauthor'),
    path('/genre/new/',NewGenreView.as_view(), name='newgenre'),
    path('/book/<int:book_id>/', book_detail, name='book_detail'),
    path('/book/like/<int:book_id>/', BookScoreView.as_view(), name='book_score'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root= settings.MEDIA_ROOT
    )