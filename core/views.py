from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.paginator import Paginator
from core.models import Book, Score, NavbarGenre
from sales.models import Order, OrderItems, StatusChoices
from core.forms import NewAuthorForm, NewBookForm, NewGenreForm, NavbarForm


def home(request):
    """
    FBV: Rendering the main page with every books without filtering
    :param request:
    :return:
    """
    # ======================== Adding pagination ==========================
    p = Paginator(Book.objects.all(), 12)
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
        'navbar_items': NavbarGenre.objects.all(),
        'active_genre': None,
        'current_page': current_page,
        'total_pages': total_pages,
        'next_pages': next_pages,
        'previous_pages': previous_pages,
    }

    return render(request,'core/home.html',context)

def home_genre(request,genre_id):
    """
    FBV: Rendering main page with only the desired genre books
    :param request:
    :param genre_id: ID of desired genre
    :return:
    """

    # ======================== Adding pagination ==========================
    p = Paginator(Book.objects.filter(genre= genre_id), 12)
    page = request.GET.get('page')
    books = p.get_page(page)
    # ======================== for page surfing ===========================
    current_page = books.number
    total_pages = p.num_pages
    next_pages = [i for i in range(current_page+1,min(current_page+5,total_pages)+1)] # min prevents numbers above max page
    previous_pages = [i for i in range(max(current_page-5,1),current_page)] # max prevents numbers below 1
    # =====================================================================

    context = {
        'books': books,
        'navbar_items': NavbarGenre.objects.all(),
        'active_genre': genre_id,
        'current_page': current_page,
        'total_pages': total_pages,
        'next_pages': next_pages,
        'previous_pages': previous_pages,
    }

    return render(request,'core/home.html',context)

def home_author(request,author_id):
    """
    FBV: Rendering main page with only the desired author books
    :param request:
    :param author_id: ID of the desired author
    :return:
    """

    # ======================== Adding pagination ==========================
    p = Paginator(Book.objects.filter(author= author_id), 12)
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
        'navbar_items': NavbarGenre.objects.all(),
        'active_genre': None,
        'current_page': current_page,
        'total_pages': total_pages,
        'next_pages': next_pages,
        'previous_pages': previous_pages,
    }

    return render(request,'core/home.html',context)

def book_detail(request,book_id):
    """
    FBV: renders a page that shows selected book's detail.\n
    context for template:\n
    1. what book
    2. if it is already purchased
    3. If the user currently has the book in their shopping cart
    :param request:
    :param book_id: ID of the desired book
    :return:
    """
    book = get_object_or_404(Book,pk=book_id)

    # ================================= Check to see if user has already purchased , show download ======================================
    if request.user.is_authenticated:
        already_purchased = OrderItems.objects.filter(
            order__user=request.user,
            order__status=StatusChoices.PAID,
            book=book
        ).exists()
    else:
        already_purchased = False
    # ===================================================================================================================================

    # ================================ Check to see if it is in cart , delete if from the cart ==========================================
    def in_cart():
        if request.user.is_authenticated:
            order = Order.objects.filter(
                user=request.user,
                status=StatusChoices.PENDING
            ).first()

            item = OrderItems.objects.filter(
                order=order,
                book=book
            ).first()
        else:
            item = False

        return item
    # ===================================================================================================================================

    # # ============================== Counting the number of scores ==============================
    # vote_count = book.scores.count()
    # return render(request,'core/book_detail.html',{'book':book,'vote_count':vote_count})
    # # ===========================================================================================

    context = {'book':book, 'purchased': already_purchased, 'in_cart':in_cart()}

    return render(request,'core/book_detail.html', context)


class NewBook(LoginRequiredMixin, UserPassesTestMixin,View):
    """
    CBV: Renders a page where user can fill in a form to add new books in DB\n
    - user needs to be staff or superuser
    """

    def get(self,request):
        form = NewBookForm()
        return render(request, 'core/new_book.html',{'form':form})

    def post(self,request):
        form = NewBookForm(request.POST, request.FILES)
        if form.is_valid():
            # data = form.cleaned_data
            # genres = data.pop('genre')
            form.save()
            messages.success(request,'کتاب "{}" از نویسنده "{}" با موفقیت اضافه شد.'.format(form.cleaned_data.get('title'),form.cleaned_data.get('author')))
            return redirect('newbook')
        return render(request, 'core/new_book.html',{'form':form})

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'شما اجازه ورود به این صفحه را ندارید')
            # Redirect back to previous page safely
            return redirect(self.request.META.get('HTTP_REFERER', '/'))

        messages.warning(self.request,'ابتدا وارد شوید')
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )

class NewAuthorView(LoginRequiredMixin, UserPassesTestMixin,View):
    """
    CBV: Renders a page where user can fill in a form to add new authors in DB\n
    - user needs to be staff or superuser
    """
    def get(self,request):
        form = NewAuthorForm()
        return render(request, 'core/new_author.html',{'form':form})

    def post(self,request):
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'نویسنده جدید ({}) با موفقیت ثبت شد.'.format(form.cleaned_data.get('name')))
            return redirect('newauthor')
        return render(request, 'core/new_author.html',{'form':form})

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'شما اجازه ورود به این صفحه را ندارید')
            return redirect(self.request.META.get('HTTP_REFERER', '/'))

        messages.warning(self.request, 'ابتدا وارد شوید')
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )

class NewGenreView(LoginRequiredMixin, UserPassesTestMixin,View):
    """
    CBV: Renders a page where user can fill in a form to add new genres in DB\n
    - user needs to be staff or superuser
    """
    def get(self,request):
        form = NewGenreForm()
        return render(request, 'core/new_genre.html',{'form':form})

    def post(self,request):
        form = NewGenreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ژانرا جدید ({}) با موفقیت ثبت گردید'.format(form.cleaned_data.get('name')))
            return redirect('newgenre')
        return render(request, 'core/new_genre.html',{'form':form})


    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'شما اجازه ورود به این صفحه را ندارید')
            return redirect(self.request.META.get('HTTP_REFERER', '/'))

        messages.warning(self.request, 'ابتدا وارد شوید')
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )

class BookScoreView(LoginRequiredMixin, View):
    """
    CBV: Allow user submit a score for the book\n
    user needs to be logged in.
    """
    def get(self,request,book_id):
        return redirect('book_detail',book_id=book_id)

    def post(self,request,book_id):
        book = get_object_or_404(Book,pk=book_id)
        score =request.POST.get('score')
        Score.objects.update_or_create(user=request.user,book=book, defaults={'score':score})
        messages.success(request,'امتیاز شما با موفقیت ثبت گردید')
        return redirect('book_detail',book_id=book_id)


class NavbarView(LoginRequiredMixin, UserPassesTestMixin,View):
    """
    CBV: Renders a page with form for changing navbar genre items.\n
    - user need to be logged in and be staff or superuser
    """

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'شما اجازه ورود به این صفحه را ندارید')
            return redirect(self.request.META.get('HTTP_REFERER', '/'))

        messages.warning(self.request, 'ابتدا وارد شوید')
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )

    def get_initial_from_db(self):
        """
        CBV: Builds initial dictionary like {'genre1': <genre_pk>, 'genre2': <genre_pk>, ...}
        Only include positions that exist in DB and are within 1 to MAX_ITEMS.
        """
        initial = {}
        for ng in NavbarGenre.objects.all():
            pos = ng.position
            if 1 <= pos <= NavbarForm.MAX_ITEMS:
                initial[f'genre{pos}'] = ng.genre_id
        return initial

    def get(self,request):
        initial = self.get_initial_from_db()
        form = NavbarForm(initial=initial)
        return render(request,'core/navbar_genres.html', {'form':form})

    def post(self,request):
        form = NavbarForm(request.POST)
        if form.is_valid():
            for i in range(1, form.MAX_ITEMS+1):
                genre = form.cleaned_data.get('genre{}'.format(i))
                NavbarGenre.objects.update_or_create(position=i, defaults={'genre':genre})
            messages.success(request, "منو نوار ناوبری شما با موفقیت ثبت گردید")
            return redirect('home')
        return render(request,'core/navbar_genres.html', {'form':form})