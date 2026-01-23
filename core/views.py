from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from core.models import Book
from core.forms import NewBookForm

def home(request):
    books = Book.objects.all()
    return render(request,'core/home.html',{'books':books})

def book_detail(request,book_id):
    book = get_object_or_404(Book,pk=book_id)
    return render(request,'core/book_detail.html',{'book':book})

class NewBook(View):
    def get(self,request):
        form = NewBookForm()
        return render(request, 'core/new_book.html',{'newBook_form':form})

    def post(self,request):
        form = NewBookForm(request.POST, request.FILES)
        if form.is_valid():
            form = NewBookForm(request.POST, request.FILES)
            form.save()
            messages.success(request,'کتاب با موفقیت اضافه شد.')
            return redirect('home')