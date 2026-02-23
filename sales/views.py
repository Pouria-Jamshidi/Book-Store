
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db import transaction
from django.db.models import Value, F, Sum, ExpressionWrapper, DecimalField
from django.db.models.functions import Greatest
from core.models import Book
from sales.models import Order,OrderItems,StatusChoices
from sales.services import update_cart_cache
from sales.forms import Increase_user_credit, PaymentForm

User = get_user_model()
class Add_to_cart_View(LoginRequiredMixin, View):
    """
    CBV: Adds books to the shopping cart\n
    - user has to be logged in
    - Checks to see if we already have it in shopping cart or have bought it before
    - Recalculate total of the order after each addition
    - updates the number of items in shopping cart (session value) after each addition
    """
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
        # order.total = sum(item.price*item.quantity for item in order.items.all())
        order.total = OrderItems.objects.filter(order=order).aggregate(total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField(max_digits=10, decimal_places=0))))['total'] or 0
        order.save()
        # ============================================================================================================================
        # ========================================== updating the number of items in cart ============================================
        update_cart_cache(request)
        # ============================================================================================================================

        return redirect(next_url,pk=book_id)

class Remove_from_cart_View(LoginRequiredMixin, View):
    """
    CBV: Removes a book from the shopping cart\n
    - user has to be logged in
    - Checks to see if we have a shopping cart, and if we do, does it exist in it?
    - Recalculate total of the order after each removing
    - updates the number of items in shopping cart (session value) after each removing
    """

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
        # order.total = sum(item.price * item.quantity for item in order.items.all())
        order.total = OrderItems.objects.filter(order=order).aggregate(total = Sum(ExpressionWrapper(F('price')*F('quantity'),output_field=DecimalField(max_digits=10, decimal_places=0))))['total'] or 0
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
    """
    CBV: Renders a page that shows our shopping cart\n
    - user has to be logged in
    """

    def get(self,request):
        order = Order.objects.filter(user=request.user,status=StatusChoices.PENDING).first()
        items = OrderItems.objects.filter(order=order).all()

        context = {'order':order,'items':items}

        return render(request,'sales/cart_view.html', context)

class Increase_credit(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    CBV: Adds credit to the desired user\n
    - user performing the task has to be a superuser
    """
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'شما اجازه ورود به این صفحه را ندارید')
            # Redirect back to previous page safely
            return redirect(self.request.META.get('HTTP_REFERER', '/'))

        messages.warning(self.request, 'ابتدا وارد شوید')
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )

    def get(self,request):
        form = Increase_user_credit()
        return render(request,'sales/credit_increase.html',{'form':form})

    @transaction.atomic
    def post(self, request):
        form = Increase_user_credit(request.POST)

        if form.is_valid():

            user = form.cleaned_data.get('username')
            credit_to_add = form.cleaned_data.get('credit')


            User.objects.filter(pk=user.pk).update(credit=F('credit') + credit_to_add) # F reads from data base at the moment so no mistake will happen if 2 admin try to increase at the same time.(only works on querysets.)

            messages.success(request,'مبلغ {} به کیف پول کاربر {} اضافه شد'.format(credit_to_add, user.username))
            return redirect('credit_increase')

        return render(request, 'sales/credit_increase.html', {'form': form})

@login_required
def send_to_payment(request):
    if request.method == 'POST':
        return redirect('payment')

    return redirect('cart_view')


class Temp_purchase(LoginRequiredMixin, View): # This is called temporary because it is going to be replaced with a real payment system

    def get(self,request):
        order = Order.objects.filter(user=request.user,status=StatusChoices.PENDING).first()

        # =============== Checking to see if a cart exists or not ===============
        if not order:
            messages.warning(request, "سفارش پیدا نشد.")
            return redirect('cart_view')
        # =======================================================================

        form = PaymentForm()
        remain = max(order.total - request.user.credit,0)
        context = {'order':order,'form':form, 'remain':remain}
        return render(request,'sales/payment.html', context)

    @transaction.atomic
    def post(self,request):
        order = Order.objects.select_for_update().filter(user=request.user, status=StatusChoices.PENDING).first()
        user = User.objects.select_for_update().get(pk=request.user.pk)

        # =============== Checking to see if a cart exists or not ===============
        if not order:
            messages.warning(request, "سفارش پیدا نشد.")
            return redirect('cart_view')
        # =======================================================================

        remain = max(order.total - user.credit, 0)
        form = PaymentForm(request.POST)
        context = {'order': order, 'form': form, 'remain': remain}

        if form.is_valid():

            use_credit = form.cleaned_data.get('use_credit')
            if use_credit:
                User.objects.filter(pk=request.user.pk).update(credit=Greatest(F('credit') - Value(order.total),Value(0)))
            else:
                # Since the amount added to user wallet (credits) is the same that is removed, without their initial credit touched,
                # we don't really need to make any changes here
                pass

            Order.objects.filter(pk=order.pk).update(status=StatusChoices.PAID)

            # ========================================== updating the number of items in cart ============================================
            update_cart_cache(request)
            # ============================================================================================================================

            messages.success(request,'تراکنش شما با موفقیت انجام شد.')

            return redirect('home')
        return render(request, 'sales/payment.html', context)




