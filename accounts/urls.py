


from django.urls import path
from accounts.views import RegisterView, Login_view, logout_view, profile_fbv, profile_books_fbv, \
    profile_scored_books_fbv, profile_not_scored_books_fbv, profile_orders_fbv, profile_order_items_fbv

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login_view.as_view(), name='login'),
    path('logout/', logout_view.as_view(), name='logout'),
    path('profile/', profile_fbv, name='profile'),
    path('profile/books/', profile_books_fbv, name='profile-books'),
    path('profile/books/scored/', profile_scored_books_fbv, name='profile-books-scored'),
    path('profile/books/not_scored/',profile_not_scored_books_fbv, name='profile-books-not-scored'),
    path('profile/orders/',profile_orders_fbv, name='profile-orders'),
    path('profile/order/<int:order_id>/',profile_order_items_fbv, name='profile-order-items'),
]