from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Book, Review

@login_required
def home(request):
    return render(request, "reviews/home.html")

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    reviews = book.review_set.all()
    return render(request, "reviews/book.html", {"book": book, "reviews": reviews})