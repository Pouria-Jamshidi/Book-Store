from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery, IntegerField, Exists, Sum, F
from accounts.forms import Register_form, Login_form
from core.models import Book,Score
from sales.models import StatusChoices, Order, OrderItems
from sales.services import update_cart_cache

User = get_user_model()

class RegisterView(View):
    def get(self, request):
        form = Register_form()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = Register_form(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'اکانت شما به نام کاربری {} ساخته شد!'.format(new_user.username))
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})

class Login_view(LoginView):
    form_class = Login_form
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'شما قبلاً وارد شده‌اید')
            # check for next parameter
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            # fallback to default success_url
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        #  ===================== Remember me ======================
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        #  ================== End of Remember me ==================

        user = form.get_user()
        messages.success(self.request,'کاربر {} با موفقیت وارد شد'.format(user.username))

        # ======================================== To update the number of cart items in session when user logs in ===================================
        # return super().form_valid(form)
        response = super().form_valid(form) # performs the login adn save the http response in a variable
        update_cart_cache(self.request) # update the number of cart items
        return response # Return the saved http response
        # =================================================================================================================================


    def form_invalid(self, form):
        messages.error(self.request, 'کاربری با این مشخصات یافت نشد')
        return super().form_invalid(form)


class logout_view(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.success(request,'شما با موفقیت خارج شدید')
        return super().dispatch(request,*args,**kwargs)

@login_required
def profile_fbv(request):
    return render(request,'accounts/profile.html',{'active':'profile'})

@login_required
def profile_books_fbv(request):

    owned_books = Book.objects.filter(orderitems__order__user=request.user,orderitems__order__status=StatusChoices.PAID).distinct().order_by('-orderitems__order__updated_at', 'title')

    # ======================== Adding pagination ==========================
    p=Paginator(owned_books,8)
    page = request.GET.get('page')
    books = p.get_page(page)
    # ======================== for page surfing ===========================
    current_page = books.number
    total_pages = p.num_pages
    next_pages = [i for i in range(current_page + 1, min(current_page + 5, total_pages) + 1)]  # min prevents numbers above max page
    previous_pages = [i for i in range(max(current_page - 5, 1), current_page)]  # max prevents numbers below 1
    # =====================================================================

    context = {
        'books': books,
        'current_page': current_page,
        'total_pages': total_pages,
        'next_pages': next_pages,
        'previous_pages': previous_pages,
        'active': 'books'
    }
    return render(request,'accounts/profile_books.html',context)

@login_required
def profile_scored_books_fbv(request):

    # ===================== User score for the book =======================
    user_score_subq = Score.objects.filter(user=request.user, book=OuterRef('pk'),score__gte=1).values('score')[:1]
    owned_books = (Book.objects.filter(orderitems__order__user=request.user,orderitems__order__status=StatusChoices.PAID)
                   .filter(Exists(user_score_subq))
                   .annotate(user_score=(Subquery(user_score_subq,output_field=IntegerField()))).distinct()
                   .order_by('-orderitems__order__updated_at', 'title')
                   )
    # =====================================================================

    # ======================== Adding pagination ==========================
    p=Paginator(owned_books,8)
    page = request.GET.get('page')
    books = p.get_page(page)
    # ======================== for page surfing ===========================
    current_page = books.number
    total_pages = p.num_pages
    next_pages = [i for i in range(current_page + 1, min(current_page + 5, total_pages) + 1)]  # min prevents numbers above max page
    previous_pages = [i for i in range(max(current_page - 5, 1), current_page)]  # max prevents numbers below 1
    # =====================================================================

    context = {
        'books': books,
        'current_page': current_page,
        'total_pages': total_pages,
        'next_pages': next_pages,
        'previous_pages': previous_pages,
        'active': 'scored'
    }
    return render(request, 'accounts/profile_books_score.html', context)

@login_required
def profile_not_scored_books_fbv(request):

    # ===================== User score for the book =======================
    user_score_subq = Score.objects.filter(user=request.user, book=OuterRef('pk'),score__gte=1).values('score')[:1]
    owned_books = (Book.objects.filter(orderitems__order__user=request.user,orderitems__order__status=StatusChoices.PAID)
                   .exclude(Exists(user_score_subq))
                   .annotate(user_score=(Subquery(user_score_subq,output_field=IntegerField()))).distinct()
                   .order_by('-orderitems__order__updated_at', 'title')
                   )
    # =====================================================================

    # ======================== Adding pagination ==========================
    p=Paginator(owned_books,8)
    page = request.GET.get('page')
    books = p.get_page(page)
    # ======================== for page surfing ===========================
    current_page = books.number
    total_pages = p.num_pages
    next_pages = [i for i in range(current_page + 1, min(current_page + 5, total_pages) + 1)]  # min prevents numbers above max page
    previous_pages = [i for i in range(max(current_page - 5, 1), current_page)]  # max prevents numbers below 1
    # =====================================================================

    context = {
        'books': books,
        'current_page': current_page,
        'total_pages': total_pages,
        'next_pages': next_pages,
        'previous_pages': previous_pages,
        'active': 'not-scored'
    }
    return render(request,'accounts/profile_books_score.html',context)


@login_required
def profile_orders_fbv(request):


    orders=Order.objects.filter(user=request.user,status=StatusChoices.PAID).annotate(len_items =Sum("items__quantity")).order_by('-updated_at')
    # =====================================================================

    # ======================== Adding pagination ==========================
    p=Paginator(orders,4)
    page = request.GET.get('page')
    books = p.get_page(page)
    # ======================== for page surfing ===========================
    current_page = books.number
    total_pages = p.num_pages
    next_pages = [i for i in range(current_page + 1, min(current_page + 5, total_pages) + 1)]  # min prevents numbers above max page
    previous_pages = [i for i in range(max(current_page - 5, 1), current_page)]  # max prevents numbers below 1
    # =====================================================================

    context = {
        'orders': orders,
        'current_page': current_page,
        'total_pages': total_pages,
        'next_pages': next_pages,
        'previous_pages': previous_pages,
        'active': 'orders'
    }
    return render(request,'accounts/profile_orders.html',context)

@login_required
def profile_order_items_fbv(request,order_id):
    order_items = OrderItems.objects.filter(order__user=request.user, order=order_id).order_by('-price')
    # order_items = Book.objects.filter(orderitems__order=order_id,orderitems__order__user=request.user).order_by('-price')

    context = {
        'items': order_items,
        'order_id': order_id,
        'active': 'orders'
    }
    return render(request,'accounts/profile_order_items.html',context)