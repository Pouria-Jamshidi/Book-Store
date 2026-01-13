from django.shortcuts import render, redirect

from core.models import Book


def home(request):
    books = Book.objects.all()
    render(request,'home.html',{'books':books})