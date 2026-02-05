from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from core.models import Book
from sales.models import Order,OrderItems,StatusChoices
from sales.services import update_cart_cache

class Add_to_cart_View(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request,book_id):
        book = get_object_or_404(Book,pk=book_id)
        next_url = request.GET.get('next') or 'book_detail' # So we can go back to the previous page

        # ================================== Checking to see if we already ordered this book before ====================================
        already_purchased = OrderItems.objects.filter(
            order__user=request.user,
            order__status=StatusChoices.PAID,
            book=book
        ).exists()

        if already_purchased:
            messages.info(request, 'شما قبلاً این کتاب را خریداری کرده‌اید.')
            return redirect(next_url,pk=book_id)
        # ==============================================================================================================================

        order, orderCreated = Order.objects.get_or_create(
            user=request.user,
            status= StatusChoices.PENDING,
            defaults={'total':0}
        )

        item,itemCreated = OrderItems.objects.get_or_create(
            order = order,
            book = book,
            defaults={'price':book.price ,'quantity':1}
        )

        if not itemCreated:
            messages.warning(request, 'این کتاب قبلا به سبد خرید شما اضافه شده')

        # ================================================= re-calculating the total =================================================
        order.total = sum(item.price*item.quantity for item in order.items.all())
        order.save()
        # ============================================================================================================================
        # ========================================== updating the number of items in cart ============================================
        update_cart_cache(request)
        # ============================================================================================================================

        return redirect(next_url,pk=book_id)

class Remove_from_cart_View(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        next_url = request.GET.get('next') or 'book_detail'

        # ============================== Check existing validation before deleting =================================================
        order = Order.objects.filter(
            user=request.user,
            status=StatusChoices.PENDING
        ).first()

        if not order:
            messages.warning(request, 'سبد خرید شما خالی است.')
            return redirect(next_url, pk=book_id)

        item = OrderItems.objects.filter(
            order=order,
            book=book
        ).first()

        if not item:
            messages.warning(request, 'این کتاب در سبد خرید شما وجود ندارد.')
            return redirect(next_url, pk=book_id)
        # ===========================================================================================================================

        item.delete()

        # ================================================= re-calculating the total =================================================
        order.total = sum(item.price * item.quantity for item in order.items.all())
        # ===========================================================================================================================

        # ======================= delete order if deleting it from cart empties the order else save it ===============================
        if order.total == 0:
            order.delete()
        else:
            order.save()
        messages.success(request, 'کتاب از سبد خرید حذف شد.')

        # ========================================== updating the number of items in cart ============================================
        update_cart_cache(request)
        # ============================================================================================================================
        return redirect(next_url, pk=book_id)


class Cart_View(LoginRequiredMixin, View):

    def get(self,request):
        order = Order.objects.filter(user=request.user,status=StatusChoices.PENDING).first()
        items = OrderItems.objects.filter(order=order).all()
        total_sum = 0
        for item in items:
            total_sum += item.price*item.quantity

        context = {'order':order,'items':items,'total_sum':total_sum}

        return render(request,'sales/cart_view.html', context)
