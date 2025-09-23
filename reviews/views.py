from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from reviews.forms import BookForm

from .models import Book, Review

@login_required
def home(request):
    return render(request, "reviews/home.html")

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.review_set.all()
    return render(request, "reviews/book.html", {"book": book, "reviews": reviews})

@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = BookForm()
    return render(request, "reviews/book_create.html", {"form": form})