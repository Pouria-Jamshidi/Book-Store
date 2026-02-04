from django.urls import path
from sales.views import Add_to_cart_View, Remove_from_cart_View

urlpatterns = [
    path('cart/add/<int:book_id>',Add_to_cart_View.as_view(),name='cart_add'),
    path('cart/remove/<int:book_id>',Remove_from_cart_View.as_view(),name='cart_remove'),
]