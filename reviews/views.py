from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from reviews.forms import BookForm, ReviewForm

from .models import Book, Review

@login_required
def home(request):
    return render(request, "reviews/home.html")

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.review_set.all()
    return render(request, "reviews/book.html", context = {"book": book, "reviews": reviews})

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

@login_required
def review_create(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = ReviewForm()
    return render(request, "reviews/review_create.html", {"form": form, "book": book})