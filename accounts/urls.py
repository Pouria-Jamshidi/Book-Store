from django.urls import path
from accounts.views import RegisterView, Login_view, logout_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login_view.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]