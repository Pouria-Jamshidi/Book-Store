from django.urls import path
from sales.views import Add_to_cart_View, Remove_from_cart_View, Cart_View, Increase_credit, send_to_payment, Temp_purchase

urlpatterns = [
    path('cart/add/<int:book_id>',Add_to_cart_View.as_view(),name='cart_add'),
    path('cart/remove/<int:book_id>',Remove_from_cart_View.as_view(),name='cart_remove'),
    path('cart/view/', Cart_View.as_view(),name='cart_view'),
    path('user/credit_increase/', Increase_credit.as_view(),name='credit_increase'),
    path('checkout/', send_to_payment, name='send_to_payment'),
    path('payment/', Temp_purchase.as_view(), name='payment'),
]