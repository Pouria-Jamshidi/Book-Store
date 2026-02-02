from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from core.models import Book, Score
from core.forms import NewAuthorForm, NewBookForm, NewGenreForm


def home(request):
    books = Book.objects.all()
    return render(request,'core/home.html',{'books':books})

def book_detail(request,book_id):
    book = get_object_or_404(Book,pk=book_id)
    # vote_count = book.scores.count()
    # return render(request,'core/book_detail.html',{'book':book,'vote_count':vote_count})
    return render(request,'core/book_detail.html',{'book':book})



class NewBook(LoginRequiredMixin, UserPassesTestMixin,View):
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
    def get(self,request,book_id):
        return redirect('book_detail',book_id=book_id)

    def post(self,request,book_id):
        book = get_object_or_404(Book,pk=book_id)
        score =request.POST.get('score')
        Score.objects.update_or_create(user=request.user,book=book, defaults={'score':score})
        messages.success(request,'امتیاز شما با موفقیت ثبت گردید')
        return redirect('book_detail',book_id=book_id)


